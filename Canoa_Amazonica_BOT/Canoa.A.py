import pandas as pd
import streamlit as st
from fuzzywuzzy import fuzz, process

# Inicializar claves en session_state
def init_session_state():
    session_defaults = {
        "order_placed": False,
        "current_order": []
    }
    for key, default in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

# Formatear menú para visualización en tabla
def format_menu(menu):
    table = "| **Plato** | **Descripción** | **Precio** |\n"
    table += "|-----------|-----------------|-------------|\n"
    for idx, row in menu.iterrows():
        table += f"| {row['Plato']} | {row['Descripción']} | S/{row['Precio']:.2f} |\n"
    return table

# Definir postres manualmente
postres_data = {
    "Plato": ["Dulce de Cocona", "Mazamorra de Chonta", "Pastel de Plátano", "Gelatina de Frutas Amazónicas", "Anmitsu", 
              "Trufas de Cacao Amazónico", "Galletas de Suri", "Flan de Camu Camu", "Galletas de Castaña", "Pudín de Yuca"],
    "Descripción": ["Cocona caramelizada con un toque de limón y especias amazónicas", 
                    "Postre cremoso a base de chonta (palmito) con canela y clavo", 
                    "Pastel suave de plátano maduro con nueces y cobertura de chocolate", 
                    "Gelatina fresca hecha con una mezcla de frutas típicas de la Amazonía", 
                    "Postre japonés de gelatina de frutas y pasta dulce", 
                    "Trufas de chocolate oscuro con cacao nativo y un toque de sal marina", 
                    "Galletas crujientes elaboradas con harina de yuca y trozos de suri", 
                    "Flan cremoso elaborado con jugo de camu camu, con un sabor único", 
                    "Galletas crujientes hechas con harina de castaña, ideales para acompañar café", 
                    "Pudín cremoso de yuca con canela y nuez moscada, servido frío"],
    "Precio": [12.5, 12, 8.5, 9.5, 19.5, 16, 13.5, 14, 10, 12]
}

postre = pd.DataFrame(postres_data)

# Configuración de la página
st.set_page_config(page_title="La Canoa Amazónica", page_icon=":canoe:")
init_session_state()

# Menú lateral
menu_opciones = ["Pedidos", "Ofertas", "Reclamos"]
choice = st.sidebar.selectbox("Menú", menu_opciones)

# Añadir botón de reinicio en la barra lateral
if st.sidebar.button("Reiniciar pedido"):
    st.session_state["current_order"] = []
    st.success("Pedido reiniciado.")

if choice == "Pedidos":
    st.markdown("<h2>¡Bienvenidos a La Canoa Amazónica!</h2>", unsafe_allow_html=True)

    # Preguntar si desean postre
    añadir_postre = st.radio("¿Deseas añadir un postre?", ("Sí", "No"))
    
    if añadir_postre == "Sí":
        st.markdown("### Postres")
        st.markdown(format_menu(postre), unsafe_allow_html=True)
        postre_pedido = st.text_input("¿Qué postre deseas pedir?")
        
        if postre_pedido:
            postre_resultados = process.extractOne(postre_pedido, postre["Plato"], scorer=fuzz.token_sort_ratio)
            if postre_resultados[1] > 80:
                postre_seleccionado = postre_resultados[0]
                cantidad_postre = st.number_input(f"¿Cuántos {postre_seleccionado} deseas?", min_value=1, step=1)
                
                if st.button("Añadir postre al pedido"):
                    st.session_state["current_order"].append((postre_seleccionado, cantidad_postre))
                    st.success(f"{cantidad_postre} {postre_seleccionado} añadido(s) al pedido.")
