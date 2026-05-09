import uuid
import os
import json
import logging
import shutil
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel

from src.api.auth.auth import get_current_user, require_admin, get_optional_user
from src.db.connection import get_connection
from src.models.image import Image, IMAGE_STATES

from src.services.eof_service import analyze_eof
from src.services.exif_service import detect_exif, sanitize_image
from src.services.histogram_service import analyze_histogram
from src.services.lsb_service import analyze_lsb
from src.services.mime_service import validate_mime

logger = logging.getLogger(__name__)

class PatchImageRequest(BaseModel):
  state: str | None = None


router = APIRouter(prefix="/images", tags=["images"])

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

os.makedirs(UPLOAD_DIR, exist_ok=True)


def check_image_suspicious(path: str) -> dict:
  results = {}
  risks = []

  # MIME (structural re-check from disk)
  with open(path, "rb") as f:
    mime_result = validate_mime(f.read(2048))
  results["mime"] = mime_result
  if not mime_result["valid"]:
    risks.append(f"MIME inválido: {mime_result['mime']}")

  # EXIF (detect before sanitizing)
  exif_result = detect_exif(path)
  results["exif"] = exif_result
  if exif_result["risks"]:
    risks.extend(exif_result["risks"])

  # EOF
  eof_result = analyze_eof(path)
  results["eof"] = eof_result
  if eof_result["suspicious"]:
    reason = eof_result.get("reason") or f"{eof_result.get('extra_bytes')} bytes extra tras EOF"
    risks.append(f"EOF sospechoso: {reason}")

  # Histogram
  histogram_result = analyze_histogram(path)
  results["histogram"] = histogram_result
  if histogram_result["suspicious"]:
    risks.append(f"Histograma sospechoso: varianza {histogram_result['variance']:.2f}")

  # LSB
  lsb_result = analyze_lsb(path)
  results["lsb"] = lsb_result
  if lsb_result["suspicious"]:
    risks.append(f"LSB sospechoso: ratio {lsb_result['lsb_ratio']:.4f}")

  return {
    "suspicious": len(risks) > 0,
    "risks": risks,
    "details": results,
  }


@router.get('/suspicious')
def get_suspicious_images(user: dict = Depends(require_admin)):
  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        """
        SELECT i.image_id, i.image_name, i.image_date_uploaded, i.image_path,
               i.image_mimetype, i.image_state, i.image_analysis,
               u.user_id, u.user_name
        FROM IMAGES i
        JOIN ALBUM_IMAGES ai ON i.image_id = ai.image_id
        JOIN ALBUMS a ON ai.album_id = a.album_id
        JOIN USERS u ON a.user_id = u.user_id
        WHERE i.image_state = 'Sospechoso'
        """
      )
      rows = cur.fetchall()

  return [
    {
      "image": Image(
        id=row[0],
        name=row[1],
        date_uploaded=row[2],
        path=row[3],
        mimetype=row[4],
        state=IMAGE_STATES(row[5]),
        analysis=row[6],
      ).to_dict(),
      "owner": {
        "id": row[7],
        "name": row[8]
      }
    }
    for row in rows
  ]


@router.get('/id/{image_id}')
def get_image_by_id(image_id: str, user: dict = Depends(get_current_user)):
  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        """
        SELECT image_id, image_name, image_date_uploaded, image_path,
               image_mimetype, image_state, image_analysis
        FROM IMAGES
        WHERE image_id = %s
        """,
        (image_id,),
      )
      row = cur.fetchone()

  if not row:
    raise HTTPException(status_code=404, detail="Imagen no encontrada")

  return Image(
    id=row[0],
    name=row[1],
    date_uploaded=row[2],
    path=row[3],
    mimetype=row[4],
    state=IMAGE_STATES(row[5]),
    analysis=row[6],
  ).to_dict()


@router.get('/album/{album_id}')
def get_images_by_album(album_id: str, user: Optional[dict] = Depends(get_optional_user)):
  """
  Visitantes sin auth solo ven imágenes 'Limpio' de álbumes 'Aprobado'.
  Usuarios autenticados ven todas las imágenes del álbum.
  """
  with get_connection() as conn:
    with conn.cursor() as cur:
      if user:
        cur.execute(
          """
          SELECT i.image_id, i.image_name, i.image_date_uploaded, i.image_path,
                 i.image_mimetype, i.image_state, i.image_analysis
          FROM IMAGES i
          JOIN ALBUM_IMAGES ai ON i.image_id = ai.image_id
          WHERE ai.album_id = %s
          """,
          (album_id,),
        )
      else:
        cur.execute(
          """
          SELECT i.image_id, i.image_name, i.image_date_uploaded, i.image_path,
                 i.image_mimetype, i.image_state, i.image_analysis
          FROM IMAGES i
          JOIN ALBUM_IMAGES ai ON i.image_id = ai.image_id
          JOIN ALBUMS a ON ai.album_id = a.album_id
          WHERE ai.album_id = %s
            AND i.image_state = 'Limpio'
            AND a.album_state = 'Aprobado'
          """,
          (album_id,),
        )
      rows = cur.fetchall()

  return [
    Image(
      id=row[0],
      name=row[1],
      date_uploaded=row[2],
      path=row[3],
      mimetype=row[4],
      state=IMAGE_STATES(row[5]),
      analysis=row[6],
    ).to_dict()
    for row in rows
  ]


@router.post("/", status_code=201)
def post_image(
  album_id: str,
  file: UploadFile = File(...),
  user: dict = Depends(get_current_user)
):
  # Primero se lee el contenido en memoria primero
  content = file.file.read()
  size = len(content)

  # Luego se valida el tamaño antes de guardar
  if size > MAX_FILE_SIZE:
    raise HTTPException(status_code=413, detail="Archivo demasiado grande. Máximo 10 MB.")

  # Validar MIME en memoria (antes de tocar el disco)
  mime_result = validate_mime(content[:2048])
  if not mime_result["valid"]:
    raise HTTPException(status_code=415, detail=f"Tipo de archivo no permitido: {mime_result['mime']}")

  # Guardar en disco solo si pasó las validaciones
  image_id  = str(uuid.uuid4())
  extension = os.path.splitext(str(file.filename))[1].lower()
  file_path = os.path.join(UPLOAD_DIR, f"{image_id}{extension}")

  with open(file_path, "wb") as buffer:
    buffer.write(content)

  suspicious_dict = check_image_suspicious(file_path)
  logger.debug("Análisis de imagen %s: %s", image_id, suspicious_dict)

  # Sanitizar EXIF (strip de metadatos del archivo almacenado)
  sanitize_image(file_path, file_path)

  image_state = IMAGE_STATES.SOSPECHOSO if suspicious_dict['suspicious'] else IMAGE_STATES.LIMPIO

  # Persistir en DB incluyendo resultados del análisis
  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        """
        INSERT INTO IMAGES (image_id, image_name, image_size, image_path, image_mimetype, image_state, image_analysis)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING image_id, image_name, image_date_uploaded, image_path, image_mimetype, image_state, image_analysis
        """,
        (image_id, file.filename, size, file_path, file.content_type, image_state.value, json.dumps(suspicious_dict)),
      )
      image_row = cur.fetchone()

      cur.execute(
        "INSERT INTO ALBUM_IMAGES (album_id, image_id) VALUES (%s, %s)",
        (album_id, image_id),
      )
    conn.commit()

  return Image(
    id=image_row[0],
    name=image_row[1],
    date_uploaded=image_row[2],
    path=image_row[3],
    mimetype=image_row[4],
    state=IMAGE_STATES(image_row[5]),
    analysis=image_row[6],
  ).to_dict()


@router.patch('/id/{image_id}')
def patch_image(image_id: str, body: PatchImageRequest, user: dict = Depends(require_admin)):
  if not body.state:
    raise HTTPException(status_code=400, detail="No se enviaron campos a actualizar")

  try:
    IMAGE_STATES(body.state)
  except ValueError:
    raise HTTPException(status_code=400, detail=f"Estado inválido: {body.state}")

  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        """
        UPDATE IMAGES
        SET image_state = %s
        WHERE image_id = %s
        RETURNING image_id, image_name, image_date_uploaded, image_path, image_mimetype, image_state, image_analysis
        """,
        (body.state, image_id),
      )
      row = cur.fetchone()
    conn.commit()

  if not row:
    raise HTTPException(status_code=404, detail="Imagen no encontrada")

  return Image(
    id=row[0],
    name=row[1],
    date_uploaded=row[2],
    path=row[3],
    mimetype=row[4],
    state=IMAGE_STATES(row[5]),
    analysis=row[6],
  ).to_dict()
