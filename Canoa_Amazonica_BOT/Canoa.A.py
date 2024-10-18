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

# CSS para la imagen de fondo
st.markdown(
    """
    <style>
    .background {
        background-image: url("https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Canoa_Amazonica_BOT/Capturaaaaaaaaaaaaaaaaaaaaaaaaa.JPG");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        height: 100vh;
        padding: 20px;
        color: white; /* Establecer color de texto blanco para mejorar la visibilidad */
    }
    </style>
    <div class="background">
    """,
    unsafe_allow_html=True
)

# Mostrar imágenes en la barra lateral
url_chica_comida = "https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Canoa_Amazonica_BOT/La%20Canooa.jpg"
st.sidebar.image(url_chica_comida, caption="Deliciosos Manjares de la Selva", use_column_width=True)

# Menú lateral
menu = ["La Canoa Amazónica", "Ofertas", "Pedidos", "Reclamos"]
choice = st.sidebar.selectbox("Menú", menu)

if choice == "La Canoa Amazónica":
    # Mensaje de bienvenida en HTML con estilo
    welcome_message = """
    <h2>¡Bienvenidos a La Canoa Amazónica! 🌿🍃</h2>   
    <p>Si eres amante de la comida exótica y auténtica de nuestra querida selva, aquí te ofrecemos una experiencia gastronómica única que no querrás perderte.
    En La Canoa Amazónica, vendemos una variedad de deliciosos platos de la selva, elaborados con ingredientes frescos y autóctonos que capturan la esencia de la Amazonía. Cada bocado es un viaje sensorial que te transporta a lo más profundo de la selva, donde los sabores vibrantes y las especias exóticas se fusionan para crear una explosión de gusto en tu paladar. Desde suculentas carnes, como el pez amazónico, hasta opciones vegetarianas llenas de nutrientes, tenemos algo para todos los gustos.
    Nuestro compromiso va más allá de ofrecer comida deliciosa; también te invitamos a disfrutar de un ambiente acogedor y familiar en cualquiera de nuestras cuatro sedes en San Martín, San Isidro y Chorrillos. Aquí, recibirás una atención personalizada que te hará sentir como en casa, porque en La Canoa Amazónica, tú eres parte de nuestra familia.
    Además de nuestro conveniente servicio de delivery, te garantizamos que cada visita será memorable. Te invitamos a sumergirte en la cultura y las tradiciones de la selva, donde cada plato cuenta una historia y cada sabor es un homenaje a la riqueza natural de nuestra región.</p>
    
    <p>Recuerda: ¡tú eres parte de la selva, y la selva es parte de ti! Ven a disfrutar de la comida con el verdadero sabor de la Amazonía, y déjate envolver por la magia de nuestros platos. ¡Te esperamos con los brazos abiertos en La Canoa Amazónica! 🌿🍽️</p>  
    """
    
    # Mostrar el mensaje de bienvenida
    st.markdown(welcome_message, unsafe_allow_html=True)

elif choice == "Ofertas":
    # Mensaje de ofertas
    offers_message = """¡Promo familiar! 3 juanes a 70 soles, más una botella de 2 litros de chicha morada.  
    ¡Tacacho con cecina 2 por 30 soles! ¡Super promo!"""
    st.markdown(offers_message)

elif choice == "Pedidos":
    # Mostrar mensaje de bienvenida
    intro = """
    <h2>¡Descubre los Sabores de la Selva en La Canoa Amazónica! 🌿🍃</h2>  
    <p>Llegaste al rincón del sabor, donde la selva te recibe con sus platos más deliciosos.</p>  
    <p>¿Qué se te antoja hoy? ¡Escribe "Carta" para comenzar!</p>
    """
    st.markdown(intro, unsafe_allow_html=True)

    # Función para cargar el menú desde un archivo CSV
    def load_menu(csv_file):
        try:
            return pd.read_csv(csv_file, delimiter=';')
        except FileNotFoundError:
            st.error("Archivo de menú no encontrado.")
            return pd.DataFrame(columns=["Plato", "Descripción", "Precio"])

    # Función para cargar los distritos de reparto desde otro CSV
    def load_districts(csv_file):
        try:
            return pd.read_csv(csv_file)
        except FileNotFoundError:
            st.error("Archivo de distritos no encontrado.")
            return pd.DataFrame(columns=["Distrito"])

    # Función para verificar el distrito con similitud
    def verify_district(prompt, districts):
        district_list = districts['Distrito'].tolist()
        best_match, similarity = process.extractOne(prompt, district_list)
        return best_match if similarity > 65 else None

    # Función para guardar el pedido en un archivo CSV
    def save_order_to_csv(order_dict, district, filename="orders.csv"):
        try:
            orders_list = [
                {'Fecha y Hora': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 'Distrito': district, 'Plato': dish, 'Cantidad': quantity}
                for dish, quantity in order_dict.items()
            ]
            df_orders = pd.DataFrame(orders_list)
            df_orders.to_csv(filename, mode='a', header=False, index=False)
        except Exception as e:
            st.error(f"Error al guardar el pedido: {e}")

    # Función para extraer el pedido y la cantidad usando similitud
    def improved_extract_order_and_quantity(prompt, menu):
        if not prompt:
            return {}

        pattern = r"(\d+|uno|dos|tres|cuatro|cinco)?\s*([^\d,]+)"
        orders = re.findall(pattern, prompt.lower())

        order_dict = {}
        menu_items = menu['Plato'].tolist()

        num_text_to_int = {
            'uno': 1, 'dos': 2, 'tres': 3, 'cuatro': 4, 'cinco': 5
        }

        for quantity, dish in orders:
            dish_cleaned = dish.strip()
            best_match, similarity = process.extractOne(dish_cleaned, menu_items, scorer=fuzz.token_set_ratio)

            if similarity > 65:
                if not quantity:
                    quantity = 1
                elif quantity.isdigit():
                    quantity = int(quantity)
                else:
                    quantity = num_text_to_int.get(quantity, 1)

                if best_match in order_dict:
                    order_dict[best_match] += quantity
                else:
                    order_dict[best_match] = quantity

        return order_dict

    # Función para verificar los pedidos contra el menú disponible
    def verify_order_with_menu(order_dict, menu):
        available_orders = {}
        unavailable_orders = []

        for dish, quantity in order_dict.items():
            if dish in menu['Plato'].values:
                available_orders[dish] = quantity
            else:
                unavailable_orders.append(dish)

        return available_orders, unavailable_orders

    # Función para mostrar el menú en un formato amigable
    def format_menu(menu):
        if menu.empty:
            return "No hay platos disponibles."
        formatted_menu = [f"**{row['Plato']}**  \n{row['Descripción']}  \n**Precio:** S/{row['Precio']}" for idx, row in menu.iterrows()]
        return "\n\n".join(formatted_menu)

    # Cargar el menú y los distritos
    menu = load_menu("carta_amazonica.csv")
    districts = load_districts("distritos.csv")

    # Botón para limpiar la conversación
    if st.button("Limpiar Conversación", key="clear"):
        init_session_state()

    # Mostrar el historial de la conversación
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🍃" if message["role"] == "assistant" else "👤"):
            st.markdown(message["content"])

    # Entrada del usuario
    user_input = st.chat_input("Escribe aquí...")

    # Procesar la conversación
    if not st.session_state["order_placed"]:
        if user_input:
            order_dict = improved_extract_order_and_quantity(user_input, menu)
            if st.session_state["district_selected"]:
                district = st.session_state["current_district"]
            else:
                district = verify_district(user_input, districts)

            if district:
                st.session_state["district_selected"] = True
                st.session_state["current_district"] = district
                st.session_state.messages.append({"role": "assistant", "content": f"Perfecto, has seleccionado el distrito: {district}."})

            if order_dict:
                available_orders, unavailable_orders = verify_order_with_menu(order_dict, menu)
                st.session_state.messages.append({"role": "user", "content": user_input})

                if available_orders:
                    order_details = "\n".join([f"{quantity} x {dish}" for dish, quantity in available_orders.items()])
                    st.session_state.messages.append({"role": "assistant", "content": f"Tu pedido:  \n{order_details}."})
                    st.session_state["order_placed"] = True
                    save_order_to_csv(available_orders, district)
                else:
                    st.session_state.messages.append({"role": "assistant", "content": "No se encontraron platos disponibles en tu pedido."})

            else:
                st.session_state.messages.append({"role": "assistant", "content": "No pude entender tu pedido. Intenta nuevamente."})

    # Fin del contenedor de fondo
    st.markdown("</div>", unsafe_allow_html=True)
