import streamlit as st

# Configuração da página principal
st.set_page_config(
    page_title="Sustain 4.0 - BioEngine",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Sistema de autenticação simples
def check_authentication():
    """Verifica se o usuário está autenticado"""
    return st.session_state.get('authenticated', False)

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
    # Centralizar imagem e título juntos no centro da página usando columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
      st.markdown(
        "<h1 style='text-align: center; font-size: 2.5em; font-weight: 700;'>Sustain4.0 BioEngine</h1>",
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
                        st.session_state.login_time = st.session_state.get('login_time', pd.Timestamp.now())
                        st.success("✅ Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Usuário ou senha inválidos!")
                else:
                    st.warning("⚠️ Por favor, preencha usuário e senha!")
            
            elif demo_button:
                st.session_state.authenticated = True
                st.session_state.username = "demo"
                st.session_state.login_time = pd.Timestamp.now()
                st.success("✅ Acesso demo autorizado!")
                st.rerun()
        
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
        
        # Informações sobre o sistema
        st.markdown("---")
        st.markdown("""
        ### 🌿 Sobre o Sustain 4.0 - BioEngine
        
        **Funcionalidades Principais:**
        - 🌱 Análise de Biodiversidade
        - 🌍 Monitoramento de Carbono
        - 💧 Qualidade da Água
        - 🌿 Saúde do Solo
        
        **Características:**
        - Interface intuitiva e responsiva
        - Análises baseadas em Machine Learning
        - Visualizações interativas
        - Relatórios personalizáveis
        """)

# Inicializar session state global para manter dados entre páginas
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    if 'selected_analysis' not in st.session_state:
        st.session_state.selected_analysis = "Análise de Biodiversidade"
    if 'data_uploaded' not in st.session_state:
        st.session_state.data_uploaded = False
    if 'uploaded_data' not in st.session_state:
        st.session_state.uploaded_data = None
    if 'model_params' not in st.session_state:
        st.session_state.model_params = {'n_estimators': 100, 'max_depth': 10}
    if 'notifications' not in st.session_state:
        st.session_state.notifications = True
    if 'theme' not in st.session_state:
        st.session_state.theme = "Claro"

init_session_state()

# Importar pandas para timestamp (se não estiver importado)
import pandas as pd

# Verificar autenticação antes de mostrar o conteúdo principal
if not check_authentication():
    login_page()
    st.stop()  # Para a execução aqui se não estiver autenticado






# Página Principal - Boas-vindas
st.title("🌿 Sustain 4.0 - BioEngine")
st.markdown("### Plataforma Integrada de Análise de Sustentabilidade")

# Informações de login no topo
col_header1, col_header2, col_header3 = st.columns([2, 2, 1])
with col_header1:
    st.info(f"👤 **Usuário logado:** {st.session_state.username}")
with col_header2:
    if st.session_state.get('login_time'):
        login_time_str = st.session_state.login_time.strftime("%d/%m/%Y %H:%M:%S")
        st.info(f"🕐 **Login em:** {login_time_str}")
with col_header3:
    user_type = "👑 Admin" if st.session_state.username == "admin" else "🔬 Usuário"
    st.success(user_type)

# Instruções na sidebar
st.sidebar.success(f"� Bem-vindo, **{st.session_state.username}**!")
st.sidebar.success("�👆 Selecione uma página acima para navegar.")

# Botão de logout na sidebar
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout", type="secondary"):
    # Limpar apenas dados de autenticação, manter outras configurações
    st.session_state.authenticated = False
    st.session_state.username = ""
    if 'login_time' in st.session_state:
        del st.session_state.login_time
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info(
    """
    **📖 Como usar:**
    
    1. **🏠 Home**: Configure suas informações pessoais e do projeto
    2. **📊 Análise**: Execute análises de dados ambientais
    3. **⚙️ Configurações**: Ajuste preferências do sistema
    4. **� Dashboard**: Visualize resultados e métricas
    """
)


st.markdown("""
## 🎯 Bem-vindo ao Sustain 4.0 - BioEngine!

Uma plataforma completa para análise e monitoramento de sustentabilidade ambiental, 
desenvolvida para pesquisadores, analistas e gestores ambientais.

### 🚀 Funcionalidades Principais:

- **🌱 Análise de Biodiversidade**: Avalie a diversidade de espécies em seu projeto
- **🌍 Análise de Carbono**: Monitore emissões e sequestro de carbono
- **💧 Análise de Água**: Avalie qualidade e disponibilidade hídrica
- **🌿 Análise de Solo**: Monitore saúde e qualidade do solo

### 📊 Características:

- Interface intuitiva e responsiva
- Análises baseadas em Machine Learning
- Visualizações interativas
- Relatórios personalizáveis
- Integração com dados externos
""")

# Estatísticas simuladas
st.markdown("### 📈 Estatísticas da Plataforma")
col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)

with col_stats1:
    st.metric("Projetos Ativos", "1,234", "12%")
with col_stats2:
    st.metric("Análises Realizadas", "5,678", "8%")
with col_stats3:
    st.metric("Usuários Registrados", "890", "15%")
with col_stats4:
    st.metric("Dados Processados (GB)", "2.3", "23%")

# Seção de resumo global (se houver dados do usuário)
if st.session_state.get('user_name'):
    st.divider()
    st.subheader("🌍 Seu Projeto Atual")
    
    col_global1, col_global2, col_global3 = st.columns(3)
    
    with col_global1:
        st.info(f"👤 **Usuário:** {st.session_state.user_name}")
        if st.session_state.get('project_name'):
            st.info(f"📋 **Projeto:** {st.session_state.project_name}")
    
    with col_global2:
        if st.session_state.get('selected_analysis'):
            st.info(f"🔬 **Análise Ativa:** {st.session_state.selected_analysis}")
        if st.session_state.data_uploaded:
            st.success("📊 **Dados:** Carregados")
        else:
            st.warning("📊 **Dados:** Não carregados")
    
    with col_global3:
        if st.session_state.get('theme'):
            st.info(f"🎨 **Tema:** {st.session_state.theme}")
        if st.session_state.get('notifications'):
            st.success("🔔 **Notificações:** Ativas")
        else:
            st.info("🔕 **Notificações:** Inativas")
else:
    st.divider()
    st.info("👋 **Primeira vez aqui?** Vá para a página **Home** para configurar suas informações!")

