import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from google.cloud import firestore
db= firestore.Client.from_service_account_json('keys.json')
dbMovies=db.collection('Movies')

st.header("Llenar Datos")
name =st.text_input("Nombre de la pelicula")
genre =st.text_input("Genero de la pelicula")
director =st.text_input("Director de la pelicula")
company =st.text_input("Compañia de la pelicula")

submit_button = st.button("Guardar Datos")

if name and genre and director and company:
    if submit_button:
        data = {
            'name': name,
            'genre': genre,
            'director': director,
            'company': company
        }
        dbMovies.add(data)
        st.success("Datos guardados correctamente")
