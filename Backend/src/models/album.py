from datetime import datetime
from enum import Enum

class ALBUM_STATES(Enum):
  PENDIENTE = 'Pendiente'
  APROBADO = 'Aprobado'
  DENEGADO = 'Negado'


class Album:
  id: str
  name: str
  date_created: datetime

  images: list[str]  # image ids

  state: ALBUM_STATES

  def __init__(self, id: str, name: str, date_created: datetime, state: ALBUM_STATES) -> None:
    self.id = id
    self.name = name
    self.date_created = date_created
    self.images = []
    self.state = state

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "date_created": self.date_created.isoformat(),
      "state": self.state,
      "images": self.images,
    }
