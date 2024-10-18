            verified_district = verify_district(user_input, districts)

            if verified_district:
                st.session_state.current_district = verified_district
                st.session_state.district_selected = True
                assistant_response = f"¡Perfecto! Enviaremos tu pedido a **{verified_district}**. Ahora, cuéntame, ¿qué te gustaría pedir?"
            else:
                assistant_response = "Lo siento, no hacemos envíos a ese distrito. Por favor, verifica el distrito o ingresa uno válido."

            st.session_state.messages.append({"role": "assistant", "content": assistant_response})

            with st.chat_message("assistant", avatar="🍃"):
                st.markdown(assistant_response)
    else:
        # Captura del pedido del usuario
        if user_input := st.chat_input("Escribe tu pedido aquí:"):
            st.session_state.messages.append({"role": "user", "content": user_input})

            extracted_order = improved_extract_order_and_quantity(user_input, menu)
            available_orders, unavailable_orders = verify_order_with_menu(extracted_order, menu)

            if available_orders:
                assistant_response = "He entendido tu pedido:\n" + "\n".join(
                    [f"{quantity}x {dish}" for dish, quantity in available_orders.items()]
                )
                save_order_to_csv(available_orders, st.session_state.current_district)
                st.session_state.order_placed = True
                assistant_response += f"\n\nTu pedido será enviado a **{st.session_state.current_district}**. ¡Gracias por tu preferencia!"
            else:
                assistant_response = "Lo siento, no he podido encontrar ningún plato en tu pedido."

            if unavailable_orders:
                assistant_response += "\n\nNo encontré estos platos: " + ", ".join(unavailable_orders)

            st.session_state.messages.append({"role": "assistant", "content": assistant_response})

            with st.chat_message("assistant", avatar="🍃"):
                st.markdown(assistant_response)
