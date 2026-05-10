import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
BUCKET_NAME  = os.getenv("SUPABASE_BUCKET", "images")

_client: Client | None = None


def _get_client() -> Client:
  global _client
  if _client is None:
    if not SUPABASE_URL or not SUPABASE_KEY:
      raise RuntimeError("SUPABASE_URL y SUPABASE_KEY no están configurados en el .env")
    _client = create_client(SUPABASE_URL, SUPABASE_KEY)
  return _client


def upload_image(local_path: str, storage_key: str, content_type: str) -> str:
  """Sube un archivo local al bucket y devuelve su URL pública."""
  client = _get_client()
  with open(local_path, "rb") as f:
    client.storage.from_(BUCKET_NAME).upload(
      path=storage_key,
      file=f.read(),
      file_options={"content-type": content_type, "upsert": "false"},
    )
  return client.storage.from_(BUCKET_NAME).get_public_url(storage_key)


def delete_from_storage(public_url: str) -> None:
  """Elimina una imagen del bucket a partir de su URL pública."""
  client = _get_client()
  marker = f"/object/public/{BUCKET_NAME}/"
  if marker in public_url:
    storage_key = public_url.split(marker, 1)[1]
    client.storage.from_(BUCKET_NAME).remove([storage_key])
