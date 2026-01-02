import streamlit as st
import pandas as pd
import io
import os
import streamlit.components.v1 as components

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
    st.markdown('<p class="credits">Ahorra tiempo al firmar órdenes de pago en SIGEF</p>', unsafe_allow_html=True)

with col_logo:
    if os.path.exists("logo.png"):
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
    
    if uploaded_file:
        st.write("### 🔍 Vista Previa de Origen")
        st.dataframe(df.head(10), width='stretch')
        
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

                # Preparar el archivo Excel para descarga
                df_export = df.copy()
                columna_vacia = [""] * len(df_export)
                columna_vacia[0] = consolidado_texto
                if 'Consolidado_Final' in df_export.columns:
                    df_export = df_export.drop(columns=['Consolidado_Final'])
                df_export.insert(2, 'Consolidado_Final', columna_vacia)

                # --- INTERFAZ DE RESULTADO ---
                st.success("### ✅ Proceso Exitoso") 
                st.balloons()
                
                st.write("Copia este código directamente en SIGEF:")
                st.text_area(label="Código Unificado", value=consolidado_texto, height=150, label_visibility="collapsed")
                
                # BOTÓN DE COPIAR (Usando JavaScript)
                # Este componente crea un botón que interactúa con el portapapeles del sistema
                copy_button_html = f"""
                <button onclick="copyToClipboard()" style="
                    width: 100%;
                    background-color: #28a745;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-weight: bold;
                    font-family: sans-serif;
                    margin-bottom: 10px;">
                    📋 COPIAR AL PORTAPAPELES
                </button>

                <script>
                function copyToClipboard() {{
                    const text = `{consolidado_texto}`;
                    navigator.clipboard.writeText(text).then(function() {{
                        alert('✅ ¡Copiado con éxito! Ahora puedes pegarlo en SIGEF.');
                    }}, function(err) {{
                        console.error('Error al copiar: ', err);
                    }});
                }}
                </script>
                """
                components.html(copy_button_html, height=70)
                
                # Botón de descarga de Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_export.to_excel(writer, index=False, sheet_name='SIGEF')
                
                st.download_button(
                    label="📥 DESCARGAR EXCEL CONSOLIDADO",
                    data=output.getvalue(),
                    file_name="SIGEF_Data_Unified.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
st.caption("DRCC DATA UNIFY - Herramienta diseñada para agilizar el proceso de firma en SIGEF")
