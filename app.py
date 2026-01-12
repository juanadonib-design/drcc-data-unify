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
    code { color: #202124 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown('<p class="main-title">DRCC DATA UNIFY</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Creado por Juan Brito | Idea: Chabellys Encarnacion</p>', unsafe_allow_html=True)
st.divider()

# --- CUERPO ---
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.info("### 📂 Cargar Datos")
    uploaded_file = st.file_uploader("Subir archivo Excel (.xlsx)", type=["xlsx"])
    
    if uploaded_file:
        try:
            # PASO 1: Escanear las primeras 5 filas para encontrar los encabezados reales
            # Leemos sin encabezado para analizar los datos crudos
            scan_df = pd.read_excel(uploaded_file, header=None, nrows=5)
            
            # Palabras clave exactas de tu imagen
            keywords = ["estructura", "programática", "libramiento", "número"]
            
            header_found = 0
            for i in range(len(scan_df)):
                # Convertimos toda la fila a una sola cadena de texto para buscar
                fila_unida = " ".join(scan_df.iloc[i].astype(str).lower())
                if any(k in fila_unida for k in keywords):
                    header_found = i
                    break
            
            # PASO 2: Cargar el Excel desde la fila detectada
            uploaded_file.seek(0)
            df = pd.read_excel(uploaded_file, header=header_found, dtype=str).fillna("")
            
            st.success(f"✅ Encabezados detectados en la fila {header_found + 1}")
            
            st.write("### ⚙️ Configuración")
            
            # Función de búsqueda mejorada para coincidir con tu imagen
            def auto_detect(columns, target_keys):
                for i, col in enumerate(columns):
                    col_str = str(col).lower()
                    if any(k in col_str for k in target_keys):
                        return i
                return 0

            # Detectamos las columnas según el texto de tu imagen
            idx_est = auto_detect(df.columns, ["estructura", "programática"])
            idx_lib = auto_detect(df.columns, ["libramiento", "número"])
            
            col_larga = st.selectbox("Estructura Programática", df.columns, index=idx_est)
            col_sufijo = st.selectbox("Número de Libramiento", df.columns, index=idx_lib)
            
            btn_procesar = st.button("UNIFICAR PARA SIGEF")
            
        except Exception as e:
            st.error(f"Error técnico: {e}")

with col2:
    if not uploaded_file:
        st.warning("Esperando archivo...")
    else:
        st.write("### 🔍 Vista Previa (Datos Limpios)")
        st.dataframe(df.head(10), use_container_width=True)
        
        if 'btn_procesar' in locals() and btn_procesar:
            try:
                # Lógica de unificación manteniendo los ceros a la izquierda
                def transformar(fila):
                    # Limpiar el dato y asegurar 12 dígitos
                    v1 = str(fila[col_larga]).strip().split('.')[0].zfill(12)
                    v2 = str(fila[col_sufijo]).strip().split('.')[0]
                    
                    if v1 == "000000000000" or not v2: return ""
                    
                    # Formato XXXX.XX.XXXX
                    return f"{v1[:4]}.{v1[4:6]}.{v1[8:]}.{v2}"

                resultados = df.apply(transformar, axis=1)
                consolidado = ";".join(resultados[resultados != ""].astype(str))

                st.success("✔️ Proceso Exitoso")
                st.markdown("**Copia esto en SIGEF:**")
                st.code(consolidado, language=None)
                st.balloons()
            except Exception as e:
                st.error(f"Error al procesar: {e}")

st.divider()
st.caption("DRCC DATA UNIFY - Herramienta diseñada para agilizar el proceso de firma en SIGEF")
