from fastapi import APIRouter, UploadFile, File

router = APIRouter()


@router.get("/")
async def root():
  return {"message": "Backend corriendo :p"}


