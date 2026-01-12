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

# 2. Estilo CSS para el área gris y botones
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
    code {
        color: #202124 !important;
    }
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
        df = pd.read_excel(uploaded_file, dtype=str).fillna("") 
        st.success("✅ Archivo cargado")
        
        st.write("### ⚙️ Configuración")
        
        # --- LÓGICA DE DETECCIÓN AUTOMÁTICA ---
        def buscar_columna(lista_columnas, palabras_clave):
            for i, col in enumerate(lista_columnas):
                if any(palabra.lower() in str(col).lower() for palabra in palabras_clave):
                    return i
            return 0

        # Intentamos pre-seleccionar automáticamente buscando coincidencias
        idx_estructura = buscar_columna(df.columns, ["estructura", "programatica", "codigo"])
        idx_libramiento = buscar_columna(df.columns, ["libramiento", "numero", "sufijo"])
        
        # Selectores con detección automática mediante el parámetro 'index'
        col_larga = st.selectbox("Estructura Programatica", df.columns, index=idx_estructura)
        col_sufijo = st.selectbox("Numero de Libramiento", df.columns, index=idx_libramiento)
        
        if idx_estructura != 0 or idx_libramiento != 0:
            st.toast("Columnas detectadas automáticamente", icon="🔍")
        
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
                    val1 = str(fila[col_larga]).strip().split('.')[0] 
                    val2 = str(fila[col_sufijo]).strip().split('.')[0]
                    
                    if not val1 or val1.lower() == 'nan': return ""
                    
                    val1 = val1.zfill(12) 
                    parte_a = val1[:6] 
                    parte_b = val1[8:] 
                    
                    bloque1 = parte_a[:4]
                    bloque2 = parte_a[4:6]
                    bloque3 = parte_b
                    
                    return f"{bloque1}.{bloque2}.{bloque3}.{val2}"

                resultados = df.apply(transformar_seguro, axis=1)
                consolidado_texto = ";".join(resultados[resultados != ""].astype(str))

                st.markdown("""
                    <div style="background-color: #f0fff4; border: 1px solid #c6f6d5; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                        <span style="color: #2f855a; font-size: 50px;">✔️</span>
                        <h2 style="color: #2f855a; margin-top: 10px; margin-bottom: 0;">Proceso Exitoso</h2>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("<p style='font-size: 18px; font-weight: 500; color: #333; margin-bottom: 5px;'>Copia y pega este código directamente en SIGEF:</p>", unsafe_allow_html=True)
                
                st.code(consolidado_texto, language=None)
                
                # Preparar Excel para descarga
                df_export = df.copy()
                col_res = [""] * len(df_export)
                col_res[0] = consolidado_texto
                df_export.insert(0, 'RESULTADO_UNIFICADO', col_res)

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_export.to_excel(writer, index=False)
                
                st.download_button(
                    label="📥 DESCARGAR EXCEL CONSOLIDADO",
                    data=output.getvalue(),
                    file_name="Resultado_SIGEF.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
st.caption("DRCC DATA UNIFY - Herramienta diseñada para agilizar el proceso de firma en SIGEF")
