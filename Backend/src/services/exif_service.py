from PIL import Image
import os

def sanitize_image(input_path: str, output_path: str) -> str:
  with Image.open(input_path) as img:
    ext = os.path.splitext(output_path)[1].lower()
    fmt_map = {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG", ".webp": "WEBP"}
    output_format = fmt_map.get(ext, img.format or "PNG")

    clean = img.copy()
    clean.info = {}

    # Convert mode if the target format doesn't support it
    if output_format == "JPEG" and clean.mode not in ("RGB", "L", "CMYK"):
      clean = clean.convert("RGB")

    # Save with metadata suppressed at the encoder level
    save_kwargs = {}
    if output_format == "JPEG":
      save_kwargs["exif"] = b""          # empty EXIF block
    elif output_format == "PNG":
      save_kwargs["pnginfo"] = None      # drop PNG text/metadata chunks

    clean.save(output_path, format=output_format, **save_kwargs)

  return output_path

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def detect_exif(image_path: str) -> dict:
  findings = {
    "exif": {},
    "gps": {},
    "risks": [],
  }

  with Image.open(image_path) as img:
    exif_data = img.getexif()

    if not exif_data:
      return findings

    for tag_id, value in exif_data.items():
      tag_name = TAGS.get(tag_id, tag_id)

      if tag_name == "GPSInfo":
        for gps_tag_id, gps_value in value.items():
          gps_tag_name = GPSTAGS.get(gps_tag_id, gps_tag_id)
          findings["gps"][gps_tag_name] = str(gps_value)
      else:
        findings["exif"][tag_name] = str(value)

  # Evaluación de riesgos
  if findings["gps"]:
    findings["risks"].append("GPS: contiene coordenadas de ubicación")

  sensitive_keys = {
    "Make", "Model", "Software", "Artist", "Copyright",
    "CameraOwnerName", "BodySerialNumber", "LensSerialNumber",
  }
  found_sensitive = sensitive_keys & findings["exif"].keys()
  if found_sensitive:
    findings["risks"].append(
      f"Dispositivo/autor identificable: {', '.join(found_sensitive)}"
    )

  if any("datetime" in k.lower() for k in findings["exif"]):
    findings["risks"].append("Timestamps: revelan fecha y hora de captura")

  return findings
