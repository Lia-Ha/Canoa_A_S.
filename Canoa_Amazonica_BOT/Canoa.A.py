import pandas as pd
import streamlit as st
from datetime import datetime
from fuzzywuzzy import fuzz, process
import re

# Inicializar claves en session_state
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

# Configuración inicial de la página
st.set_page_config(page_title="La Canoa Amazónica!", page_icon=":canoe:")

# Menú lateral
menu_opciones = ["La Canoa Amazónica", "Ofertas", "Pedidos", "Reclamos"]
choice = st.sidebar.selectbox("Menú", menu_opciones)

# Estilo para la imagen de fondo
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Canoa_Amazonica_BOT/assets/images/_Barco.a.jpeg%20(5).jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: white;
    }
    .overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 1;
    }
    </style>
    <div class="overlay"></div>
    """,
    unsafe_allow_html=True
)

# Función para cargar datos desde CSV
def load(file_path):
    return pd.read_csv(file_path)

# Función para formatear el menú en una tabla
def format_menu(menu):
    if menu.empty:
        return "No hay platos disponibles."
    table = "| **Plato** | **Descripción** | **Precio** |\n"
    table += "|-----------|-----------------|-------------|\n"
    for idx, row in menu.iterrows():
        table += f"| {row['Plato']} | {row['Descripción']} | S/{row['Precio']:.2f} |\n"
    return table

# Cargar los archivos CSV de la carta, distritos, bebidas y postres
menu = load("carta.csv")
distritos = load("distritos.csv")
bebidas = load("Bebidas.csv")
postres = load("Postres.csv")

# Mostrar las opciones de menú
if choice == "La Canoa Amazónica":
    st.markdown("<h2 style='color: white;'>¡Bienvenidos a La Canoa Amazónica!</h2>", unsafe_allow_html=True)
    
    # Mostrar carta completa
    st.markdown("### Carta de Platos")
    st.markdown(format_menu(menu), unsafe_allow_html=True)
    
    st.markdown("### Bebidas")
    st.markdown(format_menu(bebidas), unsafe_allow_html=True)
    
    st.markdown("### Postres")
    st.markdown(format_menu(postres), unsafe_allow_html=True)

elif choice == "Ofertas":
    st.markdown("### Promociones del día:")
    st.markdown("**3 juanes por S/70 + chicha morada gratis**")
    
elif choice == "Pedidos":
    st.markdown("### Realiza tu pedido aquí:")
    
    # Aquí puedes agregar la funcionalidad de chat y pedidos.
    
elif choice == "Reclamos":
    st.markdown("<h2 style='color: white;'>Deja tu reclamo aquí:</h2>", unsafe_allow_html=True)
    complaint = st.text_area("Escribe tu reclamo...")
    if st.button("Enviar Reclamo"):
        if complaint:
            st.success("Tu reclamo ha sido enviado.")
        else:
            st.error("Por favor, escribe tu reclamo antes de enviarlo.")
