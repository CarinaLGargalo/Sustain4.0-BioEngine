import streamlit as st

# Configuração da página principal
st.set_page_config(
    page_title="Sustain 4.0 - BioEngine",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar session state global para manter dados entre páginas
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

# Página Principal - Boas-vindas
st.title("� Sustain 4.0 - BioEngine")
st.markdown("### Plataforma Integrada de Análise de Sustentabilidade")

# Instruções na sidebar
st.sidebar.success("👆 Selecione uma página acima para navegar.")
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

# Conteúdo principal da página de boas-vindas
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("https://via.placeholder.com/400x200/2E8B57/FFFFFF?text=Sustain+4.0+BioEngine", 
             caption="Sustain 4.0 - BioEngine", use_column_width=True)
    
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

