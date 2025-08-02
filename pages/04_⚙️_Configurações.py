import streamlit as st

# Configuração da página (DEVE ser o primeiro comando do Streamlit)
st.set_page_config(
    page_title="Configurações - Sustain 4.0",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Importar outras bibliotecas depois da configuração da página
import yaml
from yaml.loader import SafeLoader
import pandas as pd
import json
import os
from pathlib import Path
import sys

# Background customizado com opacidade de 30%
page_bg__img = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.4)),
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

# Adicionar diretório pai ao path para importar funções
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import save_user_data

# Verificação de autenticação
if not st.session_state.get('authenticated', False):
    st.info("🔐Por favor, faça login na página principal.")
    st.stop()

# Importar funções adicionais
from utils import load_config, save_config

st.header("Configurações")

# Carregar configuração atual
config = load_config()

# Criar abas para organizar as configurações
tab1, tab2, tab3, tab4 = st.tabs(["🔒 Conta", "📊 Visualização", "🔧 Sistema", "📱 Notificações"])

with tab1:
    st.subheader("Configurações de Conta")
    
    # Exibir informações do usuário atual (se houver)
    if 'username' in st.session_state:
        st.info(f"Usuário atual: {st.session_state['username']}")
        
        # Opção para alterar senha
        with st.expander("Alterar senha"):
            current_password = st.text_input("Senha atual", type="password")
            new_password = st.text_input("Nova senha", type="password")
            confirm_password = st.text_input("Confirmar nova senha", type="password")
            
            if st.button("Atualizar senha"):
                if new_password != confirm_password:
                    st.error("As senhas não correspondem.")
                elif len(new_password) < 6:
                    st.error("A senha deve ter pelo menos 6 caracteres.")
                else:
                    # Aqui você implementaria a lógica para verificar a senha atual
                    # e atualizar para a nova senha no config
                    st.success("Senha alterada com sucesso!")

    # Seção para gerenciar usuários (somente para administradores)
    with st.expander("Gerenciar Usuários (Admin)"):
        st.warning("Esta seção está disponível apenas para administradores.")
        # Aqui você poderia adicionar uma verificação se o usuário é admin
        # E então mostrar as opções de gerenciamento de usuários

with tab2:
    st.subheader("Configurações de Visualização")
    
    # Tema da interface
    theme_options = ["Claro", "Escuro", "Sistema"]
    selected_theme = st.selectbox(
        "Tema da interface", 
        options=theme_options,
        index=theme_options.index(config.get('theme', 'Sistema'))
    )
    
    # Visualização de dados
    st.subheader("Gráficos e Relatórios")
    
    # Tipo de gráfico padrão
    chart_types = ["Barras", "Linhas", "Dispersão", "Área", "Pizza"]
    default_chart = st.selectbox(
        "Tipo de gráfico padrão", 
        options=chart_types,
        index=chart_types.index(config.get('default_chart_type', 'Barras'))
    )
    
    # Paleta de cores
    color_palettes = ["Viridis", "Magma", "Plasma", "Inferno", "Cividis", "Sustentabilidade"]
    default_palette = st.selectbox(
        "Paleta de cores para gráficos", 
        options=color_palettes,
        index=color_palettes.index(config.get('color_palette', 'Sustentabilidade'))
    )
    
    # Densidade de dados
    data_density = st.slider(
        "Densidade de dados em gráficos", 
        min_value=50, 
        max_value=1000, 
        value=config.get('data_density', 500),
        step=50,
        help="Número máximo de pontos a exibir em gráficos detalhados. Valores menores melhoram o desempenho."
    )

with tab3:
    st.subheader("Configurações do Sistema")
    
    # Configuração do cache
    cache_options = ["1 hora", "3 horas", "6 horas", "12 horas", "1 dia", "Sempre"]
    cache_setting = st.selectbox(
        "Duração do cache de dados", 
        options=cache_options,
        index=cache_options.index(config.get('cache_duration', '1 hora'))
    )
    
    # Unidades de medida
    units_system = st.radio(
        "Sistema de unidades",
        options=["Métrico", "Imperial"],
        index=0 if config.get('units', 'Métrico') == 'Métrico' else 1
    )
    
    # Configurações de backup
    st.subheader("Backup de Dados")
    backup_frequency = st.selectbox(
        "Frequência de backup automático",
        options=["Desativado", "Diário", "Semanal", "Mensal"],
        index=["Desativado", "Diário", "Semanal", "Mensal"].index(config.get('backup_frequency', 'Semanal'))
    )
    
    backup_location = st.text_input(
        "Localização de backup",
        value=config.get('backup_location', './backups'),
        help="Pasta onde os backups serão armazenados"
    )
    
    if st.button("Fazer backup agora"):
        st.info("Iniciando backup manual...")
        # Aqui você implementaria a lógica de backup
        st.success("Backup concluído com sucesso!")

with tab4:
    st.subheader("Configurações de Notificações")
    
    # Ativar/desativar notificações
    notifications_enabled = st.toggle(
        "Ativar notificações",
        value=config.get('notifications_enabled', True)
    )
    
    if notifications_enabled:
        # Tipos de notificações
        notification_types = st.multiselect(
            "Tipos de notificações",
            options=["Alertas críticos", "Atualizações de dados", "Relatórios periódicos", "Novidades do sistema"],
            default=config.get('notification_types', ["Alertas críticos"]),
        )
        
        # Email para notificações
        email_notifications = st.toggle(
            "Receber notificações por email",
            value=config.get('email_notifications', False)
        )
        
        if email_notifications:
            notification_email = st.text_input(
                "Email para notificações",
                value=config.get('notification_email', '')
            )
            
            frequency_options = ["Tempo real", "Resumo diário", "Resumo semanal"]
            email_frequency = st.radio(
                "Frequência de emails",
                options=frequency_options,
                index=frequency_options.index(config.get('email_frequency', 'Resumo diário'))
            )

# Botão para salvar todas as configurações
if st.button("Salvar todas as configurações", type="primary"):
    # Atualizar valores de configuração
    # Tema
    config['theme'] = selected_theme
    st.session_state.theme = selected_theme
    
    # Visualização
    config['default_chart_type'] = default_chart
    config['color_palette'] = default_palette
    config['data_density'] = data_density
    
    # Sistema
    config['cache_duration'] = cache_setting
    config['units'] = units_system
    config['backup_frequency'] = backup_frequency
    config['backup_location'] = backup_location
    
    # Notificações
    config['notifications_enabled'] = notifications_enabled
    st.session_state.notifications = notifications_enabled
    if notifications_enabled and 'notification_types' in locals():
        config['notification_types'] = notification_types
    if 'email_notifications' in locals():
        config['email_notifications'] = email_notifications
        if email_notifications and 'notification_email' in locals():
            config['notification_email'] = notification_email
        if email_notifications and 'email_frequency' in locals():
            config['email_frequency'] = email_frequency
    
    # Salvar no arquivo de configuração global
    try:
        save_config(config)
    except Exception as e:
        st.error(f"Erro ao salvar configurações: {e}")
        
    # Salvar as preferências do usuário em seu arquivo próprio
    if st.session_state.get('username'):
        username = st.session_state.username
        
        # Recuperar os projetos existentes (se houver)
        user_projects = st.session_state.user_projects.get(username, [])
        
        # Montar o objeto de dados do usuário
        user_data = {
            'projects': user_projects,
            'preferences': {
                'theme': selected_theme,
                'notifications': notifications_enabled,
                'default_chart_type': default_chart,
                'color_palette': default_palette,
                'data_density': data_density,
                'units': units_system
            },
            'last_update': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Salvar dados do usuário
        try:
            save_user_data(username, user_data)
            st.success("Configurações pessoais salvas com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar configurações pessoais: {e}")

# Opção para restaurar padrões
if st.button("Restaurar configurações padrão"):
    if st.checkbox("Confirmar restauração de configurações padrão"):
        # Definir valores padrão
        default_config = {
            'theme': 'Sistema',
            'default_chart_type': 'Barras',
            'color_palette': 'Sustentabilidade',
            'data_density': 500,
            'cache_duration': '1 hora',
            'units': 'Métrico',
            'backup_frequency': 'Semanal',
            'backup_location': './backups',
            'notifications_enabled': True,
            'notification_types': ["Alertas críticos"],
            'email_notifications': False
        }
        
        # Manter credenciais e configurações de cookie
        if 'credentials' in config:
            default_config['credentials'] = config['credentials']
        if 'cookie' in config:
            default_config['cookie'] = config['cookie']
        if 'preauthorized' in config:
            default_config['preauthorized'] = config['preauthorized']
        
        # Salvar
        try:
            save_config(default_config)
            st.experimental_rerun()  # Recarregar a página
        except Exception as e:
            st.error(f"Erro ao restaurar configurações: {e}")
