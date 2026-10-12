import firebase_admin
import pandas as pd
import streamlit as st

from firebase_admin import credentials, firestore


@st.cache_resource
def obtener_db():
    if not firebase_admin._apps:
        datos = dict(st.secrets["firebase"])
        cred = credentials.Certificate(datos)
        firebase_admin.initialize_app(cred)

    return firestore.client()


def cargar_peliculas():
    """Lee la colección Movies de Firestore y devuelve un DataFrame."""
    try:
        db = obtener_db()
        documentos = db.collection("Movies").stream()

        registros = []

        for documento in documentos:
            pelicula = documento.to_dict()
            pelicula["id"] = documento.id
            registros.append(pelicula)

        return pd.DataFrame(registros)

    except Exception as e:
        st.error(f"Error al cargar películas desde Firebase: {e}")
        return pd.DataFrame()
    df = pd.DataFrame(registros)

    return df
