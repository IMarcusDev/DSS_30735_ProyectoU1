from PIL import Image
import numpy as np

def analyze_lsb(path: str):
  img = Image.open(path)

  arr = np.array(img)
  lsb = arr & 1
  ratio = np.mean(lsb)

  suspicious = ratio > 0.52 or ratio < 0.48

  return {
    "lsb_ratio": float(ratio),
    "suspicious": suspicious
  }
