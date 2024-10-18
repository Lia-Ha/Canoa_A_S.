import pandas as pd
import streamlit as st
from datetime import datetime
from fuzzywuzzy import fuzz, process
import re

# Inicializar las claves de session_state si no existen
def init_session_state():
    session_defaults = {
        "order_placed": False,
        "district_selected": False,
        "current_district": None,
        "messages": []
    }
    for key, default in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

init_session_state()

# Configuración inicial de la página
st.set_page_config(page_title="La Canoa Amazónica!", page_icon=":canoe:")

# Estilo para la imagen de fondo y el superpuesto oscuro
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Canoa_Amazonica_BOT/image.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: white;  /* Cambiar el color del texto si es necesario */
    }
    
    .overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5); /* Color negro con opacidad del 50% */
        z-index: 1; /* Asegura que el superpuesto esté por encima de la imagen de fondo */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Agregar el div del superpuesto en la parte superior
st.markdown("<div class='overlay'></div>", unsafe_allow_html=True)

# URLs de las imágenes
url_chica_comida = "https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Canoa_Amazonica_BOT/La%20Canoaa.jpg"

# Mostrar imágenes en la barra lateral
st.sidebar.image(url_chica_comida, caption="Deliciosos Manjares de la Selva", use_column_width=True)
