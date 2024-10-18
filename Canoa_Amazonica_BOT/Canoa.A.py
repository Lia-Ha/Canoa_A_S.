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

if st.sidebar.button("Reiniciar"):
    st.session_state["messages"] = deepcopy(initial_state)

# Agregar el div del superpuesto en la parte superior
st.markdown("<div class='overlay'></div>", unsafe_allow_html=True)

# Menú lateral
menu = ["La Canoa Amazónica", "Ofertas", "Pedidos", "Reclamos"]
choice = st.sidebar.selectbox("Menú", menu)

# URLs de las imágenes
url_chica_comida = "https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Canoa_Amazonica_BOT/La%20Canooa.jpg"

# Mostrar imágenes en la barra lateral debajo del menú
st.sidebar.image(url_chica_comida, caption="Deliciosos Manjares de la Selva", use_column_width=True)

# URLs de las imágenes
url_cosina_cosineros = "https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Canoa_Amazonica_BOT/Cosineros.jpg"

# Mostrar imágenes en la barra lateral
st.sidebar.image(url_cosina_cosineros, caption="Contamos con un equipo de expertos dedicados a ofrecerte la mejor calidad.", use_column_width=True)

# URLs de las imágenes
url_Restaurante_comida = "https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Canoa_Amazonica_BOT/Fondo_Restaur.jpg"

# Mostrar imágenes en la barra lateral debajo del menú
st.sidebar.image(url_Restaurante_comida, caption="Cada viaje es una nueva historia por contar. Por eso cuentas con nosotros, para nuevas experiencias", use_column_width=True)

# URLs de las imágenes
url_Restaurante_comida = "https://raw.githubusercontent.com/Lia-Ha/Canoa_A_S./main/Canoa_Amazonica_BOT/Pulceras_Canoa.JPG"

# Mostrar imágenes en la barra lateral debajo del menú
st.sidebar.image(url_Restaurante_comida, caption="Adquiere dos pulseras de cortecia, para que la belleza de la naturaleza te acompañe día a día", use_column_width=True)

# Mensaje de bienvenida
if choice == "La Canoa Amazónica":
    welcome_message = """
    <h2 style='color: black;'>¡Bienvenidos a La Canoa Amazónica! 🌿🍃</h4>   
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
        {"plato": "Inchicapi con Paiche", "descripcion": "Variante del inchicapi tradicional, pero con filete de paiche", "precio": 38.5},
        {"plato": "Purtumute", "descripcion": "Estofado de frijoles y maíz, acompañado de carne de res o cerdo", "precio": 25}
    ]

    st.subheader("Verificación de la Carta")
    selected_plate = st.selectbox("Selecciona un plato", [c["plato"] for c in carta])
    
    if st.button("Verificar Plato"):
        for plato in carta:
            if plato["plato"] == selected_plate:
                verification_plate = {
                    "verificacion": {
                        "estado": "confirmado",
                        "fecha": datetime.now().strftime("%Y-%m-%d"),
                        "codigo_verificacion": "PLATO-001",
                        "responsable": "Lila Huanca"
                    },
                    "plato": plato
                }
                # Guardar verificación en un archivo JSON
                with open("verif.carta.json", "w") as

    # Cargar el menú y los distritos
    menu = load("carta.csv")
    district = load_district("distrito.csv")
    bebidas= load("Bebidas.csv")
    postres= load("Postres.csv")

    # Función para mostrar el menú en un formato amigable
    def format_menu(menu):
        if menu.empty:
            return "No hay platos disponibles."

def display_confirmed_order(order_details):
    """Genera una tabla en formato Markdown para el pedido confirmado."""
    table = "| **Plato** | **Cantidad** | **Precio Total** |\n"
    table += "|-----------|--------------|------------------|\n"
    for item in order_details:
        table += f"| {item['Plato']} | {item['Cantidad']} | S/{item['Precio Total']:.2f} |\n"
    table += "| **Total** |              | **S/ {:.2f}**      |\n".format(sum(item['Precio Total'] for item in order_details))
    return table




# Ajustar el tono del bot
def adjust_tone(tone="friendly"):
    """Ajustar el tono del bot según las preferencias del cliente."""
    if tone == "formal":
        st.session_state["tone"] = "formal"
        return "Eres un asistente formal y educado."
    else:
        st.session_state["tone"] = "friendly"
        return "Eres un asistente amigable y relajado."

        
initial_state = [
    {"role": "system", "content": get_system_prompt(menu,distritos)},
    {
        "role": "assistant",
        "content": f"¡Hola! Aquí te brindo nuestro menú del día, con que deleite quieres iniciar hoy? \n\n{format_menu(menu)}\n\n¿Qué platillo te parece más apetitoso?",
    },
]


if "messages" not in st.session_state:
    st.session_state["messages"] = deepcopy(initial_state)


if st.sidebar.button("Reiniciar"):
    st.session_state["messages"] = deepcopy(initial_state)
st.sidebar.image("https://img.freepik.com/fotos-premium/horizonte-puesta-sol-vision-panoramica-seul-corea-sur-encanto-nocturno-papel-pared-movil-vertical_892776-27123.jpg", use_column_width=True)  # Ajusta el tamaño según necesites





    # Mostrar el historial de la conversación
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🍃" if message["role"] == "assistant" else "👤"):
            st.markdown(message["content"])

    # Entrada del usuario
    user_input = st.chat_input("Escribe aquí...")

##Pendiente


def get_system_prompt(menu, distritos):
    """Define el prompt del sistema para el bot de Sazón incluyendo el menú y distritos."""
    lima_tz = pytz.timezone('America/Lima')  # Define la zona horaria de Lima
    hora_lima = datetime.now(lima_tz).strftime("%Y-%m-%d %H:%M:%S")  # Obtiene la hora actual en Lima
    system_prompt = f"""
    Eres el bot de pedidos que nos ayuda siendo amable y servicial. Ayudas a los clientes a hacer sus pedidos y siempre confirmas que solo pidan platos que están en el menú oficial. Aquí tienes el menú o en otras palabra carta para mostrárselo a los clientes:\n{display_menu(menu)}\n
    También repartimos en los siguientes distritos: {display_distritos(distritos)}.\n
    Primero, saluda al cliente y ofrécele el menú. Asegúrate de que el cliente solo seleccione platos que están en el menú actual y explícales que no podemos preparar platos fuera del menú.
    **IMPORTANTE: Validación de cantidad solicitada**
    - El cliente puede indicar la cantidad en texto (por ejemplo, "dos") o en números (por ejemplo, "2").
    - Interpreta y extrae las cantidades independientemente de si están en números o en palabras y asócialas correspondientemente.
    - Por ejemplo, si el cliente escribe "quiero dos arroz con pollo y diez pachamanca de pollo", interpreta esto como "2 unidades de arroz con pollo" y "10 unidades de pachamanca de pollo".
    - Si la cantidad solicitada está en el rango de 1 hasta 30 (inclusive), acepta el pedido sin mostrar advertencias.
    - Si la cantidad solicitada es mayor que 30, muestra el siguiente mensaje:
       "Lamentablemente según nuestra política del restaurante el límite máximo de cantidad por producto es de 30 unidades. Pero te damos la opción de comunicarte con el dueño mediante este número +51 981 884 964 para que lleguen a un acuerdo mutuo para enviar pedidos más grandes. Y para poder continuar, por favor reduce la cantidad de tu pedido. "
      
    Después de que el cliente haya seleccionado sus platos, mencionale que la entrega es a domicilio y pregúntale a qué distrito desea que se le envíe su pedido, confirma que el distrito esté dentro de las zonas de reparto y verifica el distrito de entrega con el cliente y pregúntales su direccion.
    - Si te da su dirección lo colocas juntamente con el distrito en la confirmación del envio.

    Usa solo español peruano en tus respuestas, evitando palabras como "preferís" y empleando "prefiere" en su lugar.
    
    Antes de continuar, confirma que el cliente haya ingresado un método de entrega válido. Luego, resume el pedido en la siguiente tabla:\n
    | **Plato**      | **Cantidad**|***Precio Unitario * | **Precio Total** |\n
    |----------------|-------------|-------|------------------|\n
    |                |             |       |                  |\n
    | **Total**      |             |       | **S/ 0.00**      |\n
    
    Aclara que el monto total del pedido no acepta descuentos ni ajustes de precio.
    
    Después, pregunta al cliente si quiere añadir una bebida o postre.
	- Si responde bebida, muéstrale únicamente la carta de bebidas:{display_bebida(bebidas)}
	- Si responde postre, muéstrale solo la carta de postres:{display_postre(postres)}
    *Después de que el cliente agrega bebidas o postres, pregúntale si desea agregar algo más.* Si el cliente desea agregar más platos, bebidas o postres, permite que lo haga. Si no desea agregar más, continúa con el proceso.

    Si el cliente agrega más ítems, actualiza la tabla de resumen del pedido, recalculando el monto total con precisión.

    Antes de terminar, pregúntale al cliente: "¿Estás de acuerdo con el pedido?" y espera su confirmación.

    **Luego de confirmar el pedido, pregunta explícitamente al cliente por el método de pago, pero antes decirle porfavor y de hay mencionar el metodo de pago.** Menciona los metodos de pago establecidos (tarjeta, efectivo, Yape, Plin y Contra Entrega) y**verifica que el cliente haya ingresado una opción válida antes de continuar**.
   
    Luego de verificar el método de pago, confirma el pedido al cliente incluyendo todos los detalles. Incluye explícitamente:
    	El pedido confirmado será:\n
    	{display_confirmed_order([{'Plato': '', 'Cantidad': 0, 'Precio Total': 0}])}\n
	- *Método de pago*: el método que el cliente eligió.
	- *Lugar de entrega*: el distrito de entrega  y la dirección que proporciono, pero antes de poner la dirección agregarle "-".
	- *Timestamp Confirmacion*: hora exacta de confirmación del pedido, el valor '{hora_lima}'.
         
    Recuerda siempre confirmar que el pedido, el metodo de pago y el lugar de entrega estén hayan sido ingresados, completos y correctos antes de registrarlo.
    """
    return system_prompt.replace("\n", " ")
   
def extract_order_json(response):
    """Extrae el pedido confirmado en formato JSON desde la respuesta del bot solo si todos los campos tienen valores completos."""
    prompt = f"""
		A partir de la siguiente respuesta del asistente, extrae la información del pedido confirmado.

		Respuesta del asistente:
		'''{response}'''

		Proporciona un JSON con el siguiente formato:

		{{
    			"Platos": [
        			{{"Plato": "Nombre del plato", "Cantidad": cantidad, "Precio Total": precio_total}},
        			...
    				],
    			"Total": total_pedido,
    			"Metodo de Pago": "metodo_de_pago",
    			"Lugar de Entrega": "lugar_entrega",
    			"Timestamp Confirmacion": "timestamp_confirmacion"
		}}

		Si algún campo no aparece en la respuesta, asígnale el valor null.

		Si el pedido no está confirmado explícitamente en la respuesta, devuelve un JSON vacío: {{}}.
  		Responde *solo* con el JSON, sin explicaciones adicionales.
    		"""
    #prompt = f"Extrae la información del pedido confirmado solo de la siguiente respuesta: '{response}'. Si el pedido está confirmado, proporciona una salida en formato JSON con las siguientes claves: 'Platos' (contiene los platos, cada uno con su cantidad y precio_total), 'Total', 'metodo de pago', 'lugar_entrega', y 'timestamp_confirmacion'. Si algún campo como 'metodo de pago' o 'lugar_entrega'o 'timestamp_confirmacion' no está presente, asígnale el valor null. Si el pedido no está confirmado, devuelve un diccionario vacio."
    #prompt = f"Extrae la información del pedido de la siguiente respuesta: '{response}'. Si el pedido está confirmado proporciona una salida en formato JSON con las claves: Platos(contine los platos con la cantidad y precio_total),Total,metodo de pago,lugar_entrega y timestamp_confirmacion. Si el pedido no está confirmado devuelve una diccionario vacio."

    extraction = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Eres un asistente que extrae información de pedidos en formato JSON a partir de la respuesta proporcionada."},
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo",
        temperature=0,
        max_tokens=300,
        top_p=1,
        stop=None,
        stream=False,
    )
#"gemma2-9b-it"
    response_content = extraction.choices[0].message.content
    
    # Intenta cargar como JSON
    try:
        order_json = json.loads(response_content)
        #st.markdown(order_json)
        #st.markdown(type(order_json))
        # Verifica si el JSON es un diccionario
        if isinstance(order_json, dict):
            if all(order_json[key] not in (None, '', [], {}) for key in order_json):
                return order_json
            else:
                print("Advertencia: Hay claves con valores nulos o vacíos en el pedido.")
                return {}
            # Verifica que todas las claves en order_json tengan valores no nulos
            #return order_json if order_json else {}
        
        # Si el JSON es una lista, devuelves un diccionario vacío o manejas la lista de otro modo
        elif isinstance(order_json, list):
            print("Advertencia: Se recibió una lista en lugar de un diccionario.")
            return {}
        
        # Si no es ni lista ni diccionario, retorna un diccionario vacío
        else:
            return {}
    
    except json.JSONDecodeError:
        # Manejo de error en caso de que el JSON no sea válido
        return {}

def generate_response(prompt, temperature=0,max_tokens=1000):
    """Enviar el prompt a Groq y devolver la respuesta con un límite de tokens."""
    st.session_state["messages"].append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state["messages"],
        temperature=temperature,
        max_tokens=max_tokens,
        stream=False,
    )
    response = completion.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": response})
    # Extraer JSON del pedido confirmado
    order_json = extract_order_json(response)
    #st.markdown(order_json)
    #st.markdown(type(order_json))
    logging.info(json.dumps(order_json, indent=4) if order_json else '{}')
    return response
# Función para verificar contenido inapropiado
def check_for_inappropriate_content(prompt):
    """Verifica si el prompt contiene contenido inapropiado utilizando la API de Moderación de OpenAI."""
    try:
        response = client.moderations.create(input=prompt)
        logging.info(f"Moderation API response: {response}")
         # Acceso correcto a los resultados de la respuesta de moderación
        moderation_result = response.results[0]
        
        # Verifica si está marcado como inapropiado
        if moderation_result.flagged:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Error al llamar a la API de Moderación: {e}")
        return False  



 # Mostrar la respuesta del asistente
    if user_input:
        with st.chat_message("assistant", avatar="🍃"):
            response_html = f"<p style='color: white;'>{response}</p>"
            st.markdown(response_html, unsafe_allow_html=True)

        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": response})

elif choice == "Reclamos":
    # Manejo de reclamos
    st.markdown("""
        <h2 style='color: black;'>Deja tu Reclamo</h2> 
    """, unsafe_allow_html=True)

    complaint = st.text_area("Escribe tu reclamo aquí...")

    if st.button("Enviar Reclamo"):
        if complaint:
            response = "Tu reclamo está en proceso. Te devolveremos tu dinero en una hora al verificar la información. Si tu pedido no llegó a tiempo o fue diferente a lo que pediste, también te ofreceremos cupones por la mala experiencia de tu pedido."
            st.success(response)
            response_html = f"<p style='color: black;'>{response}</p>"
            st.markdown(response_html, unsafe_allow_html=True)
        else:
            st.error("Por favor, escribe tu reclamo antes de enviarlo.")

# Agregar mensaje de despedida en la parte inferior
st.markdown("---")
st.markdown("¡Gracias por visitar La Canoa Amazónica! 🌿🍽️")
