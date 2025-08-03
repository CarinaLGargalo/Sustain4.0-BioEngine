import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import os
import streamlit as st
import pandas as pd
import time
import bcrypt
from pathlib import Path

# Configuração da página - DEVE ser o primeiro comando Streamlit
st.set_page_config(
    page_title="Sustain 4.0 - BioEngine",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Background customizado com opacidade de 40%
page_bg__img = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.25)),
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
    
    # CSS personalizado para melhorar o visual da página de login
    st.markdown("""
    <style>
    
    /* Título principal */
    .main-title {
        background: linear-gradient(135deg, #2c3e50, #27ae60, #3498db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        font-size: 3em !important;
        font-weight: 800 !important;
        margin-bottom: 30px !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Estilo das abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background: rgba(255,255,255,0.8);
        border-radius: 15px;
        padding: 5px;
        margin-bottom: 30px;
        display: flex;
        width: 100%;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 15px 25px;
        background: transparent;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        flex: 1;
        text-align: center;
        width: 50%;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3498db, #2ecc71) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
    }
    
    /* Formulários */
    .stForm {
        background: rgba(248, 249, 250, 0.9);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(222, 226, 230, 0.5);
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {
        border-radius: 10px !important;
        border: 2px solid #e9ecef !important;
        padding: 12px 15px !important;
        transition: all 0.3s ease !important;
        background: rgba(255,255,255,0.9) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #3498db !important;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1) !important;
    }
    
    /* Botões */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 12px 25px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Botão primário */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3498db, #2ecc71) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4) !important;
    }
    
    /* Botão demo */
    .stButton > button:not([kind="primary"]) {
        background: linear-gradient(135deg, #95a5a6, #7f8c8d) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(149, 165, 166, 0.3) !important;
    }
    
    /* Mensagens */
    .stSuccess {
        background: linear-gradient(135deg, #2ecc71, #27ae60) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 15px 20px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(46, 204, 113, 0.3) !important;
    }
    
    .stError {
        background: linear-gradient(135deg, #e74c3c, #c0392b) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 15px 20px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3) !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #3498db, #2980b9) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 15px 20px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3) !important;
    }
    
    /* Descrição da plataforma */
    .platform-description {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 20px;
        margin-top: 30px;
        border-left: 4px solid #2ecc71;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        font-size: 1.1em;
        line-height: 1.6;
        color: #2c3e50;
    }
    
    /* Ícones e emojis */
    .icon-enhancement {
        font-size: 1.2em;
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Criar layout com uma coluna central
    col1, center_col, col3 = st.columns([1, 2, 1])
    
    # Todo o conteúdo vai na coluna central
    with center_col:
        # Container principal com estilo personalizado
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Título principal estilizado
        st.markdown(
            '<h1 class="main-title">🌿 Sustain4.0 BioEngine</h1>',
            unsafe_allow_html=True
        )
        
        # Criar abas para Login e Registro
        tab1, tab2 = st.tabs(["Login", "Cadastro"])
        
        with tab1:
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
        
        # Botão Demo (acesso rápido) com estilo aprimorado
        st.markdown("---")
        st.markdown("### 🎯 Acesso Rápido")
        if st.button("👁️ Demo - Explorar Plataforma", use_container_width=True):
            st.session_state.authenticated = True
            st.session_state.username = "demo"
            st.session_state.user_name = "Demo User"
            st.session_state.login_time = pd.Timestamp.now()
            st.session_state.balloons_shown = False  # Resetar a flag para permitir mostrar os balões
            
            # Carregar dados do usuário demo
            load_user_data_on_login("demo")
            
            st.rerun()  # Recarrega a página para mostrar o conteúdo principal
    
        with tab2:
            st.markdown("### Criar nova conta")
            
            # Formulário customizado de registro
            with st.form("register_form"):
                col_reg1, col_reg2 = st.columns(2)
                
                with col_reg1:
                    new_name = st.text_input("👤 Nome Completo:", placeholder="Digite seu nome completo")
                    new_username = st.text_input("🔑 Username:", placeholder="Escolha um nome de usuário único")
                
                with col_reg2:
                    new_email = st.text_input("📧 Email:", placeholder="Digite seu email")
                    
                new_password = st.text_input("🔒 Senha:", type="password", placeholder="Digite uma senha segura")
                new_password_repeat = st.text_input("🔒 Confirmar Senha:", type="password", placeholder="Digite a senha novamente")
            
                submit_button = st.form_submit_button("🎉 Criar Conta", type="primary", use_container_width=True)
                
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

        # Fechar container principal
        st.markdown('</div>', unsafe_allow_html=True)

        # Descrição da plataforma estilizada
        st.markdown("""
        <div class="platform-description">
            <h4>🌍 Sobre a Plataforma</h4>
            <p><strong>Sustain4.0 BioEngine</strong> é uma plataforma integrada de análise de sustentabilidade ambiental. 
            Oferecemos uma interface intuitiva para pesquisadores e analistas ambientais, permitindo:</p>
            <ul>
                <li>🌿 <strong>Análises de biodiversidade</strong> - Monitoramento da vida selvagem</li>
                <li>🌱 <strong>Monitoramento de carbono</strong> - Rastreamento de emissões</li>
                <li>💧 <strong>Qualidade da água</strong> - Análise de recursos hídricos</li>
                <li>🌱 <strong>Saúde do solo</strong> - Avaliação da fertilidade</li>
            </ul>
            <p>Transforme dados ambientais em insights acionáveis para um futuro mais sustentável! 🚀</p>
        </div>
        """, unsafe_allow_html=True)

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
if login_time and (current_time - login_time).total_seconds() < 5:
    st.balloons()  # Efeito visual de celebração

# Aqui será colocado o cabeçalho com o nome do usuário e o botão de logout

colt1, colt2, colt3 = st.columns([7, 2, 1])

with colt1:
    st.subheader(f"🌿 Bem-vindo, {st.session_state.get('user_name', '')}!")

with colt2:
    # Botão para criar novo projeto
    if st.button("🧭 Criar Novo Projeto", use_container_width=True):
        st.session_state.show_project_form = True

with colt3:
    # Botão de logout
    if st.button("Logout", use_container_width=True):
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

# Inicializar estados para edição e exclusão de projetos
if 'selected_project' not in st.session_state:
    st.session_state.selected_project = None
if 'editing_project' not in st.session_state:
    st.session_state.editing_project = None
if 'show_edit_form' not in st.session_state:
    st.session_state.show_edit_form = False
if 'deleting_project' not in st.session_state:
    st.session_state.deleting_project = None
if 'show_delete_confirm' not in st.session_state:
    st.session_state.show_delete_confirm = False

# Formulário de criação de projeto (se estiver criando)
if st.session_state.show_project_form:
    st.subheader("Novo Projeto")
    st.write('Preencha os campos abaixo para configurar o seu novo projeto.')
    with st.form(key="new_project_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Project Name", placeholder="Digite um nome para o projeto")
            goal_statement = st.text_input("Goal Statement", placeholder="Declare o objetivo do estudo")
            intended_application = st.text_input("Intended Application", placeholder="Descreva a aplicação pretendida")
            level_of_detail = st.selectbox("Level of Detail", 
                                         ["Screening", "Streamlined", "Detailed"])
            type_of_lca = st.selectbox("Type of LCA study", 
                                     ["Prospective", "Traditional", "AESA"])
            methodology = st.selectbox("Methodology", 
                                     ["Attributional", "Consequential"])
            scale = st.selectbox("Scale", 
                               ["lab", "pilot", "industrial"])
            reference_flow = st.text_input("Reference Flow", placeholder="Defina o fluxo de referência")
            system_boundaries = st.selectbox("System Boundaries", 
                                           ["gate-to-gate", "cradle-to-gate", "cradle-to-grave", "cradle-to-cradle"])
            
        with col2:
            # Upload de figura para System Boundaries (opcional)
            system_boundaries_figure = st.file_uploader("System Boundaries Figure Upload (opcional)", 
                                                       type=['png', 'jpg', 'jpeg', 'pdf'], 
                                                       help="Faça upload de uma figura ilustrando as fronteiras do sistema")
            
            product_system = st.selectbox("Product/system to be studied", 
                                        ["Option A - Biofuels", "Option B - Food Products", "Option C - Building Materials", 
                                         "Option D - Electronics", "Option E - Chemicals", "Option F - Energy Systems"])
            
            # Functional Unit baseado no Product/system selecionado
            functional_unit_options = {
                "Option A - Biofuels": ["L of biofuel", "MJ of energy", "kg of fuel", "km driven"],
                "Option B - Food Products": ["kg of product", "1 meal", "kcal of energy", "protein content (g)"],
                "Option C - Building Materials": ["m² of surface", "m³ of volume", "kg of material", "functional unit area"],
                "Option D - Electronics": ["1 device", "year of use", "processing capacity", "storage capacity (GB)"],
                "Option E - Chemicals": ["kg of chemical", "mol of substance", "L of solution", "functional dose"],
                "Option F - Energy Systems": ["kWh generated", "MW capacity", "year of operation", "GJ of energy"]
            }
            
            functional_unit = st.selectbox("Functional Unit", 
                                         functional_unit_options.get(product_system, ["kg", "unit", "m²", "L"]))
            
            region = st.selectbox("Region", 
                                ["Brazil", "Portugal", "Denmark", "UK", "Germany", "USA", "New Zealand"])
            
        # Absolute Sustainability Study expander
        with st.expander("Absolute Sustainability Study?"):
            sharing_principle = st.selectbox("Sharing Principle", 
                                           ["Equal per Capita", "Grandfathering", "Economic Share", "Needs-Based"])
            reason_sharing_principle = st.text_input("Reason for Sharing Principle", 
                                                    placeholder="Explique a razão para o princípio de compartilhamento escolhido")
            
        submit_project = st.form_submit_button("Create", use_container_width=True)
        
        if submit_project:
            if not project_name:
                st.error("Por favor, informe pelo menos o nome do projeto!")
            else:
                # Gerar key code aleatório de 6 dígitos
                import random
                key_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                
                # Criar novo projeto na session
                username = st.session_state.username
                
                # Inicializar a lista de projetos do usuário se ainda não existir
                if username not in st.session_state.user_projects:
                    st.session_state.user_projects[username] = []
                
                # Salvar figura se foi feito upload
                figure_path = None
                if system_boundaries_figure is not None:
                    # Criar diretório para salvar figuras se não existir
                    figures_dir = Path("data/figures")
                    figures_dir.mkdir(exist_ok=True)
                    
                    # Salvar arquivo com nome único
                    figure_filename = f"{username}_{key_code}_{system_boundaries_figure.name}"
                    figure_path = figures_dir / figure_filename
                    
                    with open(figure_path, "wb") as f:
                        f.write(system_boundaries_figure.getbuffer())
                
                # Adicionar o projeto à lista do usuário
                new_project = {
                    'name': project_name,
                    'key_code': key_code,
                    'goal_statement': goal_statement,
                    'intended_application': intended_application,
                    'level_of_detail': level_of_detail,
                    'type_of_lca': type_of_lca,
                    'methodology': methodology,
                    'scale': scale,
                    'reference_flow': reference_flow,
                    'system_boundaries': system_boundaries,
                    'system_boundaries_figure': str(figure_path) if figure_path else None,
                    'product_system': product_system,
                    'functional_unit': functional_unit,
                    'region': region,
                    'sharing_principle': sharing_principle,
                    'reason_sharing_principle': reason_sharing_principle,
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
                
                st.success(f"Projeto '{project_name}' criado com sucesso! Código: {key_code}")
                st.session_state.show_project_form = False  # Fechar formulário após salvar
                st.rerun()  # Recarregar a página para mostrar o novo projeto


if not st.session_state.show_project_form:
    # Criar layout com duas colunas principais com separador: projetos à esquerda, retomar projeto à direita
    main_col1, separator_col, main_col2 = st.columns([2, 0.1, 2])

    with main_col1:
        st.subheader("Meus Projetos")
        username = st.session_state.username
        user_projects = st.session_state.user_projects.get(username, [])

        # Inicializar estado para projeto selecionado
        if 'selected_project' not in st.session_state:
            st.session_state.selected_project = None

        if not user_projects:
            st.info("Você ainda não tem projetos. Crie um!")
        # CSS personalizado para melhorar o visual dos cards
        st.markdown("""
        <style>
        .project-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #dee2e6;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }
        .project-card:hover {
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }
        .project-title {
            color: #2c3e50;
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .project-type {
            color: #6c757d;
            font-size: 0.9em;
            margin-bottom: 4px;
        }
        .project-date {
            color: #6c757d;
            font-size: 0.9em;
            margin-bottom: 8px;
        }
        .project-description {
            color: #495057;
            font-size: 0.85em;
            font-style: italic;
            margin-top: 8px;
            padding: 8px;
            background-color: rgba(255,255,255,0.7);
            border-radius: 6px;
            border-left: 3px solid #28a745;
        }
        
        /* Card Retomar Projeto */
        .resume-project-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #dee2e6;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        .resume-project-card:hover {
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }
        .resume-title {
            color: #2c3e50;
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .resume-project-name {
            color: #2c3e50;
            font-size: 1.1em;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .resume-project-info {
            color: #6c757d;
            font-size: 0.9em;
            margin-bottom: 6px;
        }
        .resume-project-description {
            color: #495057;
            font-size: 0.85em;
            font-style: italic;
            margin-top: 10px;
            padding: 10px;
            background-color: rgba(255,255,255,0.8);
            border-radius: 6px;
            border-left: 3px solid #28a745;
        }
        .resume-created-at {
            color: #6c757d;
            font-size: 0.8em;
            margin-top: 8px;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Exibir projetos em cards clicáveis aprimorados
        for idx, project in enumerate(user_projects):
            with st.container():
                # HTML personalizado para o card
                card_html = f"""
                <div class="project-card">
                    <div class="project-title">📁 {project['name']}</div>
                    <div class="project-type">🔑 <strong>Código:</strong> {project.get('key_code', 'N/A')}</div>
                    <div class="project-type">🎯 <strong>Goal:</strong> {project.get('goal_statement', project.get('description', 'N/A'))}</div>
                    <div class="project-type">🔬 <strong>LCA Type:</strong> {project.get('type_of_lca', project.get('type', 'N/A'))}</div>
                    <div class="project-date">📅 <strong>Criado em:</strong> {project.get('created_at', 'N/A')}</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
                # Botões de ação (mantendo a funcionalidade original)
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    # Botão para abrir o projeto na página de análise
                    if st.button("✅ Iniciar", key=f"open_project_{idx}", use_container_width=True):
                        # Salvar projeto selecionado no session state
                        st.session_state.selected_project = idx
                        st.session_state.current_project = user_projects[idx]
                        
                        # Salvar dados do usuário antes de navegar
                        user_data = {
                            'projects': st.session_state.user_projects[username],
                            'preferences': {
                                'theme': st.session_state.theme,
                                'notifications': st.session_state.notifications
                            },
                            'selected_project_index': idx,
                            'last_update': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        save_user_data(username, user_data)
                        
                        # Redirecionar para a página de análise
                        st.switch_page("pages/01_📊_Projeto_em_Análise.py")
                        
                with col2:
                    # Botão para editar o projeto
                    if st.button("✏️ Editar", key=f"edit_project_{idx}", use_container_width=True):
                        st.session_state.editing_project = idx
                        st.session_state.show_edit_form = True
                        
                with col3:
                    # Botão para deletar o projeto
                    if st.button("🗑️ Excluir", key=f"delete_project_{idx}", use_container_width=True):
                        st.session_state.deleting_project = idx
                        st.session_state.show_delete_confirm = True
                
                st.markdown("<br>", unsafe_allow_html=True)  # Espaçamento entre cards

    # Coluna separadora com linha vertical
    with separator_col:
        if st.session_state.selected_project is not None:    
            st.markdown("""
            <div style="
                display: flex;
                justify-content: center;
                align-items: center;
                height: 800px;
                width: 100%;
            ">
                <div style="
                    height: 600px;
                    border-left: 2px solid #e0e0e0;
                    opacity: 0.6;
                "></div>
            </div>
            """, unsafe_allow_html=True)

    with main_col2:
        # Mostrar "Retomar Projeto" apenas quando houver um projeto selecionado
        if st.session_state.selected_project is not None:
            st.subheader("Recentes")
            selected_idx = st.session_state.selected_project
            if selected_idx < len(user_projects):
                selected_project = user_projects[selected_idx]
                
                # HTML personalizado para o card de retomar projeto
                resume_card_html = f"""
                <div class="resume-project-card">
                    <div class="resume-project-name">📁 {selected_project['name']}</div>
                    <div class="resume-project-info">🔑 <strong>Código:</strong> {selected_project.get('key_code', 'N/A')}</div>
                    <div class="resume-project-info">🎯 <strong>Goal:</strong> {selected_project.get('goal_statement', selected_project.get('description', 'N/A'))}</div>
                    <div class="resume-project-info">🔬 <strong>LCA Type:</strong> {selected_project.get('type_of_lca', selected_project.get('type', 'N/A'))}</div>
                    <div class="resume-project-info">⚖️ <strong>Methodology:</strong> {selected_project.get('methodology', 'N/A')}</div>
                    <div class="resume-project-info">🌍 <strong>Region:</strong> {selected_project.get('region', 'N/A')}</div>
                    {f'<div class="resume-created-at">Criado em: {selected_project["created_at"]}</div>' if selected_project.get('created_at') else ''}
                </div>
                """
                st.markdown(resume_card_html, unsafe_allow_html=True)
                
                # Botão de ação centralizado
                if st.button("🔄️ Retomar Projeto", use_container_width=True, key="analysis_active", type="secondary"):
                    # Abrir projeto na página de análise
                    st.session_state.current_project = selected_project
                    user_data = {
                        'projects': st.session_state.user_projects[username],
                        'preferences': {
                            'theme': st.session_state.theme,
                            'notifications': st.session_state.notifications
                        },
                        'selected_project_index': selected_idx,
                        'last_update': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    save_user_data(username, user_data)
                    st.switch_page("pages/01_📊_Projeto_em_Análise.py")
        
        # Formulário de edição (se estiver editando)
        if st.session_state.get('show_edit_form') and st.session_state.get('editing_project') is not None:
            editing_idx = st.session_state.editing_project
            if editing_idx < len(user_projects):
                project_to_edit = user_projects[editing_idx]
                
                st.markdown("---")
                st.markdown("### ✏️ Editar Projeto")
                with st.form(key="edit_project_form"):
                    # Campos básicos
                    edit_name = st.text_input("Project Name", value=project_to_edit['name'])
                    edit_goal = st.text_input("Goal Statement", value=project_to_edit.get('goal_statement', project_to_edit.get('description', '')))
                    edit_application = st.text_input("Intended Application", value=project_to_edit.get('intended_application', ''))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        edit_level = st.selectbox("Level of Detail", 
                                                ["Screening", "Streamlined", "Detailed"],
                                                index=["Screening", "Streamlined", "Detailed"].index(project_to_edit.get('level_of_detail', 'Screening')))
                        edit_lca_type = st.selectbox("Type of LCA study", 
                                                   ["Prospective", "Traditional", "AESA"],
                                                   index=["Prospective", "Traditional", "AESA"].index(project_to_edit.get('type_of_lca', project_to_edit.get('type', 'Traditional'))))
                        edit_methodology = st.selectbox("Methodology", 
                                                       ["Attributional", "Consequential"],
                                                       index=["Attributional", "Consequential"].index(project_to_edit.get('methodology', 'Attributional')))
                        edit_scale = st.selectbox("Scale", 
                                                 ["lab", "pilot", "industrial"],
                                                 index=["lab", "pilot", "industrial"].index(project_to_edit.get('scale', 'lab')))
                    with col2:
                        edit_reference_flow = st.text_input("Reference Flow", value=project_to_edit.get('reference_flow', ''))
                        edit_boundaries = st.selectbox("System Boundaries", 
                                                      ["gate-to-gate", "cradle-to-gate", "cradle-to-grave", "cradle-to-cradle"],
                                                      index=["gate-to-gate", "cradle-to-gate", "cradle-to-grave", "cradle-to-cradle"].index(project_to_edit.get('system_boundaries', 'gate-to-gate')))
                        edit_product = st.selectbox("Product/system to be studied", 
                                                   ["Option A - Biofuels", "Option B - Food Products", "Option C - Building Materials", 
                                                    "Option D - Electronics", "Option E - Chemicals", "Option F - Energy Systems"],
                                                   index=["Option A - Biofuels", "Option B - Food Products", "Option C - Building Materials", 
                                                          "Option D - Electronics", "Option E - Chemicals", "Option F - Energy Systems"].index(project_to_edit.get('product_system', 'Option A - Biofuels')))
                        edit_region = st.selectbox("Region", 
                                                  ["Brazil", "Portugal", "Denmark", "UK", "Germany", "USA", "New Zealand"],
                                                  index=["Brazil", "Portugal", "Denmark", "UK", "Germany", "USA", "New Zealand"].index(project_to_edit.get('region', 'Brazil')))
                    
                    # Functional Unit baseado no Product/system selecionado
                    functional_unit_options = {
                        "Option A - Biofuels": ["L of biofuel", "MJ of energy", "kg of fuel", "km driven"],
                        "Option B - Food Products": ["kg of product", "1 meal", "kcal of energy", "protein content (g)"],
                        "Option C - Building Materials": ["m² of surface", "m³ of volume", "kg of material", "functional unit area"],
                        "Option D - Electronics": ["1 device", "year of use", "processing capacity", "storage capacity (GB)"],
                        "Option E - Chemicals": ["kg of chemical", "mol of substance", "L of solution", "functional dose"],
                        "Option F - Energy Systems": ["kWh generated", "MW capacity", "year of operation", "GJ of energy"]
                    }
                    
                    current_functional_unit = project_to_edit.get('functional_unit', 'kg of product')
                    available_units = functional_unit_options.get(edit_product, ["kg", "unit", "m²", "L"])
                    if current_functional_unit not in available_units:
                        current_functional_unit = available_units[0]
                    
                    edit_functional_unit = st.selectbox("Functional Unit", 
                                                       available_units,
                                                       index=available_units.index(current_functional_unit))
                    
                    # Absolute Sustainability Study
                    with st.expander("Absolute Sustainability Study?"):
                        edit_sharing = st.selectbox("Sharing Principle", 
                                                   ["Equal per Capita", "Grandfathering", "Economic Share", "Needs-Based"],
                                                   index=["Equal per Capita", "Grandfathering", "Economic Share", "Needs-Based"].index(project_to_edit.get('sharing_principle', 'Equal per Capita')))
                        edit_reason_sharing = st.text_input("Reason for Sharing Principle", 
                                                           value=project_to_edit.get('reason_sharing_principle', ''))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("💾 Salvar", use_container_width=True):
                            # Atualizar projeto
                            st.session_state.user_projects[username][editing_idx] = {
                                'name': edit_name,
                                'key_code': project_to_edit.get('key_code', '000000'),  # Manter código existente
                                'goal_statement': edit_goal,
                                'intended_application': edit_application,
                                'level_of_detail': edit_level,
                                'type_of_lca': edit_lca_type,
                                'methodology': edit_methodology,
                                'scale': edit_scale,
                                'reference_flow': edit_reference_flow,
                                'system_boundaries': edit_boundaries,
                                'system_boundaries_figure': project_to_edit.get('system_boundaries_figure'),  # Manter figura existente
                                'product_system': edit_product,
                                'functional_unit': edit_functional_unit,
                                'region': edit_region,
                                'sharing_principle': edit_sharing,
                                'reason_sharing_principle': edit_reason_sharing,
                                'created_at': project_to_edit.get('created_at', pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")),
                                'updated_at': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            
                            # Salvar dados
                            user_data = {
                                'projects': st.session_state.user_projects[username],
                                'preferences': {
                                    'theme': st.session_state.theme,
                                    'notifications': st.session_state.notifications
                                },
                                'last_update': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            save_user_data(username, user_data)
                            
                            st.success("Projeto atualizado com sucesso!")
                            st.session_state.show_edit_form = False
                            st.session_state.editing_project = None
                            st.rerun()
                    
                    with col2:
                        if st.form_submit_button("❌ Cancelar", use_container_width=True):
                            st.session_state.show_edit_form = False
                            st.session_state.editing_project = None
                            st.rerun()

        # Confirmação de exclusão (se estiver excluindo)
        if st.session_state.get('show_delete_confirm') and st.session_state.get('deleting_project') is not None:
            deleting_idx = st.session_state.deleting_project
            if deleting_idx < len(user_projects):
                project_to_delete = user_projects[deleting_idx]
                
                st.markdown("---")
                st.warning(f"⚠️ Tem certeza que deseja excluir o projeto '{project_to_delete['name']}'?")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ Sim, Excluir", type="primary", use_container_width=True, key="confirm_delete_sidebar"):
                        # Remover projeto
                        st.session_state.user_projects[username].pop(deleting_idx)
                        
                        # Ajustar índice do projeto selecionado se necessário
                        if st.session_state.selected_project == deleting_idx:
                            st.session_state.selected_project = None
                        elif st.session_state.selected_project is not None and st.session_state.selected_project > deleting_idx:
                            st.session_state.selected_project -= 1
                        
                        # Salvar dados
                        user_data = {
                            'projects': st.session_state.user_projects[username],
                            'preferences': {
                                'theme': st.session_state.theme,
                                'notifications': st.session_state.notifications
                            },
                            'last_update': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        save_user_data(username, user_data)
                        
                        st.success("Projeto excluído com sucesso!")
                        st.session_state.show_delete_confirm = False
                        st.session_state.deleting_project = None
                        st.rerun()
                
                with col2:
                    if st.button("❌ Cancelar", use_container_width=True, key="cancel_delete_sidebar"):
                        st.session_state.show_delete_confirm = False
                        st.session_state.deleting_project = None
                        st.rerun()