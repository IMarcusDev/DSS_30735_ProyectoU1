from datetime import datetime

STATES = [
  'Limpio',
  'Sospechoso',
  'Positivo',
]

class Image:
  id: str
  name: str
  date_uploaded: datetime
  size: int  # bytes
  path: str

  # Metadata
  mimetype: str

  state: str
