from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
import bcrypt
import uuid

from src.db.connection import get_connection
from src.utils.jwt import decode_token, create_token

router = APIRouter(prefix="/auth", tags=["auth"])

bearer_scheme = HTTPBearer()

# Aux Classes
class LoginRequest(BaseModel):
  email: EmailStr
  password: str

class RegisterRequest(BaseModel):
  name: str
  last_name: str
  email: EmailStr
  password: str


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
  return decode_token(credentials.credentials)

def require_admin(user: dict = Depends(get_current_user)) -> dict:
  if user["role"] != "Administrator":
    raise HTTPException(status_code=403, detail="Sin permisos")
  return user


@router.post("/register", status_code=201)
def register(body: RegisterRequest):
  password_hash = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode()

  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute("SELECT 1 FROM USERS WHERE user_email = %s", (body.email,))
      if cur.fetchone():
        raise HTTPException(status_code=409, detail="El email ya está registrado")

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
def login(body: LoginRequest):
  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        "SELECT user_id, user_role, user_password FROM USERS WHERE user_email = %s",
        (body.email,),
      )
      row = cur.fetchone()

  if not row or not bcrypt.checkpw(body.password.encode(), row[2].encode()):
    raise HTTPException(status_code=401, detail="Credenciales inválidas")

  token = create_token(user_id=row[0], role=row[1])
  return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def me(user: dict = Depends(get_current_user)):
  return {"user_id": user["sub"], "role": user["role"]}
