-- Migration v2: run this if ya tienes la base de datos inicializada con init.sql original
-- Safe to run multiple times (IF NOT EXISTS / IF EXISTS guards)

ALTER TABLE USERS
  ALTER COLUMN user_password TYPE VARCHAR(255);

ALTER TABLE ALBUMS
  ADD COLUMN IF NOT EXISTS album_description TEXT NOT NULL DEFAULT '',
  ADD COLUMN IF NOT EXISTS album_is_public BOOLEAN NOT NULL DEFAULT TRUE;

ALTER TABLE IMAGES
  ADD COLUMN IF NOT EXISTS image_analysis JSONB;
