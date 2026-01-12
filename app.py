import streamlit as st
import pandas as pd

st.set_page_config(page_title="DRCC DATA UNIFY", layout="centered")

# =========================
# ENCABEZADO
# =========================
st.markdown('<p class="main-title">DRCC DATA UNIFY</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Creado por Juan Brito | Idea: Chabellys Encarnacion</p>', unsafe_allow_html=True)
st.markdown(
    '<p style="color:#555; font-size:16px; margin-top:2px;">'
    'Ahorra tiempo al unificar estructuras programáticas y libramientos en SIGEF.'
    '</p>',
    unsafe_allow_html=True
)
st.divider()

# =========================
# SESSION STATE
# =========================
if "archivo" not in st.session_state:
    st.session_state.archivo = None

if "resultado" not in st.session_state:
    st.session_state.resultado = None

# =========================
# FUNCIONES
# =========================
def validar_datos(df, columnas):
    errores = []
    filas_validas = []

    for idx, row in df.iterrows():
        fila_ok = True
        for col in columnas:
            if col not in df.columns:
                errores.append(f"No se detectó la columna '{col}'")
                return errores, pd.DataFrame()

            valor = row[col]

            if pd.isna(valor) or str(valor).strip() == "":
                errores.append(f"Campo vacío en fila {idx + 1}, columna '{col}'")
                fila_ok = False

            if not str(valor).isdigit():
                errores.append(f"Formato inválido en fila {idx + 1}, columna '{col}'")
                fila_ok = False

            if len(str(valor)) > 10:
                errores.append(f"Longitud incorrecta en fila {idx + 1}, columna '{col}'")
                fila_ok = False

        if fila_ok:
            filas_validas.append(row)

    return errores, pd.DataFrame(filas_validas)

def unificar_datos(df, columnas):
    return df[columnas].astype(str).agg("".join, axis=1)

# =========================
# CARGA DE ARCHIVO
# =========================
archivo = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if archivo:
    st.session_state.archivo = archivo
    df = pd.read_excel(archivo)

    # Columnas esperadas (ajusta si es necesario)
    columnas_esperadas = df.columns.tolist()

    # =========================
    # VALIDACIÓN
    # =========================
    errores, df_valido = validar_datos(df, columnas_esperadas)

    if errores:
        st.subheader("Errores detectados")
        for error in errores:
            st.error(error)
        st.stop()

    # =========================
    # UNIFICACIÓN AUTOMÁTICA
    # =========================
    resultado = unificar_datos(df_valido, columnas_esperadas)
    st.session_state.resultado = resultado

    # =========================
    # INDICADORES VISUALES
    # =========================
    total_filas = len(df)
    filas_validas = len(df_valido)
    filas_descartadas = total_filas - filas_validas

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de filas", total_filas)
    col2.metric("Filas válidas", filas_validas)
    col3.metric("Filas descartadas", filas_descartadas)

    st.success("Datos unificados correctamente")

    # =========================
    # DESCARGA
    # =========================
    st.download_button(
        label="Descargar resultado",
        data="\n".join(resultado),
        file_name="estructura_unificada.txt",
        mime="text/plain"
    )
