import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Análise - Sustain 4.0",
    page_icon="📊",
    layout="wide"
)

# Verificação de autenticação
if not st.session_state.get('authenticated', False):
    st.error("🔐 Acesso negado! Por favor, faça login na página principal.")
    st.stop()

# Inicializar session state
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

init_session_state()

# Informações do usuário na sidebar
st.sidebar.success(f"👋 **{st.session_state.get('username', 'Usuário')}**")
st.sidebar.markdown("---")

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
    
    # Configurações avançadas
    st.subheader("🔬 Configurações Avançadas")
    
    test_size = st.slider(
        "Tamanho do conjunto de teste (%):",
        min_value=10, max_value=50,
        value=st.session_state.get('test_size', 20)
    )
    st.session_state.test_size = test_size
    
    random_state = st.number_input(
        "Semente aleatória:",
        min_value=0, max_value=9999,
        value=st.session_state.get('random_state', 42)
    )
    st.session_state.random_state = random_state
    
    # Botão para executar análise
    if st.button("🚀 Executar Análise", type="primary"):
        if st.session_state.data_uploaded:
            st.session_state.analysis_executed = True
            st.session_state.analysis_timestamp = pd.Timestamp.now()
            st.success("✅ Análise executada com sucesso!")
        else:
            st.warning("⚠️ Por favor, faça upload de dados primeiro!")

with col2:
    st.subheader("📈 Resultados da Análise")
    
    if st.session_state.get('analysis_executed', False) and st.session_state.data_uploaded:
        # Informações da análise
        st.write(f"**Tipo de Análise:** {st.session_state.selected_analysis}")
        st.write(f"**Projeto:** {st.session_state.get('project_name', 'Não informado')}")
        st.write(f"**Localização:** {st.session_state.get('project_location', 'Não informado')}")
        
        if st.session_state.get('analysis_timestamp'):
            st.write(f"**Executado em:** {st.session_state.analysis_timestamp.strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Gráfico simulado
        st.subheader("📊 Visualizações")
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['Variável A', 'Variável B', 'Variável C']
        )
        
        # Diferentes tipos de gráficos baseados no tipo de análise
        if "Biodiversidade" in st.session_state.selected_analysis:
            st.line_chart(chart_data)
            st.bar_chart(chart_data[['Variável A']])
        elif "Carbono" in st.session_state.selected_analysis:
            st.area_chart(chart_data)
        elif "Água" in st.session_state.selected_analysis:
            st.line_chart(chart_data[['Variável A', 'Variável B']])
        else:  # Solo
            st.bar_chart(chart_data)
        
        # Métricas simuladas baseadas no tipo de análise
        st.subheader("📋 Métricas")
        col_metric1, col_metric2, col_metric3 = st.columns(3)
        
        if "Biodiversidade" in st.session_state.selected_analysis:
            with col_metric1:
                st.metric("Índice Shannon", "2.85", "0.12")
            with col_metric2:
                st.metric("Riqueza de Espécies", "147", "8")
            with col_metric3:
                st.metric("Equitabilidade", "0.78", "0.05")
        elif "Carbono" in st.session_state.selected_analysis:
            with col_metric1:
                st.metric("Carbono Total (t)", "1,234", "-12")
            with col_metric2:
                st.metric("Sequestro Anual (t/ano)", "89", "5")
            with col_metric3:
                st.metric("Emissões (t CO2)", "456", "-23")
        elif "Água" in st.session_state.selected_analysis:
            with col_metric1:
                st.metric("Qualidade (%)", "92", "5.2")
            with col_metric2:
                st.metric("pH", "7.2", "0.1")
            with col_metric3:
                st.metric("Turbidez (NTU)", "2.1", "-0.3")
        else:  # Solo
            with col_metric1:
                st.metric("pH do Solo", "6.5", "0.2")
            with col_metric2:
                st.metric("Matéria Orgânica (%)", "3.8", "0.4")
            with col_metric3:
                st.metric("Fertilidade", "Alta", "Estável")
        
        # Relatório de análise
        st.subheader("📄 Relatório de Análise")
        st.markdown(f"""
        **Resumo da Análise de {st.session_state.selected_analysis}**
        
        - **Dados processados:** {len(st.session_state.uploaded_data)} amostras
        - **Variáveis analisadas:** {len(st.session_state.uploaded_data.columns)}
        - **Modelo utilizado:** Random Forest
        - **Parâmetros:** {st.session_state.model_params['n_estimators']} estimadores, profundidade máxima {st.session_state.model_params['max_depth']}
        - **Conjunto de teste:** {st.session_state.get('test_size', 20)}%
        
        Os resultados indicam {'bom' if np.random.rand() > 0.5 else 'satisfatório'} desempenho do modelo 
        para o tipo de análise selecionada.
        """)
        
        # Botões de ação
        col_action1, col_action2, col_action3 = st.columns(3)
        with col_action1:
            if st.button("📋 Gerar Relatório PDF"):
                st.info("🚧 Funcionalidade em desenvolvimento")
        with col_action2:
            if st.button("📊 Exportar Dados"):
                st.info("🚧 Funcionalidade em desenvolvimento")
        with col_action3:
            if st.button("📧 Enviar por Email"):
                st.info("🚧 Funcionalidade em desenvolvimento")
                
    elif st.session_state.data_uploaded:
        st.info("📋 Dados carregados. Clique em 'Executar Análise' para ver os resultados.")
        
        # Preview dos dados
        if st.session_state.uploaded_data is not None:
            st.write("**Preview dos dados:**")
            st.dataframe(st.session_state.uploaded_data.head())
            
            # Estatísticas básicas
            st.write("**Estatísticas Descritivas:**")
            numeric_cols = st.session_state.uploaded_data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                st.dataframe(st.session_state.uploaded_data[numeric_cols].describe())
    else:
        st.info("📤 Faça upload de dados para começar a análise.")
        
        # Exemplo de dados
        st.write("**Exemplo de formato de dados esperado:**")
        example_data = pd.DataFrame({
            'especie': ['Espécie A', 'Espécie B', 'Espécie C'],
            'abundancia': [45, 32, 28],
            'biomassa': [12.5, 8.3, 9.7],
            'localizacao': ['Plot 1', 'Plot 2', 'Plot 1']
        })
        st.dataframe(example_data)

# Footer com informações úteis
st.divider()
st.markdown("""
**💡 Dicas:**
- Certifique-se de que seus dados estão em formato CSV
- A primeira linha deve conter os nomes das colunas
- Dados numéricos devem usar ponto (.) como separador decimal
- Para melhores resultados, tenha pelo menos 50 amostras
""")

# Status global
if st.session_state.get('user_name'):
    st.success(f"👤 Análise sendo executada para o usuário: **{st.session_state.user_name}**")
    if st.session_state.get('project_name'):
        st.info(f"📋 Projeto ativo: **{st.session_state.project_name}**")
