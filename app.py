import streamlit as st
import easyocr
from PIL import Image
import pandas as pd
import re

st.set_page_config(page_title="OCR Libramientos", layout="centered")
st.title("📄 OCR de Libramientos a Excel")

reader = easyocr.Reader(['es'], gpu=False)

def limpiar_importe(texto):
    texto = texto.replace("RD$", "").replace(",", "")
    try:
        return float(texto)
    except:
        return ""

def extraer_datos(texto):
    datos = {
        "Número de Libramiento": "",
        "Estructura Programática": "",
        "Institución": "",
        "Importe": "",
        "Cuenta Objeto": ""
    }

    for i, linea in enumerate(texto):
        if "Libramiento" in linea:
            datos["Número de Libramiento"] = texto[i+1] if i+1 < len(texto) else ""

        if "Estructura" in linea:
            datos["Estructura Programática"] = texto[i+1] if i+1 < len(texto) else ""

        if "Institución" in linea:
            datos["Institución"] = texto[i+1] if i+1 < len(texto) else ""

        if "Importe" in linea:
            datos["Importe"] = limpiar_importe(texto[i+1]) if i+1 < len(texto) else ""

    return datos

imagenes = st.file_uploader(
    "📤 Sube una o varias imágenes",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if imagenes:
    resultados = []

    for img in imagenes:
        imagen = Image.open(img)
        texto = reader.readtext(imagen, detail=0)
        datos = extraer_datos(texto)
        resultados.append(datos)

    df = pd.DataFrame(resultados)

    st.success("✅ Datos extraídos correctamente")
    st.dataframe(df)

    st.download_button(
        label="⬇️ Descargar Excel",
        data=df.to_excel(index=False),
        file_name="libramientos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
