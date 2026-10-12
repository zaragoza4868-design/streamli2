import streamlit as st
from firebase_admin import credentials
from google.auth.transport.requests import Request
import traceback



st.title("Diagnóstico de credenciales")

try:
    datos = dict(st.secrets["firebase"])

    st.write("1. Secretos leídos correctamente")

    # Normalizar los saltos de línea de la clave privada
    if isinstance(datos.get("private_key"), str):
        datos["private_key"] = (
            datos["private_key"].replace("\\n", "\n")
        )

    st.write("2. Creando credencial de Firebase")
    certificado = credentials.Certificate(datos)

    st.write("3. Obteniendo credencial de Google")
    credencial_google = certificado.get_credential()

    st.write("4. Solicitando token")
    credencial_google.refresh(Request())

    st.success("5. Autenticación correcta")

except Exception as e:
    st.error(f"{type(e).__name__}: {e}")
    st.code(traceback.format_exc())

   


