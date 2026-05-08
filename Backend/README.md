# Backend

## Instalación

### Entorno Virtual

Primeramente, deberá configurarse un entorno virtual para python:

```sh
# Creación de Entorno
python -m venv {nombre_del_entorno}

# Uso del nuevo entorno
source {nombre_del_entorno}/bin/activate  # Dependerá de la consola

```

Una vez con el entorno virtual, deberán descargarse las debidas librerías:

```sh
pip install -r requirements.txt

```

### Base de Datos

La base de datos utilizada es **PostgreSQL**, el [archivo de inicialización](./db/init.sql) está escrito con esa sintaxis.

Es preferible utilizar contenedores para que no hayan problemas.

### Configuración

El archivo de configuración [.env](./example.env) está como ejemplo en este archivo, lo ideal es copiarlo y modificar sus valores de acuerdo a la configuración de la base de datos:

```sh
cp example.env .env

```
