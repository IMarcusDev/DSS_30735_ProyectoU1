from datetime import datetime

STATES = [
  'Pendiente',
  'Aprobado',
  'Negado',
]

class Album:
  id: str
  name: str
  date_created: datetime

  images: list[str]  # image ids

  state: str

  def __init__(self) -> None:
    pass
