import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Home - Sustain 4.0",
    page_icon="🏠",
    layout="wide"
)

# Verificação de autenticação
if not st.session_state.get('authenticated', False):
    st.error("🔐 Acesso negado! Por favor, faça login na página principal.")
    st.stop()

# Inicializar session state (mesmo sistema da página principal)
def init_session_state():
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

# Informações do usuário na sidebar
st.sidebar.success(f"👋 **{st.session_state.get('username', 'Usuário')}**")
st.sidebar.markdown("---")

st.header("🏠 Bem-vindo ao Sustain 4.0 - BioEngine!")

# Seção de informações do usuário
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Informações do Usuário")
    st.session_state.user_name = st.text_input(
        "Nome do usuário:", 
        value=st.session_state.user_name,
        placeholder="Digite seu nome"
    )
    
    user_role = st.selectbox(
        "Função:",
        ["Pesquisador", "Analista", "Gestor Ambiental", "Estudante"],
        index=0 if 'user_role' not in st.session_state else ["Pesquisador", "Analista", "Gestor Ambiental", "Estudante"].index(st.session_state.get('user_role', 'Pesquisador'))
    )
    st.session_state.user_role = user_role
    
    user_organization = st.text_input(
        "Organização:",
        value=st.session_state.get('user_organization', ''),
        placeholder="Digite sua organização"
    )
    st.session_state.user_organization = user_organization

with col2:
    st.subheader("🎯 Projeto Atual")
    project_name = st.text_input(
        "Nome do Projeto:",
        value=st.session_state.get('project_name', ''),
        placeholder="Nome do seu projeto de sustentabilidade"
    )
    st.session_state.project_name = project_name
    
    project_location = st.selectbox(
        "Localização do Projeto:",
        ["Amazônia", "Mata Atlântica", "Cerrado", "Caatinga", "Pantanal", "Pampa", "Outro"],
        index=0 if 'project_location' not in st.session_state else ["Amazônia", "Mata Atlântica", "Cerrado", "Caatinga", "Pantanal", "Pampa", "Outro"].index(st.session_state.get('project_location', 'Amazônia'))
    )
    st.session_state.project_location = project_location
    
    project_duration = st.slider(
        "Duração do Projeto (meses):",
        min_value=1, max_value=60, 
        value=st.session_state.get('project_duration', 12)
    )
    st.session_state.project_duration = project_duration

# Resumo das informações
if st.session_state.user_name:
    st.success(f"👋 Olá, {st.session_state.user_name}! Suas informações foram salvas.")
    
    with st.expander("📊 Resumo das Informações Salvas"):
        st.write(f"**Nome:** {st.session_state.user_name}")
        st.write(f"**Função:** {st.session_state.user_role}")
        st.write(f"**Organização:** {st.session_state.user_organization}")
        st.write(f"**Projeto:** {st.session_state.project_name}")
        st.write(f"**Localização:** {st.session_state.project_location}")
        st.write(f"**Duração:** {st.session_state.project_duration} meses")

# Informações sobre navegação
st.divider()
st.info("""
**💡 Próximos Passos:**
- Vá para a página **Análise** para fazer upload de dados e executar análises
- Configure suas preferências na página **Configurações**
- Visualize resultados na página **Dashboard**
""")

# Seção de resumo global
st.divider()
st.subheader("🌍 Status Global do Projeto")

col_global1, col_global2, col_global3 = st.columns(3)

with col_global1:
    if st.session_state.get('user_name'):
        st.success(f"👤 **Usuário:** {st.session_state.user_name}")
    else:
        st.warning("👤 **Usuário:** Não configurado")
    
    if st.session_state.get('project_name'):
        st.success(f"📋 **Projeto:** {st.session_state.project_name}")
    else:
        st.warning("📋 **Projeto:** Não configurado")

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
