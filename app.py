import streamlit as st
import pandas as pd
import io
import os

# 1. Configuración de la pestaña
st.set_page_config(
    page_title="DRCC DATA UNIFY",
    page_icon="📊",
    layout="wide"
)

# 2. Estilo CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
    }
    .main-title { color: #1E3A8A; font-size: 42px; font-weight: bold; margin-bottom: 0px; line-height: 1;}
    .sub-title { color: #333; font-size: 20px; font-weight: 600; margin-top: 5px; margin-bottom: 0px;}
    .credits { color: #666; font-style: italic; font-size: 16px; margin-top: 0px;}
    textarea {
        background-color: #f1f3f4 !important;
        color: #202124 !important;
        font-family: 'Courier New', Courier, monospace !important;
        font-size: 15px !important;
        border: 1px solid #dadce0 !important;
        border-radius: 8px !important;
    }
    /* Estilo para el mini botón de copiar */
    .copy-btn-style > div > button {
        height: 2.5em !important;
        background-color: #1E3A8A !important;
        font-size: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
col_text, col_logo = st.columns([3, 1])
with col_text:
    st.markdown('<p class="main-title">DRCC DATA UNIFY</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Creado por Juan Brito</p>', unsafe_allow_html=True)
    st.markdown('<p class="credits">Ahorra tiempo al unificar estructuras programáticas y libramientos en SIGEF</p>', unsafe_allow_html=True)

if os.path.exists("logo.png"):
    with col_logo:
        st.image("logo.png", width=180)

st.divider()

# --- CUERPO ---
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.info("### 📂 Cargar Datos")
    uploaded_file = st.file_uploader("Subir archivo Excel (.xlsx)", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file, dtype=str).fillna("") 
        st.success("✅ Archivo cargado")
        st.write("### ⚙️ Configuración")
        col_larga = st.selectbox("Columna Código Largo", df.columns)
        col_sufijo = st.selectbox("Columna Sufijo", df.columns)
        btn_procesar = st.button("UNIFICAR PARA SIGEF")

with col2:
    if not uploaded_file:
        st.warning("Esperando archivo para procesar...")
    else:
        st.write("### 🔍 Vista Previa de Origen")
        st.dataframe(df.head(10), use_container_width=True)
        
        if btn_procesar:
            try:
                def transformar_seguro(fila):
                    val1 = str(fila[col_larga]).strip().split('.')[0].zfill(12) 
                    val2 = str(fila[col_sufijo]).strip().split('.')[0]
                    if not val1 or val1 == '000000000000': return ""
                    return f"{val1[:4]}.{val1[4:6]}.{val1[8:]}.{val2}"

                resultados = df.apply(transformar_seguro, axis=1)
                consolidado_texto = ";".join(resultados[resultados != ""].astype(str))

               # --- DISEÑO DE RESULTADO CON BOTÓN AL LADO DEL TEXTO ---
st.markdown("""
    <div style="background-color: #f0fff4; border: 1px solid #c6f6d5; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
        <span style="color: #2f855a; font-size: 50px;">✔️</span>
        <h2 style="color: #2f855a; margin-top: 10px; margin-bottom: 0;">Proceso Exitoso</h2>
    </div>
""", unsafe_allow_html=True)

# Creamos dos columnas: una para el texto y otra para el botón
col_instruccion, col_boton_copiar = st.columns([3, 1])

with col_instruccion:
    st.markdown("<p style='font-size: 18px; font-weight: 500; color: #333; margin-top: 10px;'>Copia y pega este código directamente en SIGEF:</p>", unsafe_allow_html=True)

with col_boton_copiar:
    # Usamos un botón de Streamlit que, al presionarlo, muestra un mensaje de éxito
    if st.button("📋 Copiar Todo"):
        st.write(f'<script>navigator.clipboard.writeText("{consolidado_texto}")</script>', unsafe_allow_html=True)
        st.toast("Copiado al portapapeles", icon="✅")

# El cuadro gris con los números debajo
st.code(consolidado_texto, language=None)
                
                # Descarga Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False)
                
                st.download_button(label="📥 DESCARGAR EXCEL CONSOLIDADO", data=output.getvalue(), file_name="Resultado_SIGEF.xlsx")
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
st.caption("DRCC DATA UNIFY - Herramienta diseñada para agilizar el proceso de firma en SIGEF")

