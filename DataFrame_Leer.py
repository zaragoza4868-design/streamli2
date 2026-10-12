import streamlit as st
import pandas as pd
import requests

from google.oauth2 import service_account
from google.auth.transport.requests import Request


def cargar_peliculas():
    datos = dict(st.secrets["firebase"])

    # Crear credenciales y obtener un token de Google
    cred = service_account.Credentials.from_service_account_info(
        datos,
        scopes=[
            "https://www.googleapis.com/auth/datastore"
        ],
    )
    cred.refresh(Request())

    proyecto = datos["project_id"]

    url = (
        "https://firestore.googleapis.com/v1/"
        f"projects/{proyecto}/databases/(default)/documents/Movies"
    )

    registros = []
    siguiente_pagina = None

    while True:
        parametros = {"pageSize": 100}
        if siguiente_pagina:
            parametros["pageToken"] = siguiente_pagina

        respuesta = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {cred.token}"
            },
            params=parametros,
            timeout=30,
        )

        respuesta.raise_for_status()
        resultado = respuesta.json()

        for documento in resultado.get("documents", []):
            pelicula = {
                "id": documento["name"].split("/")[-1]
            }

            for campo, valor in documento.get("fields", {}).items():
                pelicula[campo] = convertir_valor(valor)

            registros.append(pelicula)

        siguiente_pagina = resultado.get("nextPageToken")
        if not siguiente_pagina:
            break

    return pd.DataFrame(registros)


def convertir_valor(valor):
    """Convierte valores de Firestore REST a valores de Python."""
    if "stringValue" in valor:
        return valor["stringValue"]
    if "integerValue" in valor:
        return int(valor["integerValue"])
    if "doubleValue" in valor:
        return float(valor["doubleValue"])
    if "booleanValue" in valor:
        return valor["booleanValue"]
    if "nullValue" in valor:
        return None
    if "timestampValue" in valor:
        return valor["timestampValue"]
    if "arrayValue" in valor:
        return [
            convertir_valor(v)
            for v in valor["arrayValue"].get("values", [])
        ]
    if "mapValue" in valor:
        return {
            k: convertir_valor(v)
            for k, v in valor["mapValue"].get("fields", {}).items()
        }
    if "referenceValue" in valor:
        return valor["referenceValue"]
    if "geoPointValue" in valor:
        return valor["geoPointValue"]

    return None
Este código obtiene las películas directamente de la API REST, convierte los campos de Firestore a valores de Python y recupera todas las páginas de resultados.

Paso 2. Comprueba tu App.py
Puedes hacer una prueba rápida con:

python
import streamlit as st
from DataFrame_Leer import cargar_peliculas

st.title("Catálogo de películas")

try:
    df = cargar_peliculas()

    if df.empty:
        st.warning("No se encontraron películas.")
    else:
        st.success(f"Películas cargadas: {len(df)}")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Error al cargar películas: {e}")
    
