import pandas as pd
import streamlit as st
from google.cloud import firestore
from DataFrame_Leer import cargar_peliculas
from Conexion import obten_conexion


db = firestore.Client.from_service_account_json('keys.json')
dbMovies=db.collection('Movies')
st.title("Diagnóstico de Firebase")

try:
    st.write("Iniciando lectura de películas...")
    df = cargar_peliculas()
    st.success("La función terminó correctamente.")
    st.write("Filas encontradas:", len(df))
    st.dataframe(df)
except Exception as e:
    st.error("Falló la carga de películas")
    st.exception(e)
Así podremos ver el erro


# Dataset base de la aplicación
df_movies = cargar_peliculas()

print("Películas cargadas:", len(df_movies))
print(df_movies)
##.dataframe(df_movies)

def obtener_generos():
    """Devuelve los géneros disponibles."""
    if "genre" not in df_movies.columns:
        return []

    return sorted(
        df_movies["genre"].dropna().unique().tolist()
    )


def filtrar_peliculas(genero):
    """Filtra las películas por género."""
    if "genre" not in df_movies.columns:
        return df_movies.iloc[0:0].copy()

    return df_movies[
        df_movies["genre"].astype(str).str.casefold()
        == genero.casefold()
    ]


# Ejemplo de uso
lista_generos = obtener_generos()
print("Géneros:", lista_generos)


# Configuración del dashboard
st.set_page_config(
    page_title="Dashboard de películas",
    page_icon="🎬",
    layout="wide"
)

# Cargar dataset base desde Firestore
df_movies = cargar_peliculas()

# Encabezado principal
st.header("🎬 Dashboard de películas")
st.write("Consulta y busca filmes de la colección movies.")

# Sidebar
st.sidebar.header("Opciones de visualización")

# Checkbox para visualizar todos los filmes
mostrar_todas = st.sidebar.checkbox(
    "Mostrar todos los filmes",
    value=False
)

# Campo de texto para buscar por título
titulo_busqueda = st.sidebar.text_input(
    "Buscar filme por título",
    placeholder="Escribe el título..."
)

# Botón de búsqueda
buscar = st.sidebar.button(
    "Buscar filmes",
    use_container_width=True
)

# Mostrar todos los filmes
if mostrar_todas:
    st.subheader("Todos los filmes")

    if df_movies.empty:
        st.warning("No hay películas registradas en Firestore.")
    else:
        st.dataframe(
            df_movies,
            use_container_width=True,
            hide_index=True
        )
        st.write(f"Total de filmes: {len(df_movies)}")

# Buscar filmes al pulsar el botón
if buscar:
    if not titulo_busqueda.strip():
        st.sidebar.warning("Escribe un título para buscar.")
    elif df_movies.empty:
        st.warning("No hay películas registradas en Firestore.")
    elif "name" not in df_movies.columns:
        st.error("No se encontró la columna 'nombre' en los datos.")
    else:
        # Coincidencia parcial e insensible a mayúsculas/minúsculas
        resultados = df_movies[
            df_movies["name"].astype("string").str.contains(
                titulo_busqueda.strip(),
                case=False,
                na=False,
                regex=False
            )
        ]

        st.subheader("Resultados de la búsqueda")

        if resultados.empty:
            st.info("No se encontraron filmes con ese título.")
        else:
            st.dataframe(
                resultados,
                use_container_width=True,
                hide_index=True
            )
            st.write(f"Filmes encontrados: {len(resultados)}")


####
def filtrar_por_director(director):
    if "director" not in df_movies.columns:
        return df_movies.iloc[0:0].copy()

    return df_movies[
        df_movies["director"].astype("string").str.strip()
        == director.strip()
    ]


# Opciones de búsqueda en el sidebar
st.sidebar.header("Buscar por director")

# Cargar los directores desde la columna del DataFrame
if "director" in df_movies.columns:
    directores = sorted(
        df_movies["director"]
        .dropna()
        .astype(str)
        .str.strip()
        .loc[lambda s: s != ""]
        .unique()
        .tolist()
    )
else:
    directores = []

# Selectbox para elegir un director
director_seleccionado = st.sidebar.selectbox(
    "Selecciona un director:",
    options=directores,
    index=0 if directores else None,
    placeholder="Selecciona un director"
)

# Botón para ejecutar el filtro
if st.sidebar.button("Filtrar por director", use_container_width=True):
    if director_seleccionado:
        resultado_director = filtrar_por_director(
            director_seleccionado
        )

        st.subheader(
            f"Filmes dirigidos por {director_seleccionado}"
        )

        st.write(
            f"Total de filmes encontrados: {len(resultado_director)}"
        )

        if resultado_director.empty:
            st.info("No se encontraron filmes para este director.")
        else:
            st.dataframe(
                resultado_director,
                use_container_width=True,
                hide_index=True
            )
    else:
        st.warning("No hay directores disponibles para seleccionar.")


        #####
        # Formulario para insertar un nuevo filme
st.sidebar.header("Registrar nuevo filme")

with st.sidebar.form("form_nuevo_filme", clear_on_submit=True):
    nombre = st.text_input("Título del filme")
    genero = st.text_input("Género")
    director = st.text_input("Director")
    compania = st.text_input("Compañía productora")

    guardar = st.form_submit_button(
        "Guardar filme",
        use_container_width=True
    )

    if guardar:
        # Validar campos obligatorios
        if not all([
            nombre.strip(),
            genero.strip(),
            director.strip(),
            compania.strip()
        ]):
            st.sidebar.error("Completa todos los campos.")
        else:
            try:
                nuevo_filme = {
                    "name": nombre.strip(),
                    "genre": genero.strip(),
                    "director": director.strip(),
                    "company": compania.strip()
                }

                # Insertar documento en Firestore
                _, referencia = db.collection("Movies").add(
                    nuevo_filme
                    
                )
                st.session_state["df_movies"] = cargar_peliculas()

                st.sidebar.success(
                    f"Filme registrado correctamente. ID: {referencia.id}"
                    
                )

            except Exception as e:
                st.sidebar.error(
                    f"Error al guardar el filme: {e}"
                )



####Comentarios sidebar
st.sidebar.header("💬 Comentarios de visitantes")

with st.sidebar.form("form_comentarios", clear_on_submit=True):
    correo = st.text_input("Correo electrónico")
    comentario = st.text_area("Escribe tu comentario")

    enviar = st.form_submit_button(
        "Enviar comentario",
        use_container_width=True
    )

    if enviar:
        if not correo.strip() or not comentario.strip():
            st.sidebar.error(
                "El nombre y el comentario son obligatorios."
            )
        else:
            conexion = None
           
            try:
                conexion = obten_conexion()
                
                with conexion.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO people VALUES (%s, %s)
                        """,
                        (
                            correo.strip() or None,
                            comentario.strip()
                        )
                    )

                conexion.commit()
                st.sidebar.success(
                    "¡Gracias! Tu comentario se registró correctamente."
                )

            except Exception as e:
                if conexion:
                    conexion.rollback()

                st.sidebar.error(
                    f"No se pudo guardar el comentario: {e}"
                )

            finally:
                if conexion:
                    conexion.close()
