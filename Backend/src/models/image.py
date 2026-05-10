from datetime import datetime
from enum import Enum

class IMAGE_STATES(Enum):
  LIMPIO = 'Limpio'
  SOSPECHOSO = 'Sospechoso'
  POSITIVO = 'Positivo'


class Image:
  id: str
  name: str
  size: int
  date_uploaded: datetime
  path: str
  mimetype: str
  state: IMAGE_STATES
  analysis: dict | None

  def __init__(self, id: str, name: str, date_uploaded: datetime, path: str, mimetype: str, state: IMAGE_STATES, analysis: dict | None = None, size: int = 0) -> None:
    self.id = id
    self.name = name
    self.size = size
    self.date_uploaded = date_uploaded
    self.path = path
    self.mimetype = mimetype
    self.state = state
    self.analysis = analysis

  def to_dict(self) -> dict:
    return {
      "image_id":            self.id,
      "image_name":          self.name,
      "image_size":          self.size,
      "image_date_uploaded": self.date_uploaded.isoformat(),
      "image_path":          self.path,
      "image_mimetype":      self.mimetype,
      "image_state":         self.state.value,
      "image_analysis":      self.analysis,
    }
