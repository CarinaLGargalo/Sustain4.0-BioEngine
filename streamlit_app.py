import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from streamlit_option_menu import option_menu

# Configuração da página
st.set_page_config(layout="wide")
st.title('🌿Sustain 4.0 - BioEngine')

# Menu de abas no topo
selected_tab = option_menu(
    menu_title=None,  # Deixa o título vazio para simular abas
    options=["Home", "Análise", "Configurações"],  # Nomes das abas
    icons=["house", "bar-chart", "gear"],  # Ícones das abas
    menu_icon="cast",  # Ícone do menu (opcional)
    default_index=0,  # Aba padrão
    orientation="horizontal",  # Define a orientação como horizontal
)

# Conteúdo de cada aba
if selected_tab == "Home":
    st.header("Bem-vindo à página inicial!")
    st.write("Aqui está o conteúdo da aba Home.")
elif selected_tab == "Análise":
    st.header("Página de Análise")
    st.write("Aqui está o conteúdo da aba Análise.")
elif selected_tab == "Configurações":
    st.header("Configurações")
    st.write("Aqui está o conteúdo da aba Configurações.")

