import pandas as pd
import streamlit as st
from datetime import datetime
from fuzzywuzzy import fuzz, process
import json
import pytz
from copy import deepcopy

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

# Reiniciar la aplicación
if st.sidebar.button("Reiniciar"):
    st.session_state["messages"] = deepcopy(initial_state)

# Agregar el div del superpuesto en la parte superior
st.markdown("<div class='overlay'></div>", unsafe_allow_html=True)

# Menú lateral
menu = ["La Canoa Amazónica", "Ofertas", "Pedidos", "Reclamos"]
choice = st.sidebar.selectbox("Menú", menu)

# Mostrar imágenes en la barra lateral
url_images = [
    "https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Canoa_Amazonica_BOT/La%20Canooa.jpg",
    "https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Canoa_Amazonica_BOT/Cosineros.jpg",
    "https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Canoa_Amazonica_BOT/Fondo_Restaur.jpg",
    "https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Canoa_Amazonica_BOT/Pulceras_Canoa.JPG"
]
captions = [
    "Deliciosos Manjares de la Selva",
    "Contamos con un equipo de expertos dedicados a ofrecerte la mejor calidad.",
    "Cada viaje es una nueva historia por contar. Por eso cuentas con nosotros, para nuevas experiencias.",
    "Adquiere dos pulseras de cortecia, para que la belleza de la naturaleza te acompañe día a día."
]

for url, caption in zip(url_images, captions):
    st.sidebar.image(url, caption=caption, use_column_width=True)

# Mensaje de bienvenida
if choice == "La Canoa Amazónica":
    welcome_message = """
    <h2 style='color: black;'>¡Bienvenidos a La Canoa Amazónica! 🌿🍃</h2>   
    <p style='color: black;'>Si eres amante de la comida exótica y auténtica de nuestra querida selva, aquí te ofrecemos una experiencia gastronómica única que no querrás perderte.</p>
    """
    st.markdown(welcome_message, unsafe_allow_html=True)

elif choice == "Ofertas":
    offers_message = """¡Promo familiar! 3 juanes a 70 soles, más una botella de 2 litros de chicha morada.  
    ¡Tacacho con cecina 2 por 30 soles! ¡Super promo!"""
    st.markdown(offers_message)

elif choice == "Pedidos":
    intro = """
    <h2 style='color: black;'>¡Descubre los Sabores de la Selva en La Canoa Amazónica! 🌿🍃</h2>  
    <p style='color: black;'>Llegaste al rincón del sabor, donde la selva te recibe con sus platos más deliciosos.</p>  
    <p style='color: black;'>¿Qué se te antoja hoy? ¡Escribe "Carta" para comenzar!</p>
    """
    st.markdown(intro, unsafe_allow_html=True)

    # Verificación de distritos
    distritos = [
        "Miraflores", "San Isidro", "Barranco", "La Molina", "Surco", 
        "San Borja", "Pueblo Libre", "Lince", "Chorrillos", "San Miguel", 
        "Magdalena del Mar", "Callao", "Rímac", "Carabayllo", "Villa El Salvador"
    ]

    st.subheader("Verifica tu distrito")
    selected_district = st.selectbox("Selecciona tu distrito", distritos)
    
    if st.button("Verificar Distrito"):
        verification_district = {
            "verificacion": {
                "estado": "confirmado",
                "fecha": datetime.now().strftime("%Y-%m-%d"),
                "codigo_verificacion": "DISTRITO-001",
                "responsable": "Lila Huanca"
            },
            "distrito": selected_district
        }
        # Guardar verificación en un archivo JSON
        with open("verif.distrito.json", "w") as f:
            json.dump(verification_district, f)
        st.success(f"Distrito verificado: {selected_district}")

    # Verificación de bebidas
    bebidas = [
        {"bebida": "Aguajina", "descripcion": "Bebida refrescante elaborada con aguaje, una fruta típica de la Amazonía", "precio": 10},
        {"bebida": "Chapo", "descripcion": "Refresco natural a base de plátano maduro, azúcar y canela", "precio": 9},
        {"bebida": "Masato", "descripcion": "Bebida fermentada de yuca, tradicional en la Amazonía, con un sabor único", "precio": 12},
        {"bebida": "Refresco de Camu Camu", "descripcion": "Bebida hecha con camu camu, rica en vitamina C, mezclada con agua", "precio": 9.5},
        {"bebida": "Sorpresa Amazónica", "descripcion": "Mezcla de jugos de frutas amazónicas como guanábana y maracuyá", "precio": 11.5},
        {"bebida": "Bebida de Castaña", "descripcion": "Refresco dulce elaborado con castaña y un toque de canela", "precio": 12},
        {"bebida": "Jugo de Maracuyá", "descripcion": "Bebida refrescante elaborada con maracuyá", "precio": 10},
        {"bebida": "Jugo de Huayo", "descripcion": "Bebida refrescante a base de huayo, dulce y aromática", "precio": 10},
        {"bebida": "Refresco de Pitahaya", "descripcion": "Bebida hecha con jugo de pitahaya y un toque de limón", "precio": 12},
        {"bebida": "Refresco de Carambola", "descripcion": "Bebida refrescante hecha con jugo de carambola", "precio": 10}
    ]

    st.subheader("Verificación de Bebidas")
    selected_beverage = st.selectbox("Selecciona tu bebida", [b["bebida"] for b in bebidas])
    
    if st.button("Verificar Bebida"):
        for bebida in bebidas:
            if bebida["bebida"] == selected_beverage:
                verification_beverage = {
                    "verificacion": {
                        "estado": "confirmado",
                        "fecha": datetime.now().strftime("%Y-%m-%d"),
                        "codigo_verificacion": "BEBIDA-001",
                        "responsable": "Lila Huanca"
                    },
                    "bebida": bebida
                }
                # Guardar verificación en un archivo JSON
                with open("verif.bebida.json", "w") as f:
                    json.dump(verification_beverage, f)
                st.success(f"Bebida verificada: {selected_beverage}")
                break

    # Verificación de la carta
    carta = [
        {"plato": "Juane", "descripcion": "Arroz con pollo envuelto en hoja de bijao, acompañado de aceitunas y huevo", "precio": 25},
        {"plato": "Inchicapi", "descripcion": "Sopa espesa a base de pollo, yuca y aguaje", "precio": 18},
        {"plato": "Cecina", "descripcion": "Pechuga de pollo a la parrilla con salsa teriyaki y arroz", "precio": 20},
        {"plato": "Sopa de Carachama", "descripcion": "Sopa hecha de pescado carachama, yuca y especias", "precio": 30},
        {"plato": "Tacacho con cecina", "descripcion": "Puré de plátano con cecina", "precio": 20},
        {"plato": "Patarashca", "descripcion": "Pescado asado envuelto en hoja de bijao con especias amazónicas", "precio": 35},
        {"plato": "Paiche a la Parrilla", "descripcion": "Filete de paiche a la parrilla con ensalada y arroz", "precio": 40},
        {"plato": "Chaufa Amazónico", "descripcion": "Arroz chaufa con cecina, chorizo regional y plátano maduro", "precio": 50.5},
        {"plato": "Inchicapi con Paiche", "descripcion
    # Guarda la verificación del plato en un archivo JSON
    with open("verif.carta.json", "w") as f:
        json.dump(verification_plate, f)
    st.success(f"Plato verificado: {selected_plate}")
    break

# Cargar el menú, distritos y bebidas
def load_data():
    menu = pd.read_csv("carta.csv")
    district = pd.read_csv("distrito.csv")
    bebidas = pd.read_csv("Bebidas.csv")
    postres = pd.read_csv("Postres.csv")
    return menu, district, bebidas, postres

menu, district, bebidas, postres = load_data()

# Función para mostrar el menú en un formato amigable
def format_menu(menu):
    if menu.empty:
        return "No hay platos disponibles."
    
    formatted_menu = "| **Plato** | **Descripción** | **Precio** |\n"
    formatted_menu += "|-----------|----------------|------------|\n"
    for index, row in menu.iterrows():
        formatted_menu += f"| {row['plato']} | {row['descripcion']} | S/{row['precio']:.2f} |\n"
    return formatted_menu

# Mostrar el menú formateado
st.subheader("Menú del Restaurante")
st.markdown(format_menu(menu), unsafe_allow_html=True)

# Función para mostrar los distritos en un formato amigable
def display_distritos(distritos):
    return ", ".join(distritos)

# Función para mostrar las bebidas en un formato amigable
def display_bebidas(bebidas):
    formatted_bebidas = "| **Bebida** | **Descripción** | **Precio** |\n"
    formatted_bebidas += "|------------|----------------|------------|\n"
    for bebida in bebidas:
        formatted_bebidas += f"| {bebida['bebida']} | {bebida['descripcion']} | S/{bebida['precio']:.2f} |\n"
    return formatted_bebidas

# Función para mostrar los postres en un formato amigable
def display_postres(postres):
    formatted_postres = "| **Postre** | **Descripción** | **Precio** |\n"
    formatted_postres += "|------------|----------------|------------|\n"
    for postre in postres:
        formatted_postres += f"| {postre['postre']} | {postre['descripcion']} | S/{postre['precio']:.2f} |\n"
    return formatted_postres

# Confirmar el pedido del cliente
if st.button("Confirmar Pedido"):
    st.session_state["order_placed"] = True
    st.success("Tu pedido ha sido confirmado. ¡Gracias por elegir La Canoa Amazónica!")

# Mensaje de despedida
if st.session_state["order_placed"]:
    goodbye_message = """
    <h2 style='color: black;'>¡Hasta Pronto! 🌟</h2>
    <p style='color: black;'>Esperamos que disfrutes de tu comida. Si necesitas algo más, no dudes en volver.</p>
    """
    st.markdown(goodbye_message, unsafe_allow_html=True)

# Mostrar el historial de la conversación
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🍃" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Entrada del usuario
user_input = st.chat_input("Escribe aquí...")

# Procesar la entrada del usuario
if user_input:
    response = process_user_input(user_input, st.session_state["messages"])
    st.session_state["messages"].append({"role": "assistant", "content": response})

def process_user_input(input_text, messages):
    # Lógica para procesar la entrada del usuario
    response = ""
    # Aquí puedes añadir la lógica para manejar las diferentes respuestas según el input del usuario
    # Por ejemplo, puedes usar condiciones para verificar si el input corresponde a un plato, bebida, etc.
    return response

# Ajustar el tono del bot
def adjust_tone(tone="friendly"):
    """Ajustar el tono del bot según las preferencias del cliente."""
    if tone == "formal":
        st.session_state["tone"] = "formal"
        return "Eres un asistente formal y educado."
    else:
        st.session_state["tone"] = "friendly"
        return "Eres un asistente amigable y relajado."

