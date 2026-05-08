from fastapi import APIRouter

from src.api.auth.auth import router as auth_router
from src.api.images.images import router as images_router
from src.api.albums.albums import router as album_router

router = APIRouter()

# Routes
router.include_router(auth_router)
router.include_router(images_router)
router.include_router(album_router)


@router.get("/")
async def root():
  return {"message": "Backend corriendo :p"}
