from datetime import datetime
from enum import Enum

class IMAGE_STATES(Enum):
  LIMPIO = 'Limpio'
  SOSPECHOSO = 'Sospechoso'
  POSITIVO = 'Positivo'


class Image:
  id: str
  name: str
  date_uploaded: datetime
  path: str
  mimetype: str
  state: IMAGE_STATES
  analysis: dict | None

  def __init__(self, id: str, name: str, date_uploaded: datetime, path: str, mimetype: str, state: IMAGE_STATES, analysis: dict | None = None) -> None:
    self.id = id
    self.name = name
    self.date_uploaded = date_uploaded
    self.path = path
    self.mimetype = mimetype
    self.state = state
    self.analysis = analysis

  def to_dict(self) -> dict:
    return {
      "id": self.id,
      "name": self.name,
      "date_uploaded": self.date_uploaded.isoformat(),
      "path": self.path,
      "mimetype": self.mimetype,
      "state": self.state.value,
      "analysis": self.analysis,
    }
