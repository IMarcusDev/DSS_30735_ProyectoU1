from fastapi import HTTPException
import jwt
import uuid
from datetime import datetime, timedelta, timezone

SECRET_KEY = "clavesecretajasja"  # Maybe pasarlo al .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas


def create_token(user_id: str, role: str) -> str:
  payload = {
    "sub": user_id,
    "role": role,
    "jti": str(uuid.uuid4()),
    "iat": datetime.now(timezone.utc),
    "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
  }
  return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
  try:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=401, detail="Token expirado")
  except jwt.InvalidTokenError:
    raise HTTPException(status_code=401, detail="Token inválido")
