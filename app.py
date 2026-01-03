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
    .sub-title { color: #333; font-size: 20px; font-weight: 600; margin-top: 5px; margin-bottom: 2px;}
    .idea-text { color: #555; font-size: 16px; font-weight: 700; margin-bottom: 8px;}
    .credits { color: #666; font-style: italic; font-size: 16px; margin-top: 0px;}
    
    /* Diseño del cuadro de bienvenida */
    .welcome-box {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        border-left: 8px solid #1E3A8A;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
col_text, col_logo = st.columns([3, 1])
with col_text:
    st.markdown('<p class="main-title">DRCC DATA UNIFY</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Creado por Juan Brito</p>', unsafe_allow_html=True)
    st.markdown('<p class="idea-text"><b>Idea: Chabellys Encarnacion</b></p>', unsafe_allow_html=True)
    st.markdown('<p class="credits">Ahorra tiempo al unificar estructuras programáticas y libramientos en SIGEF</p>', unsafe_allow_html=True)

if os.path.exists("logo.png"):
    with col_logo:
        st.image("logo.png", width=180)

st.divider()

# --- VENTANA DE BIENVENIDA ---
# Esta sección solo se muestra si no se ha subido ningún archivo
uploaded_file = st.sidebar.file_uploader("Subir archivo Excel (.xlsx)", type=["xlsx"])

if not uploaded_file:
    st.markdown("""
        <div class="welcome-box">
            <h2 style="color: #1E3A8A; margin-top: 0;">👋 ¡Bienvenido al Unificador de Datos!</h2>
            <p style="font-size: 18px; color: #444;">Esta herramienta ha sido diseñada para facilitar el trabajo de los <b>32 auditores</b> del departamento.</p>
            <hr>
            <p style="font-size: 16px;"><b>Instrucciones rápidas:</b></p>
            <ol>
                <li>Carga tu archivo Excel en el panel de la izquierda (Sidebar).</li>
                <li>Selecciona las columnas correspondientes a la estructura y el sufijo.</li>
                <li>Haz clic en unificar y copia el resultado para SIGEF.</li>
            </ol>
            <p style="font-style: italic; color: #666;">Los datos procesados son privados y solo tú puedes verlos en tu sesión.</p>
        </div>
    """, unsafe_allow_html=True)

# --- CUERPO PRINCIPAL ---
if uploaded_file:
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.info("### ⚙️ Configuración")
        try:
            df = pd.read_excel(uploaded_file, dtype=str).fillna("") 
            st.success("✅ Archivo cargado correctamente")
            
            col_larga = st.selectbox("Selecciona Columna Código Largo", df.columns)
            col_sufijo = st.selectbox("Selecciona Columna Sufijo", df.columns)
            
            btn_procesar = st.button("UNIFICAR PARA SIGEF")
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

    with col2:
        st.write("### 🔍 Vista Previa de Datos")
        st.dataframe(df.head(10), use_container_width=True)
        
        if btn_procesar:
            try:
                def transformar_seguro(fila):
                    val1 = str(fila[col_larga]).strip().split('.')[0].zfill(12)
                    val2 = str(fila[col_sufijo]).strip().split('.')[0]
                    if not val1 or val1 == '000000000000': return ""
                    
                    # Formato XXXX.XX.XXXX
                    p1, p2, p3 = val1[:4], val1[4:6], val1[8:]
                    return f"{p1}.{p2}.{p3}.{val2}"

                resultados = df.apply(transformar_seguro, axis=1)
                consolidado_texto = ";".join(resultados[resultados != ""].astype(str))

                # Mensaje de Éxito
                st.markdown("""
                    <div style="background-color: #f0fff4; border: 1px solid #c6f6d5; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                        <span style="color: #2f855a; font-size: 50px;">✔️</span>
                        <h2 style="color: #2f855a; margin-top: 10px; margin-bottom: 0;">Proceso Exitoso</h2>
                    </div>
                """, unsafe_allow_html=True)

                # Instrucción y Copiado
                col_inst, col_btn = st.columns([3, 1])
                with col_inst:
                    st.markdown("<p style='font-size: 18px; font-weight: 500; color: #333; margin-top: 10px;'>Copia y pega este código directamente en SIGEF:</p>", unsafe_allow_html=True)
                with col_btn:
                    if st.button("📋 Copiar Todo"):
                        st.write(f'<script>navigator.clipboard.writeText("{consolidado_texto}")</script>', unsafe_allow_html=True)
                        st.toast("Copiado al portapapeles", icon="✅")

                st.code(consolidado_texto, language=None)
                st.balloons()
            except Exception as e:
                st.error(f"Error en la unificación: {e}")

st.divider()
st.caption("DRCC DATA UNIFY - Herramienta diseñada para agilizar el proceso de firma en SIGEF")
