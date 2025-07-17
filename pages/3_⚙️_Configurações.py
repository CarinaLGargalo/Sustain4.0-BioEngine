import streamlit as st
import json

# Configuração da página
st.set_page_config(
    page_title="Configurações - Sustain 4.0",
    page_icon="⚙️",
    layout="wide"
)

# Inicializar session state
def init_session_state():
    if 'notifications' not in st.session_state:
        st.session_state.notifications = True
    if 'theme' not in st.session_state:
        st.session_state.theme = "Claro"
    if 'selected_analysis' not in st.session_state:
        st.session_state.selected_analysis = "Análise de Biodiversidade"

init_session_state()

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
    
    # Configurações de exibição
    st.subheader("📱 Configurações de Exibição")
    
    show_sidebar = st.checkbox(
        "Mostrar sidebar por padrão",
        value=st.session_state.get('show_sidebar', True)
    )
    st.session_state.show_sidebar = show_sidebar
    
    items_per_page = st.slider(
        "Itens por página:",
        min_value=5, max_value=50,
        value=st.session_state.get('items_per_page', 20)
    )
    st.session_state.items_per_page = items_per_page

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
    
    # Configurações de qualidade
    st.subheader("🎯 Configurações de Qualidade")
    
    min_samples = st.number_input(
        "Número mínimo de amostras:",
        min_value=10, max_value=1000,
        value=st.session_state.get('min_samples', 50)
    )
    st.session_state.min_samples = min_samples
    
    confidence_level = st.slider(
        "Nível de confiança (%):",
        min_value=80, max_value=99,
        value=st.session_state.get('confidence_level', 95)
    )
    st.session_state.confidence_level = confidence_level
    
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
        
        email_frequency = st.selectbox(
            "Frequência dos relatórios:",
            ["Diário", "Semanal", "Mensal"],
            index=st.session_state.get('email_frequency_index', 1)
        )
        st.session_state.email_frequency = email_frequency
        st.session_state.email_frequency_index = ["Diário", "Semanal", "Mensal"].index(email_frequency)

# Configurações Avançadas
st.divider()
st.subheader("🔧 Configurações Avançadas")

col3, col4 = st.columns(2)

with col3:
    st.write("**🤖 Configurações de Machine Learning**")
    
    default_algorithm = st.selectbox(
        "Algoritmo padrão:",
        ["Random Forest", "Gradient Boosting", "SVM", "Neural Network"],
        index=st.session_state.get('default_algorithm_index', 0)
    )
    st.session_state.default_algorithm = default_algorithm
    st.session_state.default_algorithm_index = ["Random Forest", "Gradient Boosting", "SVM", "Neural Network"].index(default_algorithm)
    
    cross_validation = st.checkbox(
        "Usar validação cruzada",
        value=st.session_state.get('cross_validation', True)
    )
    st.session_state.cross_validation = cross_validation
    
    if cross_validation:
        cv_folds = st.slider(
            "Número de folds:",
            min_value=3, max_value=10,
            value=st.session_state.get('cv_folds', 5)
        )
        st.session_state.cv_folds = cv_folds

with col4:
    st.write("**💾 Configurações de Dados**")
    
    cache_size = st.slider(
        "Tamanho do cache (MB):",
        min_value=100, max_value=2000,
        value=st.session_state.get('cache_size', 500)
    )
    st.session_state.cache_size = cache_size
    
    auto_backup = st.checkbox(
        "Backup automático",
        value=st.session_state.get('auto_backup', True)
    )
    st.session_state.auto_backup = auto_backup
    
    if auto_backup:
        backup_frequency = st.selectbox(
            "Frequência do backup:",
            ["A cada análise", "Diário", "Semanal"],
            index=st.session_state.get('backup_frequency_index', 0)
        )
        st.session_state.backup_frequency = backup_frequency
        st.session_state.backup_frequency_index = ["A cada análise", "Diário", "Semanal"].index(backup_frequency)

# Gerenciamento de Dados
st.divider()
st.subheader("💾 Gerenciamento de Dados")

col5, col6, col7 = st.columns(3)

with col5:
    if st.button("🗑️ Limpar Cache", help="Remove dados temporários"):
        # Manter apenas configurações essenciais
        keys_to_keep = ['user_name', 'theme', 'notifications', 'language']
        keys_to_remove = [key for key in st.session_state.keys() if key not in keys_to_keep]
        for key in keys_to_remove:
            del st.session_state[key]
        st.success("✅ Cache limpo!")
        st.rerun()

with col6:
    if st.button("📤 Exportar Configurações"):
        config_data = {key: value for key, value in st.session_state.items() if not callable(value)}
        config_json = json.dumps(config_data, indent=2, default=str)
        st.download_button(
            label="💾 Download Configurações",
            data=config_json,
            file_name="config_sustain40.json",
            mime="application/json"
        )

with col7:
    if st.button("🔄 Resetar Tudo"):
        st.session_state.clear()
        st.success("✅ Todas as configurações foram resetadas!")
        st.rerun()

# Import de configurações
st.divider()
st.subheader("📥 Importar Configurações")

uploaded_config = st.file_uploader(
    "Carregar arquivo de configurações:",
    type=['json'],
    help="Importe um arquivo JSON com configurações salvas anteriormente"
)

if uploaded_config is not None:
    try:
        config_data = json.load(uploaded_config)
        
        col_import1, col_import2 = st.columns(2)
        
        with col_import1:
            st.write("**📋 Configurações no arquivo:**")
            st.json(config_data)
        
        with col_import2:
            if st.button("✅ Aplicar Configurações", type="primary"):
                # Aplicar configurações importadas
                for key, value in config_data.items():
                    st.session_state[key] = value
                st.success("✅ Configurações importadas com sucesso!")
                st.rerun()
    except Exception as e:
        st.error(f"❌ Erro ao importar configurações: {e}")

# Mostrar estado atual
st.divider()
st.subheader("🔍 Estado Atual do Sistema")

with st.expander("Ver todas as configurações"):
    # Filtrar apenas configurações (não dados temporários)
    config_keys = [key for key in st.session_state.keys() 
                   if not key.startswith('uploaded_') and 
                   not key.startswith('analysis_') and
                   key != 'uploaded_data']
    
    config_display = {key: st.session_state[key] for key in config_keys}
    st.json(config_display)

# Informações sobre o sistema
st.divider()
st.subheader("ℹ️ Informações do Sistema")

col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.metric("Configurações Ativas", len([k for k in st.session_state.keys() if not k.startswith('uploaded_')]))

with col_info2:
    if st.session_state.get('data_uploaded'):
        st.metric("Status dos Dados", "Carregados", "✅")
    else:
        st.metric("Status dos Dados", "Não carregados", "⚠️")

with col_info3:
    if st.session_state.get('user_name'):
        st.metric("Usuário Configurado", "Sim", "✅")
    else:
        st.metric("Usuário Configurado", "Não", "⚠️")

# Footer com dicas
st.divider()
st.markdown("""
**💡 Dicas de Configuração:**
- **Tema Escuro**: Melhor para uso noturno ou ambientes com pouca luz
- **Salvamento Automático**: Recomendado para evitar perda de dados
- **Validação Cruzada**: Melhora a confiabilidade dos modelos
- **Backup Automático**: Protege contra perda acidental de dados
""")

# Status do usuário
if st.session_state.get('user_name'):
    st.success(f"👤 Configurações do usuário: **{st.session_state.user_name}**")
    if st.session_state.get('project_name'):
        st.info(f"📋 Projeto ativo: **{st.session_state.project_name}**")
