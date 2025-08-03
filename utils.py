import streamlit as st
import pandas as pd
import json
import os
import yaml
from yaml.loader import SafeLoader
from pathlib import Path

# Função para verificar autenticação
def check_authentication():
    """Verifica se o usuário está autenticado"""
    return st.session_state.get('authenticated', False)

# Criar diretório de dados se não existir
def ensure_data_dir():
    """Garante que o diretório de dados exista"""
    data_dir = Path("./data")
    if not data_dir.exists():
        data_dir.mkdir()
    return data_dir

# Função para salvar dados do usuário
def save_user_data(username, data):
    """Salva os dados do usuário em um arquivo JSON"""
    data_dir = ensure_data_dir()
    user_file = data_dir / f"{username}.json"
    
    with open(user_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, default=str, ensure_ascii=False, indent=2)
        
# Função para carregar dados do usuário
def load_user_data(username):
    """Carrega os dados do usuário de um arquivo JSON"""
    data_dir = ensure_data_dir()
    user_file = data_dir / f"{username}.json"
    
    if user_file.exists():
        try:
            with open(user_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Erro ao carregar dados do usuário: {e}")
            return {}
    else:
        return {}

# Função para carregar configuração
@st.cache_data
def load_config():
    """Carrega a configuração de usuários do arquivo YAML"""
    try:
        with open('config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)
        return config
    except FileNotFoundError:
        # Configuração padrão se o arquivo não existir
        return {
            'credentials': {'usernames': {}},
            'cookie': {
                'expiry_days': 30,
                'key': 'sustain40_bioengine_key',
                'name': 'sustain40_cookie'
            },
            'preauthorized': {'emails': []}
        }

# Função para salvar configuração
def save_config(config):
    """Salva a configuração de usuários no arquivo YAML"""
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

# Inicializar session state
def init_session_state():
    """Inicializa variáveis de estado da sessão"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    if 'notifications' not in st.session_state:
        st.session_state.notifications = True
    if 'theme' not in st.session_state:
        st.session_state.theme = "Claro"
    if 'user_projects' not in st.session_state:
        st.session_state.user_projects = {}  # Dicionário para armazenar projetos por username
    if 'last_save_time' not in st.session_state:
        st.session_state.last_save_time = pd.Timestamp.now()

# Função para carregar dados do usuário quando faz login
def load_user_data_on_login(username):
    """Carrega os dados do usuário e atualiza a session_state"""
    user_data = load_user_data(username)
    
    # Carregar projetos
    if 'projects' in user_data:
        st.session_state.user_projects[username] = user_data['projects']
    
    # Carregar projeto selecionado anteriormente (se existir)
    if 'selected_project_index' in user_data:
        projects = st.session_state.user_projects.get(username, [])
        selected_idx = user_data['selected_project_index']
        if 0 <= selected_idx < len(projects):
            st.session_state.selected_project = selected_idx
            st.session_state.current_project = projects[selected_idx]
    
    # Carregar configurações pessoais
    if 'preferences' in user_data:
        preferences = user_data['preferences']
        if 'theme' in preferences:
            st.session_state.theme = preferences['theme']
        if 'notifications' in preferences:
            st.session_state.notifications = preferences['notifications']
    
    # Carregar outras informações personalizadas
    if 'custom_data' in user_data:
        st.session_state.custom_data = user_data['custom_data']

# Função para auto-salvar os dados do usuário
def auto_save_user_data():
    """Auto-salvar dados do usuário a cada 5 minutos"""
    if not st.session_state.get('username'):
        return
        
    current_time = pd.Timestamp.now()
    last_save = st.session_state.get('last_save_time', pd.Timestamp.now())
    
    # Verifica se já passou pelo menos 5 minutos desde a última vez que salvamos
    if (current_time - last_save).total_seconds() >= 300:  # 300 segundos = 5 minutos
        username = st.session_state.username
        
        # Recuperar os projetos existentes
        user_projects = st.session_state.user_projects.get(username, [])
        
        # Dados a serem salvos
        user_data = {
            'projects': user_projects,
            'preferences': {
                'theme': st.session_state.theme,
                'notifications': st.session_state.notifications
            },
            'last_update': current_time.strftime("%Y-%m-%d %H:%M:%S"),
            'auto_saved': True
        }
        
        # Salvar dados do usuário
        save_user_data(username, user_data)
        st.session_state.last_save_time = current_time
