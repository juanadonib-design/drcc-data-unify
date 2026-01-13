import streamlit as st
import pandas as pd
import io
import os
from datetime import datetime, timedelta

# ================= CONFIGURACIÓN =================
st.set_page_config(
    page_title="DRCC DATA UNIFY",
    page_icon="📊",
    layout="wide"
)

# ================= ESTILOS =================
st.markdown("""
<style>
.main { background-color: #0f172a; color: white; }
.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    background: linear-gradient(135deg,#2563eb,#1e40af);
    color: white;
    font-weight: bold;
}
.card {
    background-color:#020617;
    padding:20px;
    border-radius:15px;
    box-shadow:0 0 20px rgba(37,99,235,.3)
}
code { color:#e5e7eb !important }
</style>
""", unsafe_allow_html=True)

# ================= SESIÓN =================
if "historial_manual" not in st.session_state:
    st.session_state.historial_manual = []

# ================= FUNCIONES =================
def unificar_manual(estructura, libramiento):
    estructura = estructura.zfill(12)
    parte_a = estructura[:6]
    parte_b = estructura[8:]
    return f"{parte_a[:4]}.{parte_a[4:6]}.{parte_b}.{libramiento}"

def limpiar_historial():
    ahora = datetime.now()
    st.session_state.historial_manual = [
        h for h in st.session_state.historial_manual
        if ahora - h["fecha"] < timedelta(hours=24)
    ][-10:]

# ================= HEADER =================
st.markdown("<h1>DRCC DATA UNIFY</h1>", unsafe_allow_html=True)
st.caption("Creado por Juan Brito · Idea de Chabellys Encarnación")
st.divider()

# ================= MODO =================
modo = st.radio(
    "Selecciona el modo de trabajo",
    ["Modo múltiple (Excel)", "Modo manual (uno por uno)"],
    horizontal=True
)

# ================= MANUAL =================
if modo == "Modo manual (uno por uno)":

    st.markdown("## ✳️ Unificación Manual")
    col1, col2 = st.columns(2)

    with col1:
        estructura = st.text_input(
            "Estructura Programática (12 dígitos)",
            max_chars=12
        )

    with col2:
        libramiento = st.text_input(
            "Número de Libramiento",
            max_chars=5
        )

    btn_unificar = st.button("UNIFICAR")

    if btn_unificar and estructura and libramiento:
        resultado = unificar_manual(estructura, libramiento)

        st.session_state.historial_manual.append({
            "estructura": estructura,
            "libramiento": libramiento,
            "resultado": resultado,
            "fecha": datetime.now()
        })

        limpiar_historial()

        st.success("Unificación guardada")

    # ===== HISTORIAL =====
    st.markdown("### 🕒 Historial (últimas 10)")

    for i, h in enumerate(st.session_state.historial_manual):
        c1, c2, c3 = st.columns([6, 3, 1])
        with c1:
            st.write(h["resultado"])
        with c2:
            st.caption(h["fecha"].strftime("%d/%m %H:%M"))
        with c3:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.historial_manual.pop(i)
                st.rerun()

    # ===== UNIFICADO TOTAL =====
    if st.session_state.historial_manual:
        st.markdown("### 🔗 Resultado Unificado del Historial")
        st.code(";".join(h["resultado"] for h in st.session_state.historial_manual))

# ================= EXCEL =================
else:
    st.markdown("## 📂 Unificación por Excel")

    uploaded_file = st.file_uploader(
        "Subir archivo Excel (.xlsx)",
        type=["xlsx"]
    )

    if uploaded_file:
        df = pd.read_excel(uploaded_file, dtype=str).fillna("")
        st.success("Archivo cargado")

        col_larga = st.selectbox("Estructura Programática", df.columns)
        col_sufijo = st.selectbox("Número de Libramiento", df.columns)

        if st.button("UNIFICAR PARA SIGEF"):
            def transformar(fila):
                v1 = str(fila[col_larga]).split('.')[0].zfill(12)
                v2 = str(fila[col_sufijo]).split('.')[0]
                return unificar_manual(v1, v2)

            resultados = df.apply(transformar, axis=1)
            texto = ";".join(resultados)

            st.code(texto)

            df.insert(0, "RESULTADO_UNIFICADO", resultados)

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False)

            st.download_button(
                "📥 DESCARGAR EXCEL",
                data=output.getvalue(),
                file_name="Resultado_SIGEF.xlsx"
            )

# ================= FOOTER =================
st.divider()
st.caption("DRCC DATA UNIFY · Herramienta institucional para SIGEF")
