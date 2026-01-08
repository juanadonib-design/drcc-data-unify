import streamlit as st
import pandas as pd
import io
import os

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="DRCC DATA UNIFY",
    page_icon="🎮",
    layout="wide"
)

# ---------------- CSS QUE STREAMLIT SÍ RESPETA ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #e0e7ff, #ffffff);
}
h1, h2, h3 {
    color: #1E3A8A;
}
.big-button button {
    height: 70px;
    font-size: 26px !important;
    font-weight: 900;
    border-radius: 18px;
    background: linear-gradient(180deg, #3B82F6, #1E40AF);
}
.panel {
    background: white;
    padding: 35px;
    border-radius: 22px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.12);
}
</style>
""", unsafe_allow_html=True)

# ---------------- ESTADO ----------------
if "page" not in st.session_state:
    st.session_state.page = "welcome"

# ---------------- PANTALLA BIENVENIDA ----------------
if st.session_state.page == "welcome":
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div style="text-align:center">
            <h1 style="font-size:60px;font-weight:900;">DRCC DATA UNIFY</h1>
            <p style="font-size:22px;color:#475569;">
                Plataforma ejecutiva para unificación SIGEF
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="big-button">', unsafe_allow_html=True)
        if st.button("🚀 ENTRAR AL SISTEMA"):
            st.session_state.page = "app"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

# ---------------- APP PRINCIPAL ----------------
st.markdown("<br>", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1,6,1])

with col_center:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    # HEADER
    h1, h2 = st.columns([4,1])
    with h1:
        st.title("DRCC DATA UNIFY")
        st.caption("Creado por Juan Brito · Idea de Chabellys Encarnacion")
    with h2:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=120)

    st.divider()

    # CONTENIDO
    col1, col2 = st.columns([1,2])

    with col1:
        st.subheader("📂 Cargar Excel")
        uploaded_file = st.file_uploader("Archivo .xlsx", type="xlsx")

        if uploaded_file:
            df = pd.read_excel(uploaded_file, dtype=str).fillna("")
            col_larga = st.selectbox("Estructura Programática", df.columns)
            col_sufijo = st.selectbox("Número de Libramiento", df.columns)
            btn = st.button("⚡ UNIFICAR")

    with col2:
        if uploaded_file:
            st.subheader("Vista previa")
            st.dataframe(df.head(), use_container_width=True)

            if btn:
                def transformar(fila):
                    v1 = str(fila[col_larga]).split('.')[0].zfill(12)
                    v2 = str(fila[col_sufijo]).split('.')[0]
                    return f"{v1[:4]}.{v1[4:6]}.{v1[8:]}.{v2}"

                r = df.apply(transformar, axis=1)
                texto = ";".join(r)

                st.success("Proceso completado")
                st.code(texto)

    st.markdown('</div>', unsafe_allow_html=True)

st.caption("DRCC DATA UNIFY · Diseño tipo producto premium")
