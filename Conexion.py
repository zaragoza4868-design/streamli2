import os
from turtle import st
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

# Buscar el archivo .env junto a Conexion.py
ruta_env = Path(__file__).resolve().parent / ".env"

print("Ruta del archivo:", ruta_env)
print("¿Existe el archivo?", ruta_env.is_file())

# Cargar las variables
load_dotenv(dotenv_path=ruta_env, override=True)

# No intentar conectar si faltan variables
if not all(os.getenv(k) for k in [
    "DB_HOST", "DB_PORT", "DB_USER",
    "DB_PASSWORD", "DB_NAME"
]):
    raise ValueError(
        "Faltan variables de conexión. Revisa el archivo .env"
    )
def obten_conexion():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME"),
        sslmode="require"
    )

