import streamlit as st
import docx
import os
import io

st.set_page_config(page_title="Largas Estancias Hospitalarias", layout="wide")

# --- PALETA DE COLORES CLÍNICA / HOSPITALARIA ---
st.markdown("""
<style>
    /* Fondo general en azul muy suave y limpio */
    .stApp {
        background-color: #f0f7f9;
        color: #1a3038;
    }
    /* Títulos en azul médico oscuro */
    h1 {
        color: #0b4f6c !important;
        font-weight: 700;
    }
    h2, h3 {
        color: #145da0 !important;
    }
    /* Estilo de la barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #e3eff3;
    }
    /* Contenedores de texto limpios */
    .stMarkdown p {
        font-size: 1.05rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏥 Gestión de Propuestas: Largas Estancias Hospitalarias")
st.caption("Visualizador institucional y seguimiento clínico-administrativo.")

# Galería de imágenes temáticas hospitalarias
col_img1, col_img2 = st.columns(2)
with col_img1:
    st.image(
        "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=900&q=80",
        caption="Centro Hospitalario y Urgencias",
        use_container_width=True
    )
with col_img2:
    st.image(
        "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=900&q=80",
        caption="Atención Médica y Cuidado del Paciente",
        use_container_width=True
    )

st.divider()

ARCHIVO_LOCAL = "documento_actual.docx"

# --- PANEL DE ADMINISTRACIÓN (SOLO PARA TI) ---
with st.sidebar:
    st.subheader("🔒 Panel de Administración")
    clave = st.text_input("Contraseña de administrador:", type="password")
    
    if clave == "admin123":
        st.success("Acceso autorizado")
        archivo_nuevo = st.file_uploader("Actualizar archivo Word (.docx)", type=["docx"])
        
        if archivo_nuevo is not None:
            contenido_bytes = archivo_nuevo.read()
            # Guardar en disco persistente
            with open(ARCHIVO_LOCAL, "wb") as f:
                f.write(contenido_bytes)
            # Guardar en memoria de sesión para renderizar de inmediato
            st.session_state["doc_bytes"] = contenido_bytes
            st.success("¡Documento cargado con éxito!")
    elif clave:
        st.error("Contraseña incorrecta")

# --- VISUALIZACIÓN DEL DOCUMENTO ---
bytes_para_leer = None

if "doc_bytes" in st.session_state:
    bytes_para_leer = io.BytesIO(st.session_state["doc_bytes"])
elif os.path.exists(ARCHIVO_LOCAL):
    with open(ARCHIVO_LOCAL, "rb") as f:
        bytes_para_leer = io.BytesIO(f.read())

if bytes_para_leer is not None:
    try:
        doc = docx.Document(bytes_para_leer)
        st.subheader("📄 Contenido del Documento")
        
        for parrafo in doc.paragraphs:
            texto = parrafo.text.strip()
            if texto:
                if parrafo.style.name.startswith("Heading") or (len(texto) > 0 and texto[0].isdigit() and "." in texto[:3]):
                    st.subheader(texto)
                else:
                    st.write(texto)
                    
        # Tablas del documento si existen
        for tabla in doc.tables:
            filas_datos = []
            for row in tabla.rows:
                filas_datos.append([cell.text.strip() for cell in row.cells])
            if filas_datos:
                st.table(filas_datos)
                
        st.divider()
        bytes_para_leer.seek(0)
        st.download_button(
            label="📥 Descargar documento original (.docx)",
            data=bytes_para_leer,
            file_name="Propuesta_Largas_Estancias.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"Error al leer el documento: {e}")
else:
    st.info("Aún no se ha cargado ningún documento. Usa el panel de la izquierda con tu contraseña para subir la propuesta.")
