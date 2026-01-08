import streamlit as st
import pandas as pd
import io
import os

# ---------------- CONFIGURACIÓN GENERAL ----------------
st.set_page_config(
    page_title="DRCC DATA UNIFY",
    page_icon="🎮",
    layout="wide"
)

# ---------------- ESTILOS VISUALES (BRAWL STYLE) ----------------
st.markdown("""
<style>
/* Fondo general */
.main {
    background: linear-gradient(135deg, #f0f4ff, #ffffff);
}

/* Títulos */
.main-title {
    font-size: 48px;
    font-weight: 900;
    color: #1E3A8A;
    margin-bottom: 0;
}
.sub-title {
    font-size: 22px;
    font-weight: 600;
    color: #334155;
}
.credits {
    font-size: 16px;
    color: #64748B;
}

/* Tarjetas */
.card {
    background: white;
    border-radius: 16px;
    padding: 25px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* Botones estilo juego */
.stButton > button {
    width: 100%;
    height: 3.2em;
    border-radius: 12px;
    font-size: 18px;
    font-weight: 800;
    background: linear-gradient(180deg, #2563EB, #1E3A8A);
    color: white;
    border: none;
    transition: 0.2s;
}
.stButton > button:hover {
    transform: scale(1.03);
    background: linear-gradient(180deg, #1D4ED8, #1E40AF);
}

/* Pantalla bienvenida */
.welcome {
    text-align: center;
    padding: 80px 20px;
}
.welcome h1 {
    font-size: 56px;
    font-weight: 900;
    color: #1E3A8A;
}
.welcome p {
    font-size: 22px;
    color: #475569;
}
</style>
""", unsafe_allow_html=True)

# ---------------- CONTROL DE ENTRADA ----------------
if "entrar" not in st.session_state:
    st.session_state.entrar = False

# ---------------- PANTALLA DE BIENVENIDA ----------------
if not st.session_state.entrar:
    st.markdown("""
    <div class="welcome">
        <h1>DRCC DATA UNIFY</h1>
        <p>Plataforma inteligente para unificación de estructuras SIGEF</p>
        <br>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 ENTRAR AL SISTEMA"):
        st.session_state.entrar = True
        st.rerun()

    st.stop()

# ---------------- ENCABEZADO PRINCIPAL ----------------
col_text, col_logo = st.columns([3,1])

with col_text:
    st.markdown('<p class="main-title">DRCC DATA UNIFY</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Creado por Juan Brito</p>', unsafe_allow_html=True)
    st.markdown('<p class="credits">Idea de Chabellys Encarnacion · Optimización SIGEF</p>', unsafe_allow_html=True)

if os.path.exists("logo.png"):
    with col_logo:
        st.image("logo.png", width=160)

st.divider()

# ---------------- CUERPO PRINCIPAL ----------------
col1, col2 = st.columns([1,2], gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📂 Cargar Datos")
    uploaded_file = st.file_uploader("Subir archivo Excel (.xlsx)", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file, dtype=str).fillna("")
        st.success("Archivo cargado correctamente")

        st.subheader("⚙️ Configuración")
        col_larga = st.selectbox("Estructura Programática", df.columns)
        col_sufijo = st.selectbox("Número de Libramiento", df.columns)

        btn_procesar = st.button("⚡ UNIFICAR PARA SIGEF")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if not uploaded_file:
        st.warning("Esperando archivo para procesar...")
    else:
        st.subheader("🔍 Vista Previa")
        st.dataframe(df.head(10), use_container_width=True)

        if btn_procesar:
            try:
                def transformar_seguro(fila):
                    val1 = str(fila[col_larga]).strip().split('.')[0]
                    val2 = str(fila[col_sufijo]).strip().split('.')[0]
                    if not val1 or val1.lower() == 'nan':
                        return ""
                    val1 = val1.zfill(12)
                    parte_a = val1[:6]
                    parte_b = val1[8:]
                    return f"{parte_a[:4]}.{parte_a[4:6]}.{parte_b}.{val2}"

                resultados = df.apply(transformar_seguro, axis=1)
                consolidado_texto = ";".join(resultados[resultados != ""])

                st.success("✔️ Proceso completado con éxito")
                st.code(consolidado_texto)

                df_export = df.copy()
                df_export.insert(0, "RESULTADO_UNIFICADO", [""] * len(df_export))
                df_export.iloc[0,0] = consolidado_texto

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df_export.to_excel(writer, index=False)

                st.download_button(
                    "📥 DESCARGAR EXCEL CONSOLIDADO",
                    data=output.getvalue(),
                    file_name="Resultado_SIGEF.xlsx"
                )
                st.balloons()

            except Exception as e:
                st.error(e)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.caption("DRCC DATA UNIFY · Plataforma Ejecutiva de Productividad SIGEF")
