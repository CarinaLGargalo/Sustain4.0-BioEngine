import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Sustain 4.0 - BioEngine",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
def init_session_state():
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

init_session_state()

# Sistema de autenticação com streamlit-authenticator
def check_authentication():
    """Verifica se o usuário está autenticado"""
    return st.session_state.get('authenticated', False)

def login_page():
    """Exibe a página de login com streamlit-authenticator"""
    
    # Centralizar título
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
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
        elif st.session_state["authentication_status"] == None:
            st.warning('⚠️ Por favor, insira username e password')
        elif st.session_state["authentication_status"]:
            st.session_state.authenticated = True
            st.session_state.username = st.session_state["username"]
            st.session_state.user_name = st.session_state["name"]
            st.session_state.login_time = pd.Timestamp.now()
            st.success(f'✅ Bem-vindo {st.session_state["name"]}!')
            import time
            time.sleep(1)
            st.rerun()  # Recarrega a página para mostrar o conteúdo principal
        
        # Botão Demo (acesso rápido)
        st.markdown("---")
        if st.button("👁️ Demo - Acesso Rápido", use_container_width=True):
            st.session_state.authenticated = True
            st.session_state.username = "demo"
            st.session_state.user_name = "Demo User"
            st.session_state.login_time = pd.Timestamp.now()
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
    
    # Informações de acesso
    st.markdown("---")
    st.info("""
    **💡 Usuários Pré-cadastrados:**
    - **admin** / admin123 (Administrador)
    - **pesquisador** / pesq2024 (Pesquisador)
    - **analista** / anl2024 (Analista)
    - **demo** / demo123 (Demonstração)
    
    Ou registre uma nova conta na aba "Cadastro"!
    """)

# Verificar autenticação antes de mostrar o conteúdo principal
if not check_authentication():
    login_page()
    st.stop()  # Para a execução aqui se não estiver autenticado


# Conteúdo principal da aplicação
st.title("🌿 Sustain 4.0 - BioEngine")
st.header(f"Bem-vindo, {st.session_state.get('user_name', '')}!")

# Verificar se acabou de fazer login (apenas uma vez)
if st.session_state.get('login_time') and not st.session_state.get('balloons_shown', False):
    st.balloons()  # Efeito visual de celebração
    st.session_state.balloons_shown = True

# Criar layout com duas colunas principais
main_col1, main_col2 = st.columns([2, 1], gap="large")

with main_col1:
    # Inicializar estados para criação de projeto
    if 'show_project_form' not in st.session_state:
        st.session_state.show_project_form = False
    
    # Botão para criar novo projeto
    if st.button("📁 Criar Novo Projeto", type="primary"):
        st.session_state.show_project_form = True

with main_col2:
    # Exibir projetos do usuário
    st.subheader("📋 Meus Projetos")
    
    username = st.session_state.username
    user_projects = st.session_state.user_projects.get(username, [])
    
    if not user_projects:
        st.info("🔍 Você ainda não tem projetos. Crie seu primeiro projeto!")
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
    
# Formulário de criação de projeto
if st.session_state.show_project_form:
    st.subheader("📋 Novo Projeto")
    
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
                st.success(f"Projeto '{project_name}' criado com sucesso!")
                st.session_state.show_project_form = False  # Fechar formulário após salvar