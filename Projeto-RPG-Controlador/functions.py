import pandas as pd
import streamlit as st
import os

file_path = os.path.abspath("Projeto-RPG-Controlador/datasets/Pasta1.xlsx")

# Função para carregar os dados do Excel
def load_data():
    try:
        return pd.read_excel(file_path, header=0)
    except FileNotFoundError:
        st.error("Arquivo 'Pasta1.xlsx' não encontrado. Verifique o caminho e o nome do arquivo.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return pd.DataFrame()