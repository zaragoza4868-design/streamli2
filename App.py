import streamlit as st

st.title("Diagnóstico de secretos")

try:
    datos = st.secrets["firebase"]

    st.write("Tipo de datos:", type(datos).__name__)
    st.write("Claves disponibles:", list(datos.keys()))

    st.success("Los secretos se han leído correctamente.")

except Exception as e:
    st.error(f"{type(e).__name__}: {e}")
