import firebase_admin
import pandas as pd

from firebase_admin import credentials, firestore
from streamlit import session_state

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("keys.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


def cargar_peliculas():
    """
    Lee todos los registros de la colección Movies
    de Firestore y los devuelve en un DataFrame.
    """
    documentos =db.collection("Movies").stream()
    

    registros = []

    for documento in documentos:
        pelicula = documento.to_dict()
        pelicula["id"] = documento.id
        registros.append(pelicula)

    df = pd.DataFrame(registros)

    return df