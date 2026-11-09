import streamlit as st
import docx
import os

st.set_page_config(page_title="Largas Estancias", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #fdfbf7;
        color: #2c3e50;
    }
    h1 {
        color: #1a5276 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📄 Documento: Largas Estancias")

ARCHIVO_LOCAL = "documento_actual.docx"

# Barra lateral protegida con clave (solo tú la usas)
with st.sidebar:
    st.subheader("🔒 Panel de Administración")
    clave = st.text_input("Contraseña de administrador:", type="password")

    if clave == "admin123":
        st.success("Acceso autorizado")
        archivo_nuevo = st.file_uploader("Actualizar archivo Word (.docx)", type=["docx"])

        if archivo_nuevo is not None:
            with open(ARCHIVO_LOCAL, "wb") as f:
                f.write(archivo_nuevo.getbuffer())
            st.success("¡Documento actualizado!")
            st.rerun()
    elif clave:
        st.error("Contraseña incorrecta")

# Vista pública para tus compañeros
if os.path.exists(ARCHIVO_LOCAL):
    doc = docx.Document(ARCHIVO_LOCAL)
    st.divider()

    for parrafo in doc.paragraphs:
        texto = parrafo.text.strip()
        if texto:
            if parrafo.style.name.startswith("Heading"):
                st.subheader(texto)
            else:
                st.write(texto)

    st.divider()
    with open(ARCHIVO_LOCAL, "rb") as f:
        st.download_button(
            label="📥 Descargar documento original (.docx)",
            data=f,
            file_name="Largas_Estancias.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
else:
    st.info("Aún no se ha cargado ningún documento. Entra a la barra lateral con tu clave para subirlo.")
