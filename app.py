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

# Inicializar el estado de la aplicación (Pantalla de bienvenida)
if 'entrar' not in st.session_state:
    st.session_state.entrar = False

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
    
    /* Diseño de la Bienvenida Completa */
    .welcome-container {
        background-color: #ffffff;
        padding: 60px;
        border-radius: 20px;
        border-top: 10px solid #1E3A8A;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center;
        max-width: 900px;
        margin: 50px auto;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE PANTALLAS ---

if not st.session_state.entrar:
    # --- PANTALLA DE INICIO COMPLETA ---
    st.markdown(f"""
        <div class="welcome-container">
            <h1 style="color: #1E3A8A; font-size: 50px;">DRCC DATA UNIFY</h1>
            <p style="font-size: 22px; color: #444;">Bienvenido al sistema de unificación de datos para el <b>SIGEF</b>.</p>
            <p style="font-size: 18px; color: #666;">Creado por <b>Juan Brito</b> | Idea: <b>Chabellys Encarnacion</b></p>
            <hr style="margin: 30px 0;">
            <div style="text-align: left; background: #f9f9f9; padding: 20px; border-radius: 10px; margin-bottom: 30px;">
                <h3 style="margin-top:0;">Instrucciones para los 32 Auditores:</h3>
                <ul style="font-size: 16px; line-height: 1.6;">
                    <li>Prepara tu archivo Excel con las estructuras y sufijos.</li>
                    <li>Carga el documento y unifica los códigos en segundos.</li>
                    <li>Copia el resultado final y pégalo directamente en la plataforma de firma.</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Botón de entrar centrado
    col_btn_1, col_btn_2, col_btn_3 = st.columns([1, 1, 1])
    with col_btn_2:
        if st.button("ENTRAR AL SISTEMA"):
            st.session_state.entrar = True
            st.rerun()

else:
    # --- PANEL DE TRABAJO (Solo se ve al presionar Entrar) ---
    
    # Botón para volver al inicio en el sidebar
    if st.sidebar.button("⬅️ Cerrar Sesión / Volver"):
        st.session_state.entrar = False
        st.rerun()

    # --- ENCABEZADO ---
    col_text, col_logo = st.columns([3, 1])
    with col_text:
        st.markdown('<p class="main-title">DRCC DATA UNIFY</p>', unsafe_allow_html=True)
        st.markdown('<p class="sub-title">Creado por Juan Brito</p>', unsafe_allow_html=True)
        st.markdown('<p class="idea-text"><b>Idea: Chabellys Encarnacion</b></p>', unsafe_allow_html=True)
        st.markdown('<p class="credits">Panel de Trabajo Activo</p>', unsafe_allow_html=True)

    if os.path.exists("logo.png"):
        with col_logo:
            st.image("logo.png", width=180)

    st.divider()

    # --- CARGA Y PROCESAMIENTO ---
    uploaded_file = st.file_uploader("Subir archivo Excel (.xlsx)", type=["xlsx"])
    
    if uploaded_file:
        col1, col2 = st.columns([1, 2], gap="large")

        with col1:
            st.info("### ⚙️ Configuración")
            try:
                df = pd.read_excel(uploaded_file, dtype=str).fillna("") 
                st.success("✅ Archivo cargado")
                col_larga = st.selectbox("Columna Código Largo", df.columns)
                col_sufijo = st.selectbox("Columna Sufijo", df.columns)
                btn_procesar = st.button("UNIFICAR PARA SIGEF")
            except Exception as e:
                st.error(f"Error: {e}")

        with col2:
            st.write("### 🔍 Vista Previa")
            st.dataframe(df.head(10), use_container_width=True)
            
            if btn_procesar:
                # Lógica de unificación
                def transformar(fila):
                    v1 = str(fila[col_larga]).strip().split('.')[0].zfill(12)
                    v2 = str(fila[col_sufijo]).strip().split('.')[0]
                    if not v1 or v1 == '000000000000': return ""
                    return f"{v1[:4]}.{v1[4:6]}.{v1[8:]}.{v2}"

                resultados = df.apply(transformar, axis=1)
                consolidado_texto = ";".join(resultados[resultados != ""].astype(str))

                st.markdown("""
                    <div style="background-color: #f0fff4; border: 1px solid #c6f6d5; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                        <span style="color: #2f855a; font-size: 50px;">✔️</span>
                        <h2 style="color: #2f855a; margin-top: 10px;">Proceso Exitoso</h2>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("<p style='font-weight: 500;'>Resultado para SIGEF:</p>", unsafe_allow_html=True)
                st.code(consolidado_texto, language=None)
                st.balloons()

    st.divider()
    st.caption("DRCC DATA UNIFY - Herramienta diseñada para agilizar el proceso de firma en SIGEF")
