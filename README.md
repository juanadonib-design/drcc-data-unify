# drcc-data-unify

# DRCC DATA UNIFY 📊

**Herramienta de automatización para la gestión de firmas masivas en SIGEF.**

---

## 📖 Descripción

**DRCC DATA UNIFY** es una aplicación diseñada para eliminar el trabajo manual repetitivo en la preparación de datos de auditoría. Su función principal es procesar los archivos de Excel exportados de **SUGEP** y convertir automáticamente los datos en códigos formateados y listos para **SIGEF**.

Esta herramienta permite a los auditores realizar **firmas múltiples (por lotes)**, unificando la *Estructura Programática* y el *Número de Libramiento* en una sola cadena de búsqueda, sin necesidad de limpiar columnas manualmente ni insertar puntos de formato uno por uno.

---

## ⚠️ El Problema

El proyecto nació de una necesidad crítica durante la temporada alta: **agilizar las firmas para descongestionar el flujo de trabajo**.

El proceso manual presentaba tres obstáculos principales:
1.  **Necesidad de Firmas Múltiples:** Se requiera dejar atrás la firma "uno a uno" para ahorrar tiempo, pero preparar los datos para hacerlo en masa era muy lento.
2.  **Gestión de Vistas en SUGEP:** El auditor debía perder tiempo configurando manualmente la vista previa para desactivar columnas innecesarias (montos, beneficiarios, estados) antes de cada exportación.
3.  **Formato Manual y Errores:** Excel (con su función `CONCAT`) no aplicaba automáticamente los puntos requeridos en la Estructura Programática (ej. `01.00.0003.1234`), obligando a hacerlo a mano y aumentando el riesgo de errores.

---

## ✅ La Solución

**DRCC DATA UNIFY** resuelve estos problemas mediante la automatización con Python:

* **🕵️‍♂️ Detección Inteligente:** Lee el archivo "crudo" de SUGEP e identifica automáticamente las columnas de *Estructura* y *Libramiento*, ignorando el resto de la información.
* **🛠️ Formateo Automático:** Inserta los puntos en las posiciones correctas y valida que la estructura tenga los 12 dígitos requeridos.
* **🚀 Búsqueda Masiva:** Genera una cadena de texto unificada que permite buscar y firmar múltiples expedientes en una sola acción, mitigando la lentitud de carga del sistema SIGEF.

---

## 🌟 Beneficios Clave

* **Agilización del Flujo:** Transforma horas de trabajo manual en un proceso de segundos.
* **Cero Errores:** Elimina los "dedazos" o errores humanos al digitar números complejos.
* **Sin Fórmulas Complejas:** El usuario no necesita saber usar fórmulas de Excel; solo carga el archivo y copia el resultado.
* **Limpieza Automática:** El sistema filtra solo las columnas necesarias, sin importar cuánta "basura" traiga el reporte original.

---

## 🛠️ Tecnologías Utilizadas

El proyecto está construido con un stack tecnológico moderno y eficiente:

* **Python:** Lógica de procesamiento y backend.
* **Streamlit:** Interfaz web interactiva y fácil de usar.
* **Pandas:** Manipulación y limpieza masiva de datos de Excel.
* **Re (Regex):** Validación de patrones numéricos.

---

## 🚀 Instalación y Ejecución Local

Si deseas correr esta aplicación en tu computadora localmente:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/drcc-data-unify.git](https://github.com/tu-usuario/drcc-data-unify.git)
    ```

2.  **Instalar dependencias:**
    Asegúrate de tener Python instalado y ejecuta:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar la aplicación:**
    ```bash
    streamlit run app.py
    ```

---

## ☁️ Despliegue

Esta aplicación está diseñada para desplegarse en **Streamlit Community Cloud**. El despliegue se realiza conectando este repositorio de GitHub con Streamlit, el cual lee el archivo `requirements.txt` para instalar el entorno y ejecutar `app.py` automáticamente.

---


* **Desarrollado por:** Juan Brito
* **Inal:** Chabellys Encarnacion
