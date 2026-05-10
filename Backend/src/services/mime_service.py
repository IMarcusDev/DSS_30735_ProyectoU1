import magic

ALLOWED_MIMES = {
  "image/jpeg",
  "image/png"
}

def validate_mime(file_bytes: bytes) -> dict:
  mime = magic.from_buffer(file_bytes, mime=True)

  return {
    "valid": mime in ALLOWED_MIMES,
    "mime": mime
  }