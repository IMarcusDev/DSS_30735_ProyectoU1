import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.api.auth.auth import get_current_user, require_admin
from src.models.album import Album
from src.db.connection import get_connection

router = APIRouter(prefix="/albums", tags=["albums"])

class CreateAlbumRequest(BaseModel):
  name: str

class PatchAlbumRequest(BaseModel):
  name: str | None = None
  state: str | None = None

@router.get('/id/{album_id}')
def getAlbumById(album_id: str):
  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        """
        SELECT album_id, album_name, album_date_created, album_state
        FROM albums
        WHERE album_id = %s
        """,
        (album_id),
      )
      row = cur.fetchone()

  return Album(
    id=row[0],
    name=row[1],
    date_created=row[2],
    state=row[3],
  ).to_dict()

@router.get('/')
def getAlbumsByUserId(user: dict = Depends(get_current_user)):
  albums: list[Album] = []
  print(user)

  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        """
        SELECT album_id, album_name, album_date_created, album_state
        FROM albums
        WHERE user_id = %s
        """,
        (user['sub'],),
      )
      rows = cur.fetchall()

      for row in rows:
        albums.append(Album(
          id=row[0],
          name=row[1],
          date_created=row[2],
          state=row[3],
        ))

  return [album.to_dict() for album in albums]


@router.post('/')
def postAlbum(body: CreateAlbumRequest, user: dict = Depends(get_current_user)):
  album_id = str(uuid.uuid4())
  name = body.name

  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        """
        INSERT INTO ALBUMS (album_id, album_name, user_id)
        VALUES (%s, %s, %s)
        RETURNING album_id, album_name, album_date_created, album_state
        """,
        (album_id, name, user['sub']),
      )
      row = cur.fetchone()
    conn.commit()

  return Album(
    id=row[0],
    name=row[1],
    date_created=row[2],
    state=row[3],
  ).to_dict()

@router.get('/pending')
def getPendingAlbums(user: dict = Depends(require_admin)):
  albums = []

  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        """
        SELECT a.album_id, a.album_name, a.album_date_created, a.album_state, u.user_id, u.user_name
        FROM albums a
        JOIN users u ON a.user_id = u.user_id
        WHERE album_state = 'Pendiente'
        """,
        (),
      )
      rows = cur.fetchall()

      for row in rows:
        album = Album(
          id=row[0],
          name=row[1],
          date_created=row[2],
          state=row[3],
        )

        albums.append({
          **album.to_dict(),
          "owner": {
            "id": row[4],
            "name": row[5]
          }
        })

    return albums


@router.patch('/id/{album_id}')
def patchAlbum(album_id: str, body: PatchAlbumRequest, user: dict = Depends(require_admin)):
  fields = {}
  if body.name  is not None: fields["album_name"]  = body.name
  if body.state is not None: fields["album_state"] = body.state

  if not fields:
    raise HTTPException(status_code=400, detail="No se enviaron campos a actualizar")

  set_clause = ", ".join(f"{col} = %s" for col in fields)
  values     = list(fields.values()) + [album_id]

  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        f"""
        UPDATE ALBUMS
        SET {set_clause}
        WHERE album_id = %s
        RETURNING album_id, album_name, album_date_created, album_state
        """,
        values,
      )
      row = cur.fetchone()
    conn.commit()

  if not row:
    raise HTTPException(status_code=404, detail="Álbum no encontrado")

  return Album(
    id=row[0],
    name=row[1],
    date_created=row[2],
    state=row[3],
  ).to_dict()
