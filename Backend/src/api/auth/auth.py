import re
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field, field_validator
import bcrypt
import uuid

from src.db.connection import get_connection
from src.utils.jwt import decode_token, create_token
from src.utils.limiter import limiter

router = APIRouter(prefix="/auth", tags=["auth"])

bearer_scheme = HTTPBearer()
optional_bearer = HTTPBearer(auto_error=False)


class LoginRequest(BaseModel):
  email: EmailStr
  password: str

class RegisterRequest(BaseModel):
  name: str = Field(min_length=1, max_length=100)
  last_name: str = Field(min_length=1, max_length=100)
  email: EmailStr
  password: str

  @field_validator('password')
  @classmethod
  def validate_password(cls, v: str) -> str:
    if len(v) < 8:
      raise ValueError('Mínimo 8 caracteres')
    if not re.search(r'[A-Z]', v):
      raise ValueError('Debe contener al menos una letra mayúscula')
    if not re.search(r'[0-9]', v):
      raise ValueError('Debe contener al menos un dígito')
    if not re.search(r'[!@#$%^&*()\-_=+\[\]{}|;:\'",.<>?/`~\\]', v):
      raise ValueError('Debe contener al menos un carácter especial')
    return v


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
  return decode_token(credentials.credentials)

def get_optional_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(optional_bearer)) -> Optional[dict]:
  if credentials is None:
    return None
  try:
    return decode_token(credentials.credentials)
  except HTTPException:
    return None

def require_admin(user: dict = Depends(get_current_user)) -> dict:
  if user["role"] != "Administrator":
    raise HTTPException(status_code=403, detail="Sin permisos")
  return user


@router.post("/register", status_code=201)
@limiter.limit("5/minute")
def register(request: Request, body: RegisterRequest):
  password_hash = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode()

  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute("SELECT 1 FROM USERS WHERE user_email = %s", (body.email,))
      if cur.fetchone():
        raise HTTPException(status_code=409, detail="No se pudo completar el registro")

      user_id = str(uuid.uuid4())
      cur.execute(
        """
        INSERT INTO USERS (user_id, user_name, user_last_name, user_email, user_password)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (user_id, body.name, body.last_name, body.email, password_hash),
      )
    conn.commit()

  return {"message": "Usuario registrado"}


@router.post("/login")
@limiter.limit("10/minute")
def login(request: Request, body: LoginRequest):
  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        "SELECT user_id, user_role, user_password FROM USERS WHERE user_email = %s",
        (body.email,),
      )
      row = cur.fetchone()

  dummy_hash = "$2b$12$KIXhW8C8W8C8W8C8W8C8uOeZzWzWzWzWzWzWzWzWzWzWzWzWzWzW2"
  stored_hash = row[2] if row else dummy_hash

  password_ok = bcrypt.checkpw(body.password.encode(), stored_hash.encode())

  if not row or not password_ok:
    raise HTTPException(status_code=401, detail="Credenciales inválidas")

  token = create_token(user_id=row[0], role=row[1])
  return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def me(user: dict = Depends(get_current_user)):
  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        "SELECT user_name, user_last_name, user_email FROM USERS WHERE user_id = %s",
        (user["sub"],),
      )
      row = cur.fetchone()

  if not row:
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

  return {
    "user_id":   user["sub"],
    "role":      user["role"],
    "name":      row[0],
    "last_name": row[1],
    "email":     row[2],
  }
