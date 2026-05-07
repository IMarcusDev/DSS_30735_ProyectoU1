import piexif

def insert_test_comment(image_path: str, comment: str = "Este es un comentario de prueba"):
  exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}
  exif_dict["0th"][piexif.ImageIFD.Make] = b"TestCamera"
  exif_dict["0th"][piexif.ImageIFD.Software] = comment.encode("utf-8")

  exif_bytes = piexif.dump(exif_dict)
  piexif.insert(exif_bytes, image_path)

insert_test_comment("test.jpeg", "Comentario de Prueba")
