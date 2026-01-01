import streamlit as st
import pandas as pd
import io
import os

# 1. Configuración de la pestaña del navegador
st.set_page_config(
    page_title="DRCC DATA UNIFY",
    page_icon="📊",
    layout="wide"
)

# Estilo CSS para personalización profesional
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
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
col_text, col_logo = st.columns([3, 1])
with col_text:
    st.markdown('<p class="main-title">DRCC DATA UNIFY</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Creado por Juan Brito</p>', unsafe_allow_html=True)
    st.markdown('<p class="credits">Auditor de Ordenes de Pago</p>', unsafe_allow_html=True)

with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=150)

st.divider()

# --- CUERPO ---
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.info("### 📂 Cargar Datos")
    uploaded_file = st.file_uploader("Subir archivo Excel (.xlsx)", type=["xlsx"])
    
    if uploaded_file:
        # Cargamos como texto y eliminamos espacios
        df = pd.read_excel(uploaded_file, dtype=str).fillna("") 
        st.success("✅ Archivo cargado")
        
        st.write("### ⚙️ Configuración")
        col_larga = st.selectbox("Columna Código Largo", df.columns)
        col_sufijo = st.selectbox("Columna Sufijo", df.columns)
        
        btn_procesar = st.button("UNIFICAR DATOS")

with col2:
    if not uploaded_file:
        st.warning("Esperando archivo para procesar...")
    
    if uploaded_file and btn_procesar:
        try:
            def transformar_seguro(fila):
                # Limpieza profunda de datos
                val1 = str(fila[col_larga]).strip().split('.')[0] # Quita decimales .0 si existen
                val2 = str(fila[col_sufijo]).strip().split('.')[0]
                
                if not val1 or val1.lower() == 'nan': return ""

                # Aseguramos que el código largo tenga al menos 10 dígitos (rellenando con ceros a la izquierda)
                # Esto es vital para que las posiciones siempre coincidan
                val1 = val1.zfill(12) 

                # 1. Borrar posiciones 7 y 8 (índices 6 y 7)
                # Ejemplo: 501001[01]2942 -> 501001 + 2942
                parte_a = val1[:6]
                parte_b = val1[8:]
                
                # 2. Construir con puntos EXACTOS
                # Estructura: XXXX . XX . XXXX . SUFIJO
                bloque1 = parte_a[:4]
                bloque2 = parte_a[4:6]
                bloque3 = parte_b
                
                return f"{bloque1}.{bloque2}.{bloque3}.{val2}"

            # Procesar
            resultados = df.apply(transformar_seguro, axis=1)
            consolidado_texto = ";".join(resultados[resultados != ""].astype(str))

            # Insertar en Columna C
            columna_final = [""] * len(df)
            columna_final[0] = consolidado_texto
            
            if 'Consolidado_Final' in df.columns:
                df = df.drop(columns=['Consolidado_Final'])
            df.insert(2, 'Consolidado_Final', columna_vacia if 'columna_vacia' in locals() else columna_final)

            st.balloons()
            st.write("### ✅ Resultado SIGEF") 
            st.dataframe(df.head(10), width='stretch')

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='SIGEF')
            
            st.download_button(
                label="📥 DESCARGAR EXCEL PROCESADO",
                data=output.getvalue(),
                file_name="DRCC_Resultado_Final.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"Error: {e}")
    elif uploaded_file:
        st.dataframe(df.head(10), width='stretch')

st.divider()
st.caption("DRCC DATA UNIFY - Auditoría de Ordenes de Pago")