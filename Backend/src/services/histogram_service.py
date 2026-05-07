import cv2
import numpy as np

def analyze_histogram(path: str) -> dict:
  img = cv2.imread(path)

  if img is None:
    raise ValueError("Could not read image")

  hist_b = cv2.calcHist([img], [0], None, [256], [0,256])
  hist_g = cv2.calcHist([img], [1], None, [256], [0,256])
  hist_r = cv2.calcHist([img], [2], None, [256], [0,256])

  variance = np.var(hist_r) + np.var(hist_g) + np.var(hist_b)

  suspicious = variance < 5000

  return {
    "variance": float(variance),
    "suspicious": suspicious
  }