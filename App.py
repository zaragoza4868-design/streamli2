import streamlit as st
import requests
from firebase_admin import credentials
import firebase_admin

st.title("Diagnóstico de conexión")

try:
    datos = dict(st.secrets["firebase"])

    cred = credentials.Certificate(datos)

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    proyecto = datos["project_id"]

    st.write("Proyecto:", proyecto)
    st.write("Comprobando acceso a la API de Firestore...")

    url = (
        "https://firestore.googleapis.com/v1/"
        f"projects/{proyecto}/databases/(default)/documents/Movies"
    )

    token = cred.get_credential()
    from google.auth.transport.requests import Request
    token.refresh(Request())

    respuesta = requests.get(
        url,
        headers={"Authorization": f"Bearer {token.token}"},
        timeout=15,
    )

    st.write("Código HTTP:", respuesta.status_code)

    if respuesta.status_code == 200:
        st.success("La API respondió correctamente.")
        st.json(respuesta.json())
    else:
        st.error("La API respondió con un error.")
        st.code(respuesta.text[:1500])

except Exception as e:
    st.error(f"{type(e).__name__}: {e}")
