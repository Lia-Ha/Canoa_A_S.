import re
from fuzzywuzzy import process, fuzz

def improved_extract_order_and_quantity(prompt, menu):
    """Extrae el pedido y la cantidad del mensaje del usuario"""
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

