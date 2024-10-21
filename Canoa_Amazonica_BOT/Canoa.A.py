import pandas as pd
import streamlit as st
from fuzzywuzzy import fuzz, process

# Inicializar claves en session_state
def init_session_state():
    session_defaults = {
        "order_placed": False,
        "current_order": [],
        "messages": []
    }
    for key, default in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

# Función para cargar datos desde URL de CSV
def load_from_url(url):
    return pd.read_csv(url)

# Formatear menú para visualización en tabla
def format_menu(menu):
    table = "| **Plato** | **Descripción** | **Precio** |\n"
    table += "|-----------|-----------------|-------------|\n"
    for idx, row in menu.iterrows():
        table += f"| {row['Plato']} | {row['Descripción']} | S/{row['Precio']:.2f} |\n"
    return table

# Cargar los archivos CSV desde GitHub
menu_url = "https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/carta.csv"
postres_url = "https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Postre.csv"
bebidas_url = "https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Bebidas.csv"
distritos_url = "https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/distrito.csv"

menu = load_from_url(menu_url)
postres = load_from_url(postres_url)
bebidas = load_from_url(bebidas_url)
distritos = load_from_url(distritos_url)

# Configuración de la página
st.set_page_config(page_title="La Canoa Amazónica", page_icon=":canoe:")
init_session_state()

# Menú lateral
menu_opciones = ["La Canoa Amazónica", "Ofertas", "Pedidos", "Reclamos"]
choice = st.sidebar.selectbox("Menú", menu_opciones)

if choice == "La Canoa Amazónica":
    st.markdown("<h2 style='color: white;'>¡Bienvenidos a La Canoa Amazónica!</h2>", unsafe_allow_html=True)
    
    # Mostrar carta completa
    st.markdown("### Carta de Platos")
    st.markdown(format_menu(menu), unsafe_allow_html=True)
    
    st.markdown("### Bebidas")
    st.markdown(format_menu(bebidas), unsafe_allow_html=True)
    
    st.markdown("### Postres")
    st.markdown(format_menu(postres), unsafe_allow_html=True)

elif choice == "Pedidos":
    st.markdown("### Realiza tu pedido aquí:")

    # Preguntar por el pedido
    pedido = st.text_input("¿Qué plato deseas pedir?")
    
    if pedido:
        resultados = process.extractOne(pedido, menu["Plato"], scorer=fuzz.token_sort_ratio)
        if resultados[1] > 80:  # Coincidencia alta
            plato_seleccionado = resultados[0]
            cantidad = st.number_input(f"¿Cuántos {plato_seleccionado} deseas?", min_value=1, step=1)
            
            if st.button("Añadir al pedido"):
                st.session_state["current_order"].append((plato_seleccionado, cantidad))
                st.success(f"{cantidad} {plato_seleccionado} añadido(s) al pedido.")
        
        # Consultar si desea añadir más
        if st.session_state["current_order"]:
            if st.checkbox("¿Deseas añadir algún postre o bebida?"):
                seleccion_postre = st.selectbox("Selecciona un postre:", postres["Plato"])
                if st.button("Añadir postre"):
                    st.session_state["current_order"].append((seleccion_postre, 1))
                    st.success(f"{seleccion_postre} añadido al pedido.")
            
    # Mostrar resumen del pedido
    if st.session_state["current_order"]:
        st.markdown("### Resumen de tu pedido:")
        total = 0
        pedido_resumen = "| **Plato** | **Cantidad** | **Precio** |\n"
        pedido_resumen += "|-----------|-------------|-------------|\n"
        for item, cantidad in st.session_state["current_order"]:
            precio = menu.loc[menu['Plato'] == item, 'Precio'].values[0]
            pedido_resumen += f"| {item} | {cantidad} | S/{precio * cantidad:.2f} |\n"
            total += precio * cantidad
        st.markdown(pedido_resumen, unsafe_allow_html=True)
        st.markdown(f"**Total a pagar: S/{total:.2f}**")

elif choice == "Reclamos":
    st.markdown("### Deja tu reclamo aquí:")
    reclamo = st.text_area("Escribe tu reclamo...")
    if st.button("Enviar Reclamo"):
        if reclamo:
            st.success("Tu reclamo ha sido enviado.")
        else:
            st.error("Por favor, escribe tu reclamo antes de enviarlo.")

