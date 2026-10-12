import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

st.title("Diagnóstico Firebase")

try:
    st.write("A. Aplicación iniciada")

    st.write("B. Leyendo secretos")
    datos = dict(st.secrets["firebase"])

    st.write("C. Validando credenciales")
    cred = credentials.Certificate(datos)

    st.write("D. Inicializando Firebase")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    st.write("E. Creando cliente Firestore")
    db = firestore.client()

    st.success("F. Cliente creado")

    st.write("G. Probando conexión con Firestore")
    docs = list(db.collection("Movies").limit(1).stream(timeout=15))

    st.success(f"Conexión completada. Documentos de prueba: {len(docs)}")

except Exception as e:
    st.error(f"{type(e).__name__}: {e}")
    st.exception(e)
