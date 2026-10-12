import streamlit as st
import firebase_admin
import pandas as pd

from firebase_admin import credentials, firestore


@st.cache_resource
def obtener_db():
    if not firebase_admin._apps:
        datos = dict(st.secrets["firebase"])
        cred = credentials.Certificate(datos)
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
    
