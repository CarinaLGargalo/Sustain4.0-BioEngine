import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Home - Sustain 4.0",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state= "collapsed"
)

# Verificação de autenticação
if not st.session_state.get('authenticated', False):
    st.error("🔐 Acesso negado! Por favor, faça login na página principal.")
    st.stop()

# Inicializar session state (mesmo sistema da página principal)
def init_session_state():
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    if 'notifications' not in st.session_state:
        st.session_state.notifications = True
    if 'theme' not in st.session_state:
        st.session_state.theme = "Claro"

init_session_state()

st.header("🏠 Bem-vindo ao Sustain 4.0 - BioEngine!")

# Verificar se acabou de fazer login
if st.session_state.get('login_time'):
    login_time = st.session_state.login_time
    import datetime
    # Se o login foi feito há menos de 30 segundos, mostrar mensagem de boas-vindas
    if (datetime.datetime.now() - login_time.to_pydatetime()).total_seconds() < 30:
        st.success(f"🎉 Bem-vindo, **{st.session_state.username}**! Você foi direcionado para a página inicial após o login.")
        st.balloons()  # Efeito visual de celebração

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
- Configure todas as suas informações pessoais e do projeto nesta página
- Volte para a página principal para visualizar o resumo geral da plataforma
- Use o botão de logout na barra lateral quando terminar
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
    if st.session_state.get('project_location'):
        st.info(f"� **Localização:** {st.session_state.project_location}")
    
    if st.session_state.get('user_role'):
        st.info(f"👨‍� **Função:** {st.session_state.user_role}")

with col_global3:
    if st.session_state.get('theme'):
        st.info(f"🎨 **Tema:** {st.session_state.theme}")
    
    if st.session_state.get('notifications'):
        st.success("🔔 **Notificações:** Ativas")
    else:
        st.info("🔕 **Notificações:** Inativas")
