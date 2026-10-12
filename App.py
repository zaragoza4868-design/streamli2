
import streamlit as st
from firebase_admin import firestore

st.title("Prueba de lectura de películas")

try:
    db = firestore.client()

    st.write("Consultando colección Movies...")

    documentos = list(
        db.collection("Movies").limit(5).stream(timeout=20)
    )

    st.success(f"Lectura correcta: {len(documentos)} documentos encontrados.")

    if documentos:
        peliculas = []

        for documento in documentos:
            pelicula = documento.to_dict()
            pelicula["id"] = documento.id
            peliculas.append(pelicula)

        st.dataframe(peliculas)
    else:
        st.warning(
            "La consulta funcionó, pero no se encontraron documentos."
        )

except Exception as e:
    st.error(f"{type(e).__name__}: {e}")
    st.exception(e)
