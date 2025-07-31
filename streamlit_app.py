import streamlit as st
import base64

# Função para converter imagem em base64
def get_base64_of_image(path):
    """Converte uma imagem em string base64"""
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

# Inicializar session state primeiro (antes de qualquer verificação)
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

init_session_state()

# Sistema de autenticação simples
def check_authentication():
    """Verifica se o usuário está autenticado"""
    return st.session_state.get('authenticated', False)

st.set_page_config(
    page_title="Sustain 4.0 - BioEngine",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def authenticate_user(username, password):
    """Autentica o usuário com credenciais predefinidas"""
    # Credenciais de exemplo (em produção, usar banco de dados ou sistema mais seguro)
    valid_users = {
        "admin": "admin123",
        "pesquisador": "pesq2024",
        "analista": "anl2024",
        "demo": "demo123"
    }
    
    return valid_users.get(username) == password

def login_page():
    """Exibe a página de login"""

    # Centralizar logo no topo da página
    col1, col2, col3 = st.columns([1, 2, 1])
        
    # Centralizar título
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
      st.markdown(
        "<h1 class='main-title' style='text-align: center; font-size: 2.5em; font-weight: 700;'>Sustain4.0 BioEngine</h1>",
        unsafe_allow_html=True
      )

    # Centralizar o formulário de login
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(
            "<h3 style='text-align: center;'>Faça seu Login</h3>",
            unsafe_allow_html=True
        )
        
        # Formulário de login
        with st.form("login_form"):
            username = st.text_input("👤 Usuário:", placeholder="Digite seu usuário")
            password = st.text_input("🔑 Senha:", type="password", placeholder="Digite sua senha")
            
            col_login1, col_login2 = st.columns(2)
            with col_login1:
                login_button = st.form_submit_button("🔓 Entrar", type="primary", use_container_width=True)
            with col_login2:
                demo_button = st.form_submit_button("👁️ Demo", use_container_width=True)
            
            if login_button:
                if username and password:
                    if authenticate_user(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.login_time = pd.Timestamp.now()
                        st.success("✅ Login realizado com sucesso! Redirecionando para a página inicial...")
                        import time
                        time.sleep(1)  # Pausa de 1 segundo para o usuário ver a mensagem
                        st.switch_page("pages/1_🏠_Home.py")
                    else:
                        st.error("❌ Usuário ou senha inválidos!")
                else:
                    st.warning("⚠️ Por favor, preencha usuário e senha!")
            
            elif demo_button:
                st.session_state.authenticated = True
                st.session_state.username = "demo"
                st.session_state.login_time = pd.Timestamp.now()
                st.success("✅ Acesso demo autorizado! Redirecionando para a página inicial...")
                import time
                time.sleep(1)  # Pausa de 1 segundo para o usuário ver a mensagem
                st.switch_page("pages/1_🏠_Home.py")

        st.markdown("---")
        st.write("Essa é uma descrição do Sustain 4.0 BioEngine, uma plataforma integrada de análise de sustentabilidade ambiental. A ideia é fornecer uma interface intuitiva para pesquisadores e analistas ambientais, permitindo análises de biodiversidade, monitoramento de carbono, qualidade da água e saúde do solo.")
        # Informações de acesso
        st.markdown("---")
        st.info("""
        **💡 Usuários de Teste:**
        - **admin** / admin123 (Administrador)
        - **pesquisador** / pesq2024 (Pesquisador)
        - **analista** / anl2024 (Analista)
        - **demo** / demo123 (Demonstração)
        
        Ou clique em **Demo** para acesso rápido.
        """)

# Importar pandas para timestamp (se não estiver importado)
import pandas as pd

# Verificar autenticação antes de mostrar o conteúdo principal
if not check_authentication():
    login_page()
    st.stop()  # Para a execução aqui se não estiver autenticado