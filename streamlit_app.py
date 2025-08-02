import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import os
import streamlit as st
import pandas as pd
import time
import bcrypt

# Configuração da página - DEVE ser o primeiro comando Streamlit
st.set_page_config(
    page_title="Sustain 4.0 - BioEngine",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from pathlib import Path
import streamlit_authenticator as stauth

# Background customizado com opacidade de 30%
page_bg__img = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.4)),
                url("https://images.unsplash.com/photo-1675130277336-23cb686f01c0?q=80&w=1374&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: cover;
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
}

/* Garantir que o conteúdo aparece sobre o fundo */
[data-testid="stToolbar"] {
    z-index: 1;
}
</style>
"""
st.markdown(page_bg__img, unsafe_allow_html=True)

# Importar funções do módulo utils
from utils import (
    load_config,
    save_config,
    ensure_data_dir,
    save_user_data,
    load_user_data,
    check_authentication,
    init_session_state,
    load_user_data_on_login,
    auto_save_user_data
)

# Inicializar configuração e authenticator
config = load_config()

# Criar o authenticator
authenticator = stauth.Authenticate(
    credentials=config['credentials'],
    cookie_name=config['cookie']['name'], 
    key=config['cookie']['key'],
    cookie_expiry_days=config['cookie']['expiry_days']
)

# Inicializar session state
init_session_state()

def login_page():
    """Exibe a página de login com streamlit-authenticator"""
    
    # Criar layout com uma coluna central
    col1, center_col, col3 = st.columns([1, 2, 1])
    
    # Todo o conteúdo vai na coluna central
    with center_col:

        # Centralizar título
        st.markdown(
            "<h1 class='main-title' style='text-align: center; font-size: 2.5em; font-weight: 700;'>Sustain4.0 BioEngine</h1>",
            unsafe_allow_html=True
        )
        
        # Criar abas para Login e Registro
        tab1, tab2 = st.tabs(["🔓 Login", "📝 Cadastro"])
        
        with tab1:
            st.markdown("### 🔓 Fazer Login")
            
            # Widget de login do streamlit-authenticator
            authenticator.login(location='main')
        
        if st.session_state["authentication_status"] == False:
            st.error('❌ Username/password incorretos')
        elif st.session_state["authentication_status"]:
            st.session_state.authenticated = True
            st.session_state.username = st.session_state["username"]
            st.session_state.user_name = st.session_state["name"]
            st.session_state.login_time = pd.Timestamp.now()
            st.session_state.balloons_shown = False  # Resetar a flag para permitir mostrar os balões
            
            # Carregar dados do usuário
            load_user_data_on_login(st.session_state["username"])
            st.rerun()  # Recarrega a página para mostrar o conteúdo principal
        
        # Botão Demo (acesso rápido)
        if st.button("👁️ Demo - Acesso Rápido", use_container_width=True):
            st.session_state.authenticated = True
            st.session_state.username = "demo"
            st.session_state.user_name = "Demo User"
            st.session_state.login_time = pd.Timestamp.now()
            st.session_state.balloons_shown = False  # Resetar a flag para permitir mostrar os balões
            
            # Carregar dados do usuário demo
            load_user_data_on_login("demo")
            
            st.rerun()  # Recarrega a página para mostrar o conteúdo principal
    
        with tab2:
            st.markdown("### 📝 Cadastrar Nova Conta")
            
            # Formulário customizado de registro
            with st.form("register_form"):
                st.write("Preencha os dados para criar sua conta:")
                
                new_name = st.text_input("Nome Completo:", placeholder="Digite seu nome completo")
                new_username = st.text_input("Username:", placeholder="Escolha um nome de usuário único")
                new_email = st.text_input("Email:", placeholder="Digite seu email")
                new_password = st.text_input("Senha:", type="password", placeholder="Digite uma senha segura")
                new_password_repeat = st.text_input("Confirmar Senha:", type="password", placeholder="Digite a senha novamente")
            
                submit_button = st.form_submit_button("📝 Criar Conta", type="primary", use_container_width=True)
                
                if submit_button:
                    # Validações
                    if not all([new_name, new_username, new_email, new_password, new_password_repeat]):
                        st.error("❌ Por favor, preencha todos os campos!")
                    elif new_password != new_password_repeat:
                        st.error("❌ As senhas não coincidem!")
                    elif new_username in config['credentials']['usernames']:
                        st.error("❌ Username já existe! Escolha outro.")
                    elif len(new_password) < 6:
                        st.error("❌ A senha deve ter pelo menos 6 caracteres!")
                    else:
                        # Adicionar novo usuário
                        import bcrypt
                        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                        
                        # Atualizar configuração
                        config['credentials']['usernames'][new_username] = {
                            'name': new_name,
                            'email': new_email,
                            'password': hashed_password
                        }
                        
                        # Salvar no arquivo
                        save_config(config)
                        
                        st.success("✅ Conta criada com sucesso!")
                        st.info("🔄 Agora você pode fazer login na aba Login!")

                        # Limpar cache para recarregar configuração
                        st.cache_data.clear()
                        
                        import time
                        time.sleep(2)
                        st.rerun()

        # Descrição da plataforma
        st.markdown("---")
        st.write("**Sustain 4.0 BioEngine** é uma plataforma integrada de análise de sustentabilidade ambiental. Fornecemos uma interface intuitiva para pesquisadores e analistas ambientais, permitindo análises de biodiversidade, monitoramento de carbono, qualidade da água e saúde do solo.")

# Verificar autenticação antes de mostrar o conteúdo principal
if not check_authentication():
    login_page()
    st.stop()  # Para a execução aqui se não estiver autenticado


# Conteúdo principal da aplicação

# Conteúdo principal da aplicação

# Conteúdo principal da aplicação

# Conteúdo principal da aplicação

# Conteúdo principal da aplicação

# Conteúdo principal da aplicação

# Conteúdo principal da aplicação

# Conteúdo principal da aplicação

# Conteúdo principal da aplicação

# Conteúdo principal da aplicação

# Conteúdo principal da aplicação

# Conteúdo principal da aplicação

# Conteúdo principal da aplicação

# Conteúdo principal da aplicação

# Auto-salvar dados do usuário
auto_save_user_data()

# Verificar se acabou de fazer login (apenas uma vez)
current_time = pd.Timestamp.now()
login_time = st.session_state.get('login_time')

# Apenas mostrar os balões se:
# 1. O usuário fez login recentemente (nos últimos 6 segundos)
# 2. Ainda não mostramos os balões
if login_time and (current_time - login_time).total_seconds() < 6:
    st.balloons()  # Efeito visual de celebração

# Aqui será colocado o cabeçalho com o nome do usuário e o botão de logout

colt1, colt2 = st.columns([10, 1])

with colt1:
    st.subheader(f"🌿 Bem-vindo, {st.session_state.get('user_name', '')}!")

with colt2:
    # Botão de logout
    if st.button("Logout"):
        # Salvar os dados do usuário antes de deslogar
        username = st.session_state.username
        
        # Recuperar os projetos existentes
        user_projects = st.session_state.user_projects.get(username, [])
        
        # Salvar dados do usuário antes de deslogar
        user_data = {
            'projects': user_projects,
            'preferences': {
                'theme': st.session_state.theme,
                'notifications': st.session_state.notifications
            },
            'last_update': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            'logout_time': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Salvar dados
        save_user_data(username, user_data)
        
        # Limpar a sessão
        for key in list(st.session_state.keys()):
            del st.session_state[key]
            
        # Reinicializar session state com valores padrão
        init_session_state()
        
        # Recarregar a página
        st.rerun()

st.markdown('---')

# # Criar layout com duas colunas principais
# main_col1, main_col2 = st.columns([1, 1])

# with main_col2:

# Inicializar estados para criação de projeto
if 'show_project_form' not in st.session_state:
    st.session_state.show_project_form = False

# Botão para criar novo projeto
if st.button("🧭 Criar Novo Projeto", type="primary"):
    st.session_state.show_project_form = True

    # Formulário de criação de projeto
if st.session_state.show_project_form:
    st.subheader("Novo Projeto")
    
    with st.form(key="new_project_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Nome do Projeto", placeholder="Digite um nome para o projeto")
            project_desc = st.text_area("Descrição", placeholder="Descreva o objetivo do projeto", height=100)
            
        with col2:
            project_type = st.selectbox("Tipo de Projeto", 
                                    ["Análise de Biodiversidade", 
                                    "Monitoramento de Carbono", 
                                    "Qualidade da Água",
                                    "Saúde do Solo",
                                    "Outro"])
            project_date = st.date_input("Data de Início")
            
        submit_project = st.form_submit_button("✅ Salvar Projeto", use_container_width=True)
        
        if submit_project:
            if not project_name:
                st.error("Por favor, informe pelo menos o nome do projeto!")
            else:
                # Criar novo projeto na session
                username = st.session_state.username
                
                # Inicializar a lista de projetos do usuário se ainda não existir
                if username not in st.session_state.user_projects:
                    st.session_state.user_projects[username] = []
                
                # Adicionar o projeto à lista do usuário
                new_project = {
                    'name': project_name,
                    'description': project_desc,
                    'type': project_type,
                    'date': project_date,
                    'created_at': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                st.session_state.user_projects[username].append(new_project)
                
                # Salvar dados do usuário
                user_data = {
                    'projects': st.session_state.user_projects[username],
                    'preferences': {
                        'theme': st.session_state.theme,
                        'notifications': st.session_state.notifications
                    },
                    'last_update': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                save_user_data(username, user_data)
                
                st.success(f"Projeto '{project_name}' criado com sucesso!")
                st.session_state.show_project_form = False  # Fechar formulário após salvar
                st.rerun()  # Recarregar a página para mostrar o novo projeto

st.subheader("Meus Projetos")
username = st.session_state.username
user_projects = st.session_state.user_projects.get(username, [])

if not user_projects:
    st.info("Você ainda não tem projetos. Crie um!")
else:
# Exibir projetos em cards
    for idx, project in enumerate(user_projects):
        with st.container():
            st.markdown(f"""
            **{project['name']}**  
            *Tipo:* {project['type']}  
            *Data:* {project['date'].strftime('%d/%m/%Y') if hasattr(project['date'], 'strftime') else project['date']}  
            """)
            st.markdown("---")

