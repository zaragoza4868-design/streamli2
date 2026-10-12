import os
import firebase_admin
import pandas as pd
import streamlit as st

from firebase_admin import credentials, firestore


@st.cache_resource
def obtener_db():
    ruta = os.path.join(os.path.dirname(__file__), "keys.json")

    if not os.path.exists(ruta):
        raise FileNotFoundError(
            f"No existe el archivo de credenciales: {ruta}"
        )

    if not firebase_admin._apps:
        cred = credentials.Certificate(ruta)
        firebase_admin.initialize_app(cred)

    return firestore.client()


def cargar_peliculas():
    db = obtener_db()

    documentos = db.collection("Movies").stream(timeout=30)

    registros = []

    for documento in documentos:
        pelicula = documento.to_dict()
        pelicula["id"] = documento.id
        registros.append(pelicula)

    return pd.DataFrame(registros)
