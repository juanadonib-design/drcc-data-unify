# --- COMPONENTE DE RESULTADO EXITOSO ---
                st.markdown("""
                    <div style="background-color: #f0fff4; border: 1px solid #c6f6d5; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                        <span style="color: #2f855a; font-size: 50px;">✔️</span>
                        <h2 style="color: #2f855a; margin-top: 10px;">Proceso Exitoso</h2>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("<p style='font-size: 18px; font-weight: 500; color: #333;'>Copia y pega este código directamente en SIGEF:</p>", unsafe_allow_html=True)
                
                # Cuadro tipo textarea con fondo gris claro
                st.text_area(
                    label="Contenedor de códigos", 
                    value=consolidado_texto, 
                    height=180, 
                    label_visibility="collapsed"
                )
                
                # Inyección de CSS para que el textarea tenga el fondo gris claro específico
                st.markdown("""
                    <style>
                        textarea {
                            background-color: #f1f3f4 !important;
                            color: #202124 !important;
                            font-family: 'Courier New', Courier, monospace !important;
                            font-size: 15px !important;
                            border: 1px solid #dadce0 !important;
                            border-radius: 8px !important;
                        }
                    </style>
                """, unsafe_allow_html=True)

                # Botón de Descarga estilizado debajo
                st.download_button(
                    label="📥 DESCARGAR EXCEL CONSOLIDADO",
                    data=output.getvalue(),
                    file_name="Resultado_SIGEF.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

st.divider()
st.caption("DRCC DATA UNIFY - Herramienta diseñada para agilizar el proceso de firma en SIGEF")

