import sys
import os

file_path = 'test/test.jpeg'

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import src.services.exif_service as exif

print(exif.detect_exif(file_path))
