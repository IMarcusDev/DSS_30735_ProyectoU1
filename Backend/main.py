import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv

load_dotenv()

from src.api.router import router
from src.utils.limiter import limiter

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["GET", "POST", "PATCH", "DELETE"],
  allow_headers=["Authorization", "Content-Type"],
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
  response = await call_next(request)
  response.headers["X-Content-Type-Options"] = "nosniff"
  response.headers["X-Frame-Options"] = "DENY"
  response.headers["X-XSS-Protection"] = "1; mode=block"
  response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
  response.headers["Content-Security-Policy"] = (
    "default-src 'self'; "
    "img-src 'self' data: blob:; "
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline';"
  )
  return response

app.include_router(router)
