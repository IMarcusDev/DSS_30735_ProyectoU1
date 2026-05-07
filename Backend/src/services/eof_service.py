JPEG_EOF = b'\xff\xd9'

def analyze_eof(path: str):
  with open(path, "rb") as f:
    data = f.read()

  eof_index = data.rfind(JPEG_EOF)

  if eof_index == -1:
    return {
      "suspicious": True,
      "reason": "EOF marker not found"
    }

  extra = data[eof_index + 2:]

  return {
    "suspicious": len(extra) > 0,
    "extra_bytes": len(extra)
  }