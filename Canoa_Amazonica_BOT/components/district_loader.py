import pandas as pd
import streamlit as st

def load_districts(csv_file):
    """Carga los distritos de entrega desde un archivo CSV"""
    try:
        return pd.read_csv(csv_file)
    except FileNotFoundError:
        st.error("Archivo de distritos no encontrado.")
        return pd.DataFrame(columns=["Distrito"])

