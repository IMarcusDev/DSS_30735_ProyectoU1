import sys
import os

import src.services.exif_service as exif
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

file_path = 'test/test.jpeg'

print(exif.detect_exif(file_path))
