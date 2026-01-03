import streamlit as st
import pandas as pd
import io
import os

# ---------------- CONFIGURACIÓN ----------------
st.set_page_config(
    page_title="DRCC DATA UNIFY",
    page_icon="🎮",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "enter_app" not in st.session_state:
    st.session_state.enter_app = False

# ---------------- ESTILOS GLOBALES ----------------
st.markdown("""
<style>
/* FONDO GENERAL */
body {
    background: radial-gradient(circle at top, #1e3a8a, #020617);
}

/* -------- PANTALLA BIENVENIDA -------- */
.welcome-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 90vh;
}

.welcome-card {
    background: linear-gradient(180deg, #1e40af, #312e81);
    padding: 60px;
    border-radius: 25px;
    box-shadow: 0px 20px 40px rgba(0,0,0,0.5);
    text-align: center;
    max-width: 720px;
    animation: fadeIn 1.2s ease;
}

.welcome-title {
    font-size: 52px;
    font-weight: 900;
    color: #facc15;
}

.welcome-subtitle {
    font-size: 22px;
    color: #e5e7eb;
    margin-bottom: 25px;
}

.welcome-text {
    font-size: 18px;
    color: #d1d5db;
    margin-bottom: 40px;
}

.enter-btn > button {
    background: linear-gradient(180deg, #facc15, #eab308);
    color: #111827;
    font-size: 22px;
    font-weight: 900;
    padding: 18px;
    border-radius: 15px;
    width: 100%;
    border: none;
}

.enter-btn > button:hover {
    transform: scale(1.05);
}

/* -------- APP PRINCIPAL -------- */
.hero {
    background: linear-gradient(135deg, #1E3A8A, #312E81);
    padding: 35px;
    border-radius: 18px;
    color: white;
    margin-bottom: 30px;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.stButton>button {
    width: 100%;
    height: 3em;
    border-radius: 10px;
    background-color: #1E3A8A;
    color: white;
    font-weight: bold;
}

@keyframes fadeIn {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}
</style>
""", unsafe_allow_html=True)

# =================================================
# =============== PANTALLA BIENVENIDA ===============
# =================================================
if not st.session_state.enter_app:

    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-card">
            <div class="welcome-title">DRCC DATA UNIFY</div>
            <div class="welcome-subtitle">Executive Data Intelligence Platform</div>
            <div class="welcome-text">
                Plataforma estratégica para la unificación, estandarización
                y validación de estructuras programáticas y libramientos en SIGEF.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([2,1,2])[1]
    with col:
        if st.button("🚀 ENTRAR", key="enter"):
            st.session_state.enter_app = True
            st.rerun()

# =================================================
# ================== APP PRINCIPAL =================
# =================================================
else:

    # HERO
    st.markdown("""
    <div class="hero">
        <h1>DRCC DATA UNIFY</h1>
        <h3>Unificación inteligente de datos SIGEF</h3>
        <p><b>Creado por Juan Brito</b> · Idea de Chabellys Encarnación</p>
        <p>Optimiza y estandariza estructuras programáticas de forma segura y eficiente.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2], gap="large")

    # -------- CARD IZQUIERDA --------
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📂 Cargar datos")

        uploaded_file = st.file_uploader("Archivo Excel (.xlsx)", type=["xlsx"])

        if uploaded_file:
            df = pd.read_excel(uploaded_file, dtype=str).fillna("")
            st.success("Archivo cargado correctamente")

            col_larga = st.selectbox("Columna Código Largo", df.columns)
            col_sufijo = st.selectbox("Columna Sufijo", df.columns)
            btn_procesar = st.button("UNIFICAR PARA SIGEF")
        else:
            btn_procesar = False

        st.markdown("</div>", unsafe_allow_html=True)

    # -------- CARD DERECHA --------
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        if not uploaded_file:
            st.warning("Esperando archivo para procesar...")
        else:
            st.subheader("🔍 Vista previa")
            st.dataframe(df.head(10), use_container_width=True)

            if btn_procesar:
                try:
                    def transformar_seguro(fila):
                        val1 = str(fila[col_larga]).strip().split('.')[0]
                        val2 = str(fila[col_sufijo]).strip().split('.')[0]

                        if not val1 or val1.lower() == "nan":
                            return ""

                        val1 = val1.zfill(12)
                        return f"{val1[:4]}.{val1[4:6]}.{val1[8:]}.{val2}"

                    resultados = df.apply(transformar_seguro, axis=1)
                    consolidado = ";".join(resultados[resultados != ""])

                    st.success("✔ Proceso exitoso")
                    st.markdown("Copia y pega este código directamente en SIGEF:")
                    st.code(consolidado)

                    # EXPORTAR EXCEL
                    df_export = df.copy()
                    df_export.insert(0, "RESULTADO_UNIFICADO", [consolidado] + [""]*(len(df)-1))

                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                        df_export.to_excel(writer, index=False)

                    st.download_button(
                        "📥 Descargar Excel Consolidado",
                        data=output.getvalue(),
                        file_name="Resultado_SIGEF.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                except Exception as e:
                    st.error(f"Error: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

    st.caption("DRCC DATA UNIFY · Plataforma ejecutiva de unificación SIGEF")
