import streamlit as st
import pandas as pd
import io
import os

# CONFIG
st.set_page_config(
    page_title="DRCC DATA UNIFY",
    page_icon="📊",
    layout="wide"
)

# ESTILO CORPORATIVO (FiscalFacil-like)
st.markdown("""
<style>
body { background-color: #f4f6f9; }

.hero {
    background: linear-gradient(135deg, #1E3A8A, #312E81);
    padding: 40px;
    border-radius: 15px;
    color: white;
    margin-bottom: 30px;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.stButton>button {
    width: 100%;
    height: 3em;
    border-radius: 8px;
    background-color: #1E3A8A;
    color: white;
    font-weight: bold;
}

h1, h2, h3 { color: #1E3A8A; }
</style>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero">
    <h1>DRCC DATA UNIFY</h1>
    <h3>Unificación inteligente de datos SIGEF</h3>
    <p><b>Creado por Juan Brito</b> · Idea de Chabellys Encarnación</p>
    <p>Ahorra tiempo al unificar estructuras programáticas y libramientos</p>
</div>
""", unsafe_allow_html=True)

# CUERPO
col1, col2 = st.columns([1, 2], gap="large")

# CARD IZQUIERDA
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📂 Cargar datos")
    uploaded_file = st.file_uploader("Archivo Excel (.xlsx)", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file, dtype=str).fillna("")
        st.success("Archivo cargado")

        col_larga = st.selectbox("Código largo", df.columns)
        col_sufijo = st.selectbox("Sufijo", df.columns)
        btn_procesar = st.button("UNIFICAR PARA SIGEF")
    st.markdown("</div>", unsafe_allow_html=True)

# CARD DERECHA
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if not uploaded_file:
        st.warning("Esperando archivo...")
    else:
        st.subheader("Vista previa")
        st.dataframe(df.head(10), use_container_width=True)

        if btn_procesar:
            def transformar_seguro(fila):
                val1 = str(fila[col_larga]).split('.')[0].zfill(12)
                val2 = str(fila[col_sufijo]).split('.')[0]
                if not val1.strip(): return ""
                return f"{val1[:4]}.{val1[4:6]}.{val1[8:]}.{val2}"

            resultados = df.apply(transformar_seguro, axis=1)
            texto = ";".join(resultados[resultados != ""])

            st.success("Proceso exitoso")
            st.code(texto)

            output = io.BytesIO()
            df_export = df.copy()
            df_export.insert(0, "RESULTADO_UNIFICADO", [texto] + [""]*(len(df)-1))
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df_export.to_excel(writer, index=False)

            st.download_button(
                "📥 Descargar Excel",
                data=output.getvalue(),
                file_name="Resultado_SIGEF.xlsx"
            )
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("DRCC DATA UNIFY · Plataforma de unificación de datos SIGEF")
