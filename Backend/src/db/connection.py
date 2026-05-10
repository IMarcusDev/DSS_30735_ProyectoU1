from dotenv import load_dotenv
load_dotenv()

import psycopg2
import os
from contextlib import contextmanager

DB_CONFIG = {
  "host": os.getenv("DB_HOST"),
  "port": os.getenv("DB_PORT"),
  "dbname": os.getenv("DB_NAME"),
  "user": os.getenv("DB_USER"),
  "password": os.getenv("DB_PASSWORD", ""),
}

@contextmanager
def get_connection():
  conn = psycopg2.connect(**DB_CONFIG)
  try:
    yield conn
  except Exception:
    conn.rollback()
    raise
  finally:
    conn.close()