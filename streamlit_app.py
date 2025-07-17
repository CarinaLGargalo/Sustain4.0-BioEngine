import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from streamlit_option_menu import option_menu

# Configuração da página
st.set_page_config(layout="wide")
st.title('🌿Sustain 4.0 - BioEngine')

# Inicializar session state para manter dados entre abas
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

elif selected_tab == "Análise":
    st.header("📊 Página de Análise")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🔧 Configurações de Análise")
        
        # Tipo de análise
        analysis_type = st.selectbox(
            "Tipo de Análise:",
            ["Análise de Biodiversidade", "Análise de Carbono", "Análise de Água", "Análise de Solo"],
            index=["Análise de Biodiversidade", "Análise de Carbono", "Análise de Água", "Análise de Solo"].index(st.session_state.selected_analysis)
        )
        st.session_state.selected_analysis = analysis_type
        
        # Upload de dados
        uploaded_file = st.file_uploader(
            "Upload de dados (CSV):",
            type=['csv'],
            help="Faça upload de um arquivo CSV com seus dados"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.uploaded_data = df
                st.session_state.data_uploaded = True
                st.success(f"✅ Arquivo carregado! {len(df)} linhas e {len(df.columns)} colunas")
            except Exception as e:
                st.error(f"❌ Erro ao carregar arquivo: {e}")
        
        # Parâmetros do modelo
        st.subheader("⚙️ Parâmetros do Modelo")
        n_estimators = st.slider(
            "Número de Estimadores:",
            min_value=10, max_value=500,
            value=st.session_state.model_params['n_estimators']
        )
        
        max_depth = st.slider(
            "Profundidade Máxima:",
            min_value=1, max_value=50,
            value=st.session_state.model_params['max_depth']
        )
        
        st.session_state.model_params = {
            'n_estimators': n_estimators,
            'max_depth': max_depth
        }
        
        # Botão para executar análise
        if st.button("🚀 Executar Análise", type="primary"):
            if st.session_state.data_uploaded:
                st.session_state.analysis_executed = True
                st.success("✅ Análise executada com sucesso!")
            else:
                st.warning("⚠️ Por favor, faça upload de dados primeiro!")
    
    with col2:
        st.subheader("📈 Resultados da Análise")
        
        if st.session_state.get('analysis_executed', False) and st.session_state.data_uploaded:
            # Simular resultados da análise
            st.write(f"**Tipo de Análise:** {st.session_state.selected_analysis}")
            st.write(f"**Projeto:** {st.session_state.get('project_name', 'Não informado')}")
            st.write(f"**Localização:** {st.session_state.get('project_location', 'Não informado')}")
            
            # Gráfico simulado
            chart_data = pd.DataFrame(
                np.random.randn(20, 3),
                columns=['Variável A', 'Variável B', 'Variável C']
            )
            st.line_chart(chart_data)
            
            # Métricas simuladas
            col_metric1, col_metric2, col_metric3 = st.columns(3)
            with col_metric1:
                st.metric("Biodiversidade", "85%", "2.1%")
            with col_metric2:
                st.metric("Carbono (t)", "1,234", "-12")
            with col_metric3:
                st.metric("Qualidade", "92", "5.2")
                
        elif st.session_state.data_uploaded:
            st.info("📋 Dados carregados. Clique em 'Executar Análise' para ver os resultados.")
            
            # Preview dos dados
            if st.session_state.uploaded_data is not None:
                st.write("**Preview dos dados:**")
                st.dataframe(st.session_state.uploaded_data.head())
        else:
            st.info("📤 Faça upload de dados para começar a análise.")

elif selected_tab == "Configurações":
    st.header("⚙️ Configurações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎨 Preferências de Interface")
        
        # Tema
        theme = st.selectbox(
            "Tema:",
            ["Claro", "Escuro", "Automático"],
            index=["Claro", "Escuro", "Automático"].index(st.session_state.theme)
        )
        st.session_state.theme = theme
        
        # Notificações
        notifications = st.checkbox(
            "Receber notificações",
            value=st.session_state.notifications
        )
        st.session_state.notifications = notifications
        
        # Idioma
        language = st.selectbox(
            "Idioma:",
            ["Português", "English", "Español"],
            index=0 if 'language' not in st.session_state else ["Português", "English", "Español"].index(st.session_state.get('language', 'Português'))
        )
        st.session_state.language = language
        
        # Salvar configurações automáticas
        auto_save = st.checkbox(
            "Salvamento automático",
            value=st.session_state.get('auto_save', True)
        )
        st.session_state.auto_save = auto_save
    
    with col2:
        st.subheader("📊 Configurações de Análise Padrão")
        
        # Configurações de análise padrão
        default_analysis = st.selectbox(
            "Análise padrão:",
            ["Análise de Biodiversidade", "Análise de Carbono", "Análise de Água", "Análise de Solo"],
            index=["Análise de Biodiversidade", "Análise de Carbono", "Análise de Água", "Análise de Solo"].index(st.session_state.selected_analysis)
        )
        st.session_state.default_analysis = default_analysis
        
        # Configurações de export
        export_format = st.multiselect(
            "Formatos de export:",
            ["PDF", "CSV", "Excel", "JSON"],
            default=st.session_state.get('export_formats', ["PDF", "CSV"])
        )
        st.session_state.export_formats = export_format
        
        # Configurações de email
        email_reports = st.checkbox(
            "Receber relatórios por email",
            value=st.session_state.get('email_reports', False)
        )
        st.session_state.email_reports = email_reports
        
        if email_reports:
            email_address = st.text_input(
                "Email para relatórios:",
                value=st.session_state.get('email_address', ''),
                placeholder="seu.email@exemplo.com"
            )
            st.session_state.email_address = email_address
    
    st.subheader("💾 Gerenciamento de Dados")
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        if st.button("🗑️ Limpar Cache", help="Remove dados temporários"):
            # Manter apenas configurações essenciais
            keys_to_keep = ['user_name', 'theme', 'notifications', 'language']
            keys_to_remove = [key for key in st.session_state.keys() if key not in keys_to_keep]
            for key in keys_to_remove:
                del st.session_state[key]
            st.success("✅ Cache limpo!")
            st.rerun()
    
    with col4:
        if st.button("📤 Exportar Configurações"):
            config_data = {key: value for key, value in st.session_state.items()}
            st.download_button(
                label="💾 Download Configurações",
                data=str(config_data),
                file_name="config_sustain40.txt",
                mime="text/plain"
            )
    
    with col5:
        if st.button("🔄 Resetar Tudo"):
            st.session_state.clear()
            st.success("✅ Todas as configurações foram resetadas!")
            st.rerun()
    
    # Mostrar estado atual
    with st.expander("🔍 Estado Atual do Sistema"):
        st.json(dict(st.session_state))

# Seção de resumo global (visível em todas as abas)
st.divider()
st.subheader("🌍 Resumo Global do Projeto")

if st.session_state.get('user_name'):
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
    st.warning("👋 Bem-vindo! Vá para a aba 'Home' para configurar suas informações.")

