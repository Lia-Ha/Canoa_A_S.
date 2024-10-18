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

# Estilo de la imagen de fondo y superpuesto oscuro
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Canoa_Amazonica_BOT/assets/images/_Barco.a.jpeg (5).jpg");
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
    """, unsafe_allow_html=True)

# Superpuesto oscuro
st.markdown("<div class='overlay'></div>", unsafe_allow_html=True)

# Menú lateral
menu = ["La Canoa Amazónica", "Ofertas", "Pedidos", "Reclamos"]
choice = st.sidebar.selectbox("Menú", menu)

# Mostrar imágenes en la barra lateral
image_urls = {
    "comida": "https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Canoa_Amazonica_BOT/assets/images/La Canooa.jpg",
    "cocina": "https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Canoa_Amazonica_BOT/assets/images/Cosineros.jpg",
    "restaurante": "https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Canoa_Amazonica_BOT/assets/images/Fondo_Restaur.jpg",
    "pulseras": "https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Canoa_Amazonica_BOT/assets/images/Pulceras_Canoa.jpg"
}

st.sidebar.image(image_urls["comida"], caption="Deliciosos Manjares de la Selva", use_column_width=True)
st.sidebar.image(image_urls["cocina"], caption="Expertos dedicados a ofrecer la mejor calidad", use_column_width=True)
st.sidebar.image(image_urls["restaurante"], caption="Nuevas experiencias", use_column_width=True)
st.sidebar.image(image_urls["pulseras"], caption="Pulseras de cortesía", use_column_width=True)

# Función para cargar datos
def load_data(file, delimiter=';', columns=[]):
    try:
        return pd.read_csv(file, delimiter=delimiter)
    except FileNotFoundError:
        st.error(f"Archivo {file} no encontrado.")
        return pd.DataFrame(columns=columns)

# Función para validar distritos
def verify_district(prompt, districts):
    district_list = districts['Distrito'].tolist()
    best_match, similarity = process.extractOne(prompt, district_list)
    return best_match if similarity > 65 else None

# Función para guardar pedido
def save_order_to_csv(order_dict, district, filename="orders.csv"):
    try:
        orders_list = [{'Fecha y Hora': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Distrito': district, 'Plato': dish, 'Cantidad': quantity} for dish, quantity in order_dict.items()]
        df_orders = pd.DataFrame(orders_list)
        df_orders.to_csv(filename, mode='a', header=False, index=False)
    except Exception as e:
        st.error(f"Error al guardar el pedido: {e}")

# Función para extraer pedidos y cantidades usando similitud
def extract_order_and_quantity(prompt, menu):
    if not prompt:
        return {}

    pattern = r"(\d+|uno|dos|tres|cuatro|cinco)?\s*([^\d,]+)"
    orders = re.findall(pattern, prompt.lower())
    order_dict = {}
    menu_items = menu['Plato'].tolist()

    num_text_to_int = {'uno': 1, 'dos': 2, 'tres': 3, 'cuatro': 4, 'cinco': 5}

    for quantity, dish in orders:
        dish_cleaned = dish.strip()
        best_match, similarity = process.extractOne(dish_cleaned, menu_items, scorer=fuzz.token_set_ratio)

        if similarity > 65:
            quantity = num_text_to_int.get(quantity, 1) if not quantity.isdigit() else int(quantity)
            order_dict[best_match] = order_dict.get(best_match, 0) + quantity

    return order_dict

# Función para mostrar el menú
def format_menu(menu):
    if menu.empty:
        return "No hay platos disponibles."
    formatted_menu = [f"**{row['Plato']}**  \n{row['Descripción']}  \n**Precio:** S/{row['Precio']}" for idx, row in menu.iterrows()]
    return "\n\n".join(formatted_menu)

# Cargar el menú y distritos
menu = load_data("carta_amazonica.csv", delimiter=';', columns=["Plato", "Descripción", "Precio"])
districts = load_data("distritos.csv", columns=["Distrito"])

# Mostrar el contenido según la selección del menú
if choice == "La Canoa Amazónica":
    st.markdown("""
    <h2 style='color: white;'>¡Bienvenidos a La Canoa Amazónica! 🌿🍃</h4>   
    <p style='color: white;'>Experiencia gastronómica única...</p>
    """, unsafe_allow_html=True)

elif choice == "Ofertas":
    st.markdown("¡Promo familiar! 3 juanes a 70 soles, más una botella de 2 litros de chicha morada. Tacacho con cecina 2 por 30 soles!")

elif choice == "Pedidos":
    st.markdown("<h2 style='color: white;'>¡Descubre los Sabores de la Selva!</h2>", unsafe_allow_html=True)

    if st.button("Limpiar Conversación", key="clear"):
        init_session_state()

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🍃" if message["role"] == "assistant" else "👤"):
            st.markdown(message["content"])

    user_input = st.chat_input("Escribe aquí...")

    if not st.session_state["order_placed"] and user_input:
        order_dict = extract_order_and_quantity(user_input, menu)
        if not order_dict:
            response = f"😊 ¡Selecciona un plato de la selva! Escribe la cantidad seguida del plato.\n\n{format_menu(menu)}"
        else:
            st.session_state["order_placed"] = True
            st.session_state["current_order"] = order_dict
            response = f"Tu pedido ha sido registrado: {', '.join([f'{qty} x {dish}' for dish, qty in order_dict.items()])}. ¿De qué distrito nos visitas?"

    elif st.session_state["order_placed"] and user_input:
        district = verify_district(user_input, districts)
        if not district:
            response = f"Lo siento, no entregamos en ese distrito. Distritos disponibles: {', '.join(districts['Distrito'].tolist())}."
        else:
            st.session_state["district_selected"] = True
            st.session_state["current_district"] = district
            save_order_to_csv(st.session_state["current_order"], district)
            response = f"Gracias por tu pedido desde **{district}**. ¡Tu pedido ha sido registrado con éxito! 🍽️"

    if user_input:
        with st.chat_message("assistant", avatar="🍃"):
            st.markdown(f"<p style='color: white;'>{response}</p>", unsafe_allow_html=True)

        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": response})

elif choice == "Reclamos":
    st.markdown("<h2 style='color: white;'>Deja tu Reclamo</h2>", unsafe_allow_html=True)
    complaint = st.text_area("Escribe tu reclamo aquí...")

    if st.button("Enviar Reclamo"):
        if complaint:
            st.success("Tu reclamo está en proceso. Recibirás una respuesta pronto.")
        else:
            st.warning("Por favor, ingresa tu reclamo antes de enviar.")

