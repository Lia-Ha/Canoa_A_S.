import pandas as pd
import streamlit as st

def load_menu(csv_file):
    """Carga el menú desde un archivo CSV"""
    try:
        return pd.read_csv(csv_file, delimiter=';')
    except FileNotFoundError:
        st.error("Archivo de menú no encontrado.")
        return pd.DataFrame(columns=["Plato", "Descripción", "Precio"])
