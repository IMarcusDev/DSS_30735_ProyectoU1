JPEG_MAGIC = b'\xff\xd8'
JPEG_EOF   = b'\xff\xd9'

PNG_MAGIC  = b'\x89PNG\r\n\x1a\n'
PNG_EOF    = b'\x49\x45\x4e\x44\xae\x42\x60\x82'  # IEND chunk + CRC


def analyze_eof(path: str) -> dict:
  with open(path, "rb") as f:
    data = f.read()

  if data[:2] == JPEG_MAGIC:
    eof_marker = JPEG_EOF
  elif data[:8] == PNG_MAGIC:
    eof_marker = PNG_EOF
  else:
    return {
      "suspicious": True,
      "reason": "Formato de archivo no reconocido"
    }

  eof_index = data.rfind(eof_marker)

  if eof_index == -1:
    return {
      "suspicious": True,
      "reason": "Marcador EOF no encontrado"
    }

  extra = data[eof_index + len(eof_marker):]

  return {
    "suspicious": len(extra) > 0,
    "extra_bytes": len(extra)
  }
