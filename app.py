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
    code { color: #202124 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
col_text, col_logo = st.columns([3, 1])
with col_text:
    st.markdown('<p class="main-title">DRCC DATA UNIFY</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Creado por Juan Brito</p>', unsafe_allow_html=True)
    st.markdown('<p class="idea-text"><b>Idea de Chabellys Encarnacion</b></p>', unsafe_allow_html=True)
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
        try:
            # ESCANEO INTELIGENTE DE LAS PRIMERAS 4 FILAS
            # Leemos las primeras 4 filas para ver cuál tiene los encabezados reales
            scan = pd.read_excel(uploaded_file, header=None, nrows=4)
            keywords = ["estructura", "programatica", "libramiento", "numero"]
            
            header_row = 0
            for i in range(len(scan)):
                fila = scan.iloc[i].astype(str).str.lower().tolist()
                # Si encontramos las palabras clave en esta fila, fijamos el encabezado ahí
                if any(any(key in cell for key in keywords) for cell in fila):
                    header_row = i
                    break
            
            # Recargar el archivo usando la fila correcta
            uploaded_file.seek(0)
            df = pd.read_excel(uploaded_file, header=header_row, dtype=str).fillna("")
            
            st.success(f"✅ Encabezado detectado en fila {header_row + 1}")
            
            st.write("### ⚙️ Configuración")
            
            def buscar_col(cols, keys):
                for i, c in enumerate(cols):
                    if any(k.lower() in str(c).lower() for k in keys): return i
                return 0

            # Buscar las columnas específicas que vimos en tu imagen
            idx_e = buscar_col(df.columns, ["estructura", "programatica"])
            idx_l = buscar_col(df.columns, ["libramiento", "numero"])
            
            col_larga = st.selectbox("Estructura Programatica", df.columns, index=idx_e)
            col_sufijo = st.selectbox("Numero de Libramiento", df.columns, index=idx_l)
            
            btn_procesar = st.button("UNIFICAR PARA SIGEF")
            
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

with col2:
    if not uploaded_file:
        st.warning("Esperando archivo para procesar...")
    else:
        st.write("### 🔍 Vista Previa de Datos")
        # Mostramos la tabla limpia
        st.dataframe(df.head(10), use_container_width=True)
        
        if 'btn_procesar' in locals() and btn_procesar:
            try:
                def transformar(fila):
                    v1 = str(fila[col_larga]).strip().split('.')[0].zfill(12)
                    v2 = str(fila[col_sufijo]).strip().split('.')[0]
                    if not v1 or v1 == '000000000000': return ""
                    return f"{v1[:4]}.{v1[4:6]}.{v1[8:]}.{v2}"

                res = df.apply(transformar, axis=1)
                final_txt = ";".join(res[res != ""].astype(str))

                st.markdown("""
                    <div style="background-color: #f0fff4; border: 1px solid #c6f6d5; padding: 20px; border-radius: 10px; text-align: center;">
                        <h2 style="color: #2f855a; margin: 0;">✔️ Proceso Exitoso</h2>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("<p style='margin-top:15px; font-weight:500;'>Copia esto en SIGEF:</p>", unsafe_allow_html=True)
                st.code(final_txt, language=None)
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
st.caption("DRCC DATA UNIFY - Optimizando la auditoría para SIGEF")
