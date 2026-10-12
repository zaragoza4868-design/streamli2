import streamlit as st
import traceback

st.title("Diagnóstico de Firebase")

st.write("1. App.py está ejecutándose.")

try:
    st.write("2. Importando el módulo...")
    from DataFrame_Leer import obtener_db

    st.write("3. Inicializando el cliente de Firestore...")
    db = obtener_db()

    st.success("3. Cliente de Firestore creado.")

    st.write("4. Consultando la colección Movies...")

    documentos = db.collection("Movies").stream(timeout=15)
    peliculas = list(documentos)

    st.success(f"Consulta completada: {len(peliculas)} documentos.")

    if peliculas:
        datos = []
        for doc in peliculas:
            pelicula = doc.to_dict()
            pelicula["id"] = doc.id
            datos.append(pelicula)

        st.dataframe(datos)
    else:
        st.warning("La colección Movies no contiene documentos.")

except Exception as e:
    st.error(f"Error: {type(e).__name__}: {e}")
    st.code(traceback.format_exc())

