from datetime import datetime
from enum import Enum

class ALBUM_STATES(Enum):
  PENDIENTE = 'Pendiente'
  APROBADO = 'Aprobado'
  DENEGADO = 'Negado'


class Album:
  id: str
  name: str
  description: str
  is_public: bool
  date_created: datetime
  images: list[str]
  state: ALBUM_STATES

  def __init__(self, id: str, name: str, date_created: datetime, state: ALBUM_STATES, description: str = "", is_public: bool = True) -> None:
    self.id = id
    self.name = name
    self.description = description
    self.is_public = is_public
    self.date_created = date_created
    self.images = []
    self.state = state

  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "description": self.description,
      "is_public": self.is_public,
      "date_created": self.date_created.isoformat(),
      "state": self.state.value,
      "images": self.images,
    }
