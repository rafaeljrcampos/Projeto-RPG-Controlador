import pandas as pd
import streamlit as st
import os
from PIL import Image
import requests
from io import BytesIO

# Função para carregar os dados do Excel
def load_data():
    file_path_first = os.path.abspath("Projeto-RPG-Controlador/datasets/Pasta1.xlsx")
    file_path_sec = os.path.abspath("datasets/Pasta1.xlsx")    
    try:
        try:
            return pd.read_excel(file_path_first, header=0)
        except:
            return pd.read_excel(file_path_sec, header=0)
    except FileNotFoundError:
        st.error("Arquivo 'Pasta1.xlsx' não encontrado. Verifique o caminho e o nome do arquivo.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return pd.DataFrame()
    
def openImage(player_stats):
    try:
        url = player_stats['Foto']
    except:
        url = player_stats
    response = requests.get(url)
    imagem = Image.open(BytesIO(response.content))
    imagem_resized = imagem.resize((250, 250))
    return imagem_resized