import streamlit as st
import pandas as pd

# 1. Configuración
st.set_page_config(
    page_title="DRCC DATA UNIFY",
    page_icon="📊",
    layout="wide"
)

# 2. Estilos
st.markdown("""
<style>
.main-title { color:#1E3A8A; font-size:42px; font-weight:bold; margin-bottom:0; }
.sub-title { color:#333; font-size:20px; font-weight:600; margin-top:5px; }
</style>
""", unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown('<p class="main-title">DRCC DATA UNIFY</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Creado por Juan Brito | Idea: Chabellys Encarnacion</p>', unsafe_allow_html=True)
st.markdown(
    '<p style="color:#555; font-size:16px;">'
    'Ahorra tiempo al unificar estructuras programáticas y libramientos en SIGEF.'
    '</p>',
    unsafe_allow_html=True
)
st.divider()

# --- CUERPO ---
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.info("### 📂 Cargar Datos")
    uploaded_file = st.file_uploader("Subir archivo Excel (.xlsx)", type=["xlsx"])
    df = None

    if uploaded_file:
        try:
            # 🔍 Escaneo inicial
            scan_df = pd.read_excel(uploaded_file, header=None, nrows=6).fillna("")
            keywords = ["estructura", "programática", "libramiento", "número"]

            header_auto = max(
                range(len(scan_df)),
                key=lambda i: sum(
                    any(k in str(c).lower() for k in keywords)
                    for c in scan_df.iloc[i]
                )
            )

            st.success(f"✅ Encabezados detectados automáticamente (Fila {header_auto + 1})")

            # 🛠️ OVERRIDE MANUAL
            override = st.checkbox("✏️ Cambiar encabezado manualmente")

            if override:
                header_manual = st.selectbox(
                    "Selecciona la fila del encabezado",
                    options=list(range(1, 11)),
                    index=header_auto
                )
                header_final = header_manual - 1
            else:
                header_final = header_auto

            # 📥 Cargar archivo definitivo
            uploaded_file.seek(0)
            df = pd.read_excel(uploaded_file, header=header_final, dtype=str).fillna("")

        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

with col2:
    if df is None:
        st.warning("Esperando archivo para procesar...")
    else:
        try:
            # 🔎 Detección automática de columnas
            def detectar_columna(cols, claves):
                for col in cols:
                    if any(k in col.lower() for k in claves):
                        return col
                return None

            col_estructura = detectar_columna(df.columns, ["estructura", "programática"])
            col_libramiento = detectar_columna(df.columns, ["libramiento", "número"])

            if not col_estructura or not col_libramiento:
                st.error("❌ No se pudieron detectar las columnas necesarias.")
            else:
                # ⚙️ Unificación automática
                def transformar(fila):
                    v1 = str(fila[col_estructura]).split('.')[0].zfill(12)
                    v2 = str(fila[col_libramiento]).split('.')[0]
                    if v1 == "000000000000" or not v2:
                        return ""
                    return f"{v1[:4]}.{v1[4:6]}.{v1[8:]}.{v2}"

                resultados = df.apply(transformar, axis=1)
                validos = resultados[resultados != ""]

                if not validos.empty:
                    st.success("✔️ Datos unificados automáticamente")
                    st.metric("📊 Registros unificados", len(validos))
                    st.code(";".join(validos), language=None)
                else:
                    st.warning("⚠️ No se encontraron datos válidos.")

        except Exception as e:
            st.error(f"Error en unificación: {e}")

st.divider()
st.caption("DRCC DATA UNIFY - Herramienta diseñada para agilizar el proceso de firma en SIGEF")
