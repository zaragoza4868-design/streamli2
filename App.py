import streamlit as st
from DataFrame_Leer import cargar_peliculas

st.title("Catálogo de películas")

try:
    df = cargar_peliculas()

    if df.empty:
        st.warning("No se encontraron películas.")
    else:
        st.success(f"Películas cargadas: {len(df)}")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Error al cargar películas: {e}")
