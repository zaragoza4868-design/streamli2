import streamlit as st
from firebase_admin import credentials
from google.auth.transport.requests import Request

st.title("Diagnóstico de credenciales Firebase")

try:
    st.write("1. Leyendo secretos...")
    datos = dict(st.secrets["firebase"])

    st.write("2. Creando credencial...")
    cred = credentials.Certificate(datos)

    st.write("3. Solicitando token de Google...")
    google_cred = cred.get_credential()
    google_cred.refresh(Request())

    st.success("4. ¡Autenticación correcta!")
    st.write("La credencial pudo obtener un token.")

except Exception as e:
    st.error(f"{type(e).__name__}: {e}")
    st.exception(e)
