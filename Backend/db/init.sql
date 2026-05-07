-- PostgreSQL syntax

CREATE DATABASE SecureFrameGallery;

-- States
CREATE TYPE IMAGE_STATES AS ENUM(
    'Limpio',
    'Sospechoso',
    'Positivo'
);

CREATE TYPE ALBUM_STATES AS ENUM(
    'Pendiente',
    'Aprobado',
    'Negado'
);

CREATE TYPE USER_ROLES AS ENUM(
    'Administrator',
    'Guest'
);

-- Tables
CREATE TABLE USERS (
    user_id VARCHAR(36) PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    user_last_name VARCHAR(100) NOT NULL,
    user_email VARCHAR(150) NOT NULL UNIQUE,
    user_role USER_ROLES NOT NULL DEFAULT 'Guest'
);

CREATE TABLE ALBUMS (
    album_id VARCHAR(36) PRIMARY KEY,
    album_name VARCHAR(150) NOT NULL,
    album_date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    album_state ALBUM_STATES NOT NULL DEFAULT 'Pendiente'
);

CREATE TABLE IMAGES (
    image_id VARCHAR(36) PRIMARY KEY,
    image_name VARCHAR(255) NOT NULL,
    image_date_uploaded TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    image_size BIGINT NOT NULL,
    image_path TEXT NOT NULL,
    image_mimetype VARCHAR(100) NOT NULL,
    image_state IMAGE_STATES NOT NULL DEFAULT 'Limpio'
);

CREATE TABLE ALBUM_IMAGES (
    album_id VARCHAR(36) NOT NULL,
    image_id VARCHAR(36) NOT NULL,

    PRIMARY KEY (album_id, image_id),

    FOREIGN KEY (album_id) REFERENCES ALBUMS(album_id) ON DELETE CASCADE,
    FOREIGN KEY (image_id) REFERENCES IMAGES(image_id) ON DELETE CASCADE
);