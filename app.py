import streamlit as st
import pandas as pd

# ======================================================
# CONTROL DE NAVEGACIÓN
# ======================================================
if "pagina" not in st.session_state:
    st.session_state.pagina = "masivo"

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
# CUERPO
# ======================================================
col1, col2 = st.columns([1, 2], gap="large")

# ======================================================
# COLUMNA IZQUIERDA
# ======================================================
with col1:
    st.info("### 📂 Cargar Datos")
    uploaded_file = st.file_uploader("Subir archivo Excel (.xlsx)", type=["xlsx"])
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
            st.success(f"✅ Encabezados detectados (Fila {header_row + 1})")

            override = st.checkbox("✏️ Cambiar columnas manualmente")

        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

    # ==================================================
    # 🔹 MODO MANUAL (DEBAJO DE SUBIR ARCHIVO)
    # ==================================================
    if st.session_state.pagina == "manual":
        st.divider()
        st.subheader("🧩 Unificación manual")
        st.caption("Para baja carga de trabajo")

        estructura = st.text_input(
            "Estructura Programática (12 dígitos)",
            placeholder="Ej: 010203040506"
        )

        libramiento = st.text_input(
            "Número de Libramiento",
            placeholder="Ej: 12345"
        )

        if st.button("UNIFICAR MANUALMENTE"):
            if not estructura or not libramiento:
                st.error("❌ Ambos campos son obligatorios")
            elif not estructura.isdigit() or len(estructura) != 12:
                st.error("❌ La estructura debe tener exactamente 12 dígitos")
            else:
                resultado_manual = (
                    f"{estructura[:4]}."
                    f"{estructura[4:6]}."
                    f"{estructura[8:]}."
                    f"{libramiento}"
                )
                st.success("✔️ Unificación exitosa")
                st.code(resultado_manual, language=None)

        st.button(
            "⬅️ Volver al modo masivo",
            on_click=lambda: st.session_state.update({"pagina": "masivo"})
        )

# ======================================================
# COLUMNA DERECHA – MODO MASIVO
# ======================================================
with col2:
    if df is None:
        st.warning("Esperando archivo para procesar...")
    else:
        try:
            def detectar_columna(cols, claves):
                for col in cols:
                    if any(k in col.lower() for k in claves):
                        return col
                return None

            col_auto_estructura = detectar_columna(df.columns, ["estructura", "programática"])
            col_auto_libramiento = detectar_columna(df.columns, ["libramiento", "número"])

            if override:
                st.write("### 👀 Vista previa del documento")
                st.dataframe(df.head(20), use_container_width=True)

                col_estructura = st.selectbox(
                    "Estructura Programática",
                    df.columns,
                    index=df.columns.get_loc(col_auto_estructura)
                )

                col_libramiento = st.selectbox(
                    "Número de Libramiento",
                    df.columns,
                    index=df.columns.get_loc(col_auto_libramiento)
                )
            else:
                col_estructura = col_auto_estructura
                col_libramiento = col_auto_libramiento

            if col_estructura and col_libramiento:
                def transformar(fila):
                    v1 = str(fila[col_estructura]).split('.')[0].zfill(12)
                    v2 = str(fila[col_libramiento]).split('.')[0]
                    if v1 == "000000000000" or not v2:
                        return ""
                    return f"{v1[:4]}.{v1[4:6]}.{v1[8:]}.{v2}"

                resultados = df.apply(transformar, axis=1)
                validos = resultados[resultados != ""]

                if not validos.empty:
                    st.success("✔️ Datos unificados correctamente")
                    st.metric("📊 Registros unificados", len(validos))
                    st.code(";".join(validos), language=None)

                    st.button(
                        "➡️ Cambiar a unificación manual",
                        on_click=lambda: st.session_state.update({"pagina": "manual"})
                    )
                else:
                    st.warning("⚠️ No se encontraron datos válidos.")

        except Exception as e:
            st.error(f"Error en unificación: {e}")

st.divider()
st.caption("DRCC DATA UNIFY - Herramienta diseñada para agilizar el proceso de firma en SIGEF")
