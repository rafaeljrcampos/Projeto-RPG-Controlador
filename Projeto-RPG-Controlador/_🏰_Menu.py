import streamlit as st
import pandas as pd
from functions import load_data

st.set_page_config(page_title="Salão Principal", page_icon="🎲")
# Verifica se os dados já estão no session_state. Se não, carrega o Excel.
if 'data' not in st.session_state:
    st.session_state['data'] = load_data()

# Exibe o conteúdo da sidebar
st.sidebar.markdown("Desenvolvido por [Rafael Junior de Campos](https://github.com/rafaeljrcampos)")

# Título da página
st.markdown(
    """
    <h1 style="text-align: center;">🎲 PROJETO BÁSICO PARA CONTROLE DE RPG! 🧙🏻‍♂</h1>
    """,
    unsafe_allow_html=True
)
# Descrição do projeto
st.markdown(
    """
    Este projeto é uma ferramenta simples para **controle de personagens em RPG**, ideal para jogadores e mestres que desejam organizar suas aventuras.

    Com ele, é possível gerenciar informações como atributos, equipamentos e habilidades dos personagens de forma prática e intuitiva. 🎲✨

    Perfeito para quem busca simplicidade e eficiência durante suas campanhas.
    """
)