import streamlit as st
import pandas as pd
import re

# ======================================================
# FUNCIÓN: BLOQUEAR LETRAS (SOLO NÚMEROS)
# ======================================================
def solo_numeros(key):
    valor = st.session_state.get(key, "")
    st.session_state[key] = re.sub(r"\D", "", valor)

# ======================================================
# CONFIGURACIÓN
# ======================================================
st.set_page_config(
    page_title="DRCC DATA UNIFY",
    page_icon="📊",
    layout="wide"
)

# ======================================================
# ESTILOS
# ======================================================
st.markdown("""
<style>
.main-title { color:#1E3A8A; font-size:42px; font-weight:bold; margin-bottom:0; }
.sub-title { color:#333; font-size:20px; font-weight:600; margin-top:5px; }
</style>
""", unsafe_allow_html=True)

# ======================================================
# ENCABEZADO
# ======================================================
st.markdown('<p class="main-title">DRCC DATA UNIFY</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Creado por Juan Brito | Idea: Chabellys Encarnacion</p>', unsafe_allow_html=True)
st.markdown(
    '<p style="color:#555; font-size:16px;">'
    'Ahorra tiempo al unificar estructuras programáticas y libramientos en SIGEF.'
    '</p>',
    unsafe_allow_html=True
)
st.divider()

# ======================================================
# SELECCIÓN DE MODO
# ======================================================
modo = st.radio(
    "🧭 Selecciona el modo de trabajo",
    ["🔁 Modo múltiple (Excel)", "🧩 Modo manual (uno por uno)"],
    horizontal=True
)

st.divider()

# ======================================================
# MODO MÚLTIPLE
# ======================================================
if modo.startswith("🔁"):

    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.info("### 📂 Cargar archivo Excel")
        uploaded_file = st.file_uploader("Subir archivo (.xlsx)", type=["xlsx"])
        df = None

        if uploaded_file:
            try:
                scan_df = pd.read_excel(uploaded_file, header=None, nrows=6).fillna("")
                keywords = ["estructura", "programática", "libramiento", "número"]

                header_row = max(
                    range(len(scan_df)),
                    key=lambda i: sum(
                        any(k in str(c).lower() for k in keywords)
                        for c in scan_df.iloc[i]
                    )
                )

                uploaded_file.seek(0)
                df = pd.read_excel(uploaded_file, header=header_row, dtype=str).fillna("")
                st.success("✅ Archivo cargado correctamente")

                override = st.checkbox(
                    "✏️ El archivo no tiene encabezados / Cambiar columnas manualmente"
                )

            except Exception as e:
                st.error(f"Error al leer el archivo: {e}")

    with col2:
        if df is None:
            st.warning("Esperando archivo para procesar...")
        else:
            try:
                if override:
                    st.info("El archivo no contiene encabezados. Se asignarán automáticamente.")

                    df.columns = [f"Columna_{i+1}" for i in range(len(df.columns))]

                    st.subheader("👀 Vista previa de los datos")
                    st.dataframe(df.head(20), use_container_width=True)

                    columnas = list(df.columns)

                    col_estructura = st.selectbox(
                        "Selecciona la columna de Estructura Programática",
                        columnas
                    )

                    col_libramiento = st.selectbox(
                        "Selecciona la columna de Número de Libramiento",
                        columnas
                    )
                else:
                    def detectar_columna(cols, claves):
                        for col in cols:
                            if any(k in col.lower() for k in claves):
                                return col
                        return None

                    col_estructura = detectar_columna(df.columns, ["estructura", "programática"])
                    col_libramiento = detectar_columna(df.columns, ["libramiento", "número"])

                if not col_estructura or not col_libramiento:
                    st.error("❌ No se pudieron identificar las columnas necesarias.")
                else:
                    def transformar(fila):
                        v1 = str(fila[col_estructura]).split('.')[0].zfill(12)
                        v2 = str(fila[col_libramiento]).split('.')[0]
                        if v1 == "000000000000" or not v2:
                            return ""
                        return f"{v1[:4]}.{v1[4:6]}.{v1[8:]}.{v2}"

                    resultados = df.apply(transformar, axis=1)
                    validos = resultados[resultados != ""]

                    if not validos.empty:
                        resultado_final = ";".join(validos)
                        st.success("✔️ Datos unificados correctamente")
                        st.metric("📊 Registros unificados", len(validos))
                        st.code(resultado_final, language=None)
                    else:
                        st.warning("⚠️ No se encontraron datos válidos.")

            except Exception as e:
                st.error(f"Error en unificación: {e}")

# ======================================================
# MODO MANUAL (AUTOMÁTICO + BLOQUEO DE LETRAS)
# ======================================================
if modo.startswith("🧩"):

    st.subheader("🧩 Unificación manual")
    st.caption("Ideal cuando el volumen de trabajo es bajo")

    col1, col2 = st.columns(2)

    with col1:
        st.text_input(
            "Estructura Programática (12 dígitos)",
            placeholder="Ej: 010203040506",
            key="estructura",
            on_change=solo_numeros,
            args=("estructura",)
        )

    with col2:
        st.text_input(
            "Número de Libramiento (2 o 5 dígitos)",
            placeholder="Ej: 1234 o 12345",
            key="libramiento",
            on_change=solo_numeros,
            args=("libramiento",)
        )

    estructura = st.session_state.get("estructura", "")
    libramiento = st.session_state.get("libramiento", "")

    # 🔄 VALIDACIÓN + UNIFICACIÓN AUTOMÁTICA
    if estructura and libramiento:

        errores = False

        if len(estructura) != 12:
            st.error("❌ La Estructura Programática debe tener exactamente 12 dígitos")
            errores = True

        if not (2 <= len(libramiento) <= 5):
            st.error("❌ El Número de Libramiento debe tener entre 2 y 5 dígitos")
            errores = True

        if not errores:
            resultado = (
                f"{estructura[:4]}."
                f"{estructura[4:6]}."
                f"{estructura[8:]}."
                f"{libramiento}"
            )

            st.success("✔️ Unificación automática exitosa")
            st.code(resultado, language=None)

st.divider()
st.caption("DRCC DATA UNIFY - Herramienta diseñada para agilizar el proceso de firma en SIGEF")



