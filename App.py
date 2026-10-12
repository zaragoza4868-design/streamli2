import streamlit as st
import firebase_admin
from firebase_admin import firestore
from google.api_core import exceptions

st.title("Diagnóstico de lectura Firestore")

try:
    st.write("1. Creando cliente...")
    db = firestore.client()

    st.write("2. Consultando colección Movies...")
    consulta = db.collection("Movies").limit(1)

    documentos = list(consulta.stream(timeout=15))

    st.success(f"Firestore respondió. Documentos encontrados: {len(documentos)}")

    for documento in documentos:
        st.write("ID:", documento.id)
        st.json(documento.to_dict())

except exceptions.PermissionDenied as e:
    st.error("La cuenta de servicio no tiene permiso para leer Firestore.")
    st.code(str(e))

except exceptions.DeadlineExceeded as e:
    st.error("Firestore no respondió dentro de los 15 segundos.")
    st.code(str(e))

except Exception as e:
    st.error(f"{type(e).__name__}: {e}")
    st.exception(e)
