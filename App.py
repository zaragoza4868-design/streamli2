import streamlit as st
import requests
from firebase_admin import credentials

st.title("Diagnóstico OAuth de Google")

try:
    datos = dict(st.secrets["firebase"])
    cred = credentials.Certificate(datos)
    google_cred = cred.get_credential()

    st.write("Endpoint:", google_cred._token_uri)
    st.write("Solicitando autenticación...")

    from google.auth.transport.requests import Request

    class DiagnosticoRequest(Request):
        def __call__(self, url, method="GET", body=None,
                     headers=None, timeout=None, **kwargs):
            response = super().__call__(
                url, method=method, body=body,
                headers=headers, timeout=timeout, **kwargs
            )

            if "oauth2.googleapis.com/token" in url:
                st.write("HTTP status:", response.status)
                st.write(
                    "Content-Type:",
                    response.headers.get("content-type", "no disponible")
                )

                # No mostrar tokens ni respuestas completas.
                st.write(
                    "Tipo de respuesta:",
                    type(response.data).__name__
                )

                try:
                    import json
                    contenido = json.loads(response.data.decode("utf-8"))
                    if isinstance(contenido, dict):
                        st.write(
                            "Campos recibidos:",
                            list(contenido.keys())
                        )
                        if "error" in contenido:
                            st.error(
                                f"Error OAuth: {contenido['error']}"
                            )
                            st.write(
                                contenido.get(
                                    "error_description",
                                    "Sin descripción"
                                )
                            )
                    else:
                        st.write(
                            "La respuesta JSON no es un objeto."
                        )
                except Exception:
                    st.write(
                        "La respuesta no contiene JSON válido."
                    )

            return response

    google_cred.refresh(DiagnosticoRequest())
    st.success("Autenticación completada.")

except Exception as e:
    st.error(f"{type(e).__name__}: {e}")
