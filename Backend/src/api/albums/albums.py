import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from src.api.auth.auth import get_current_user, require_admin
from src.models.album import Album, ALBUM_STATES
from src.db.connection import get_connection

router = APIRouter(prefix="/albums", tags=["albums"])

ALLOWED_PATCH_FIELDS = {"album_name", "album_description", "album_is_public", "album_state"}

class CreateAlbumRequest(BaseModel):
  name: str = Field(min_length=1, max_length=150)
  description: str = Field(default="", max_length=500)
  is_public: bool = True

class PatchAlbumRequest(BaseModel):
  name: str | None = Field(default=None, min_length=1, max_length=150)
  description: str | None = Field(default=None, max_length=500)
  state: str | None = None
  is_public: bool | None = None


@router.get('/id/{album_id}')
def getAlbumById(album_id: str):
  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        """
        SELECT album_id, album_name, album_description, album_is_public, album_date_created, album_state
        FROM albums
        WHERE album_id = %s
        """,
        (album_id,),
      )
      row = cur.fetchone()

  if not row:
    raise HTTPException(status_code=404, detail="Álbum no encontrado")

  return Album(
    id=row[0],
    name=row[1],
    description=row[2],
    is_public=row[3],
    date_created=row[4],
    state=ALBUM_STATES(row[5]),
  ).to_dict()


@router.get('/')
def getAlbumsByUserId(user: dict = Depends(get_current_user)):
  albums = []

  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        """
        SELECT a.album_id, a.album_name, a.album_description, a.album_is_public,
               a.album_date_created, a.album_state,
               COUNT(ai.image_id) AS image_count
        FROM albums a
        LEFT JOIN album_images ai ON a.album_id = ai.album_id
        WHERE a.user_id = %s
        GROUP BY a.album_id, a.album_name, a.album_description,
                 a.album_is_public, a.album_date_created, a.album_state
        """,
        (user['sub'],),
      )
      rows = cur.fetchall()

      for row in rows:
        album = Album(
          id=row[0],
          name=row[1],
          description=row[2],
          is_public=row[3],
          date_created=row[4],
          state=ALBUM_STATES(row[5]),
        )
        albums.append({**album.to_dict(), "image_count": row[6]})

  return albums


@router.post('/')
def postAlbum(body: CreateAlbumRequest, user: dict = Depends(get_current_user)):
  album_id = str(uuid.uuid4())

  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        """
        INSERT INTO ALBUMS (album_id, album_name, album_description, album_is_public, user_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING album_id, album_name, album_description, album_is_public, album_date_created, album_state
        """,
        (album_id, body.name, body.description, body.is_public, user['sub']),
      )
      row = cur.fetchone()
    conn.commit()

  return Album(
    id=row[0],
    name=row[1],
    description=row[2],
    is_public=row[3],
    date_created=row[4],
    state=ALBUM_STATES(row[5]),
  ).to_dict()


@router.get('/public')
def getPublicAlbums():
  albums = []

  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        """
        SELECT a.album_id, a.album_name, a.album_description, a.album_is_public,
               a.album_date_created, a.album_state, u.user_name
        FROM albums a
        JOIN users u ON a.user_id = u.user_id
        WHERE a.album_state = 'Aprobado' AND a.album_is_public = TRUE
        ORDER BY a.album_date_created DESC
        """,
      )
      rows = cur.fetchall()

      for row in rows:
        album = Album(
          id=row[0],
          name=row[1],
          description=row[2],
          is_public=row[3],
          date_created=row[4],
          state=ALBUM_STATES(row[5]),
        )
        albums.append({
          **album.to_dict(),
          "author_name": row[6],
        })

  return albums


@router.get('/pending')
def getPendingAlbums(user: dict = Depends(require_admin)):
  albums = []

  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        """
        SELECT a.album_id, a.album_name, a.album_description, a.album_is_public,
               a.album_date_created, a.album_state, u.user_id, u.user_name
        FROM albums a
        JOIN users u ON a.user_id = u.user_id
        WHERE album_state = 'Pendiente'
        """,
      )
      rows = cur.fetchall()

      for row in rows:
        album = Album(
          id=row[0],
          name=row[1],
          description=row[2],
          is_public=row[3],
          date_created=row[4],
          state=ALBUM_STATES(row[5]),
        )
        albums.append({
          **album.to_dict(),
          "owner": {
            "id": row[6],
            "name": row[7]
          }
        })

    return albums


@router.patch('/id/{album_id}')
def patchAlbum(album_id: str, body: PatchAlbumRequest, user: dict = Depends(require_admin)):
  fields = {}
  if body.name        is not None: fields["album_name"]        = body.name
  if body.description is not None: fields["album_description"] = body.description
  if body.state       is not None: fields["album_state"]       = body.state
  if body.is_public   is not None: fields["album_is_public"]   = body.is_public

  if not fields:
    raise HTTPException(status_code=400, detail="No se enviaron campos a actualizar")

  # Whitelist de columnas permitidas para evitar inyección
  for col in fields:
    if col not in ALLOWED_PATCH_FIELDS:
      raise HTTPException(status_code=400, detail=f"Campo no permitido: {col}")

  set_clause = ", ".join(f"{col} = %s" for col in fields)
  values     = list(fields.values()) + [album_id]

  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        f"""
        UPDATE ALBUMS
        SET {set_clause}
        WHERE album_id = %s
        RETURNING album_id, album_name, album_description, album_is_public, album_date_created, album_state
        """,
        values,
      )
      row = cur.fetchone()

      if row and body.state in ('Aprobado', 'Negado'):
        action = 'album_approved' if body.state == 'Aprobado' else 'album_rejected'
        cur.execute(
          """
          INSERT INTO audit_logs (supervisor_id, action, target_type, target_id, target_name)
          VALUES (%s, %s, 'album', %s, %s)
          """,
          (user['sub'], action, row[0], row[1]),
        )

    conn.commit()

  if not row:
    raise HTTPException(status_code=404, detail="Álbum no encontrado")

  return Album(
    id=row[0],
    name=row[1],
    description=row[2],
    is_public=row[3],
    date_created=row[4],
    state=ALBUM_STATES(row[5]),
  ).to_dict()
