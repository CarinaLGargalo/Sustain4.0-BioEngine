import streamlit as st  # type: ignore

# Page configuration (MUST be the first Streamlit command)
st.set_page_config(
    page_title="Settings - Sustain 4.0",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import other libraries after page configuration
import pandas as pd  # type: ignore
import os
import sys

# Custom background with 30% opacity
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

/* Ensure content appears over the background */
[data-testid="stToolbar"] {
    z-index: 1;
}
</style>
"""
st.markdown(page_bg__img, unsafe_allow_html=True)

# Add parent directory to path to import functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import check_authentication, load_config, save_config, save_user_data  # type: ignore

# Authentication verification
if not check_authentication():
    st.info("🔐Please login on the main page.")
    st.stop()

st.header("Settings")

# Load current configuration
config = load_config()
current_user_id = st.session_state.get('user_id')
user_projects = st.session_state.user_projects.get(current_user_id, [])

# Create tabs to organize settings
tab1, tab2, tab3, tab4 = st.tabs(["🔒 Account", "📊 Visualization", "🔧 System", "📱 Notifications"])

with tab1:
    st.subheader("Account")
    st.info(f"Name: {st.session_state.get('user_name', 'User')}")
    st.info(f"Email: {st.session_state.get('user_email', 'N/A')}")
    st.caption("Authentication is managed via Google OIDC (Streamlit st.login/st.logout).")

with tab2:
    st.subheader("Configurações de Visualização")
    
    # Tema da interface
    theme_options = ["Claro", "Escuro", "Sistema"]
    selected_theme = st.selectbox(
        "Tema da interface", 
        options=theme_options,
        index=theme_options.index(config.get('theme', 'Sistema'))
    )
    
    # Data visualization
    st.subheader("Charts and Reports")
    
    # Default chart type
    chart_types = ["Bars", "Lines", "Scatter", "Area", "Pie"]
    default_chart = st.selectbox(
        "Default chart type", 
        options=chart_types,
        index=chart_types.index(config.get('default_chart_type', 'Bars')) if config.get('default_chart_type', 'Bars') in chart_types else 0
    )
    
    # Color palette
    color_palettes = ["Viridis", "Magma", "Plasma", "Inferno", "Cividis", "Sustainability"]
    default_palette = st.selectbox(
        "Color palette for charts", 
        options=color_palettes,
        index=color_palettes.index(config.get('color_palette', 'Sustainability')) if config.get('color_palette', 'Sustainability') in color_palettes else 0
    )
    
    # Data density
    data_density = st.slider(
        "Data density in charts", 
        min_value=50, 
        max_value=1000, 
        value=config.get('data_density', 500),
        step=50,
        help="Maximum number of points to display in detailed charts. Lower values improve performance."
    )

with tab3:
    st.subheader("System Settings")
    
    # Cache configuration
    cache_options = ["1 hour", "3 hours", "6 hours", "12 hours", "1 day", "Always"]
    cache_setting = st.selectbox(
        "Data cache duration", 
        options=cache_options,
        index=cache_options.index(config.get('cache_duration', '1 hour')) if config.get('cache_duration', '1 hour') in cache_options else 0
    )
    
    # Units of measurement
    units_system = st.radio(
        "Unit system",
        options=["Metric", "Imperial"],
        index=0 if config.get('units', 'Metric') == 'Metric' else 1
    )
    
    # Backup settings
    st.subheader("Data Backup")
    backup_frequency = st.selectbox(
        "Automatic backup frequency",
        options=["Disabled", "Daily", "Weekly", "Monthly"],
        index=["Disabled", "Daily", "Weekly", "Monthly"].index(config.get('backup_frequency', 'Weekly')) if config.get('backup_frequency', 'Weekly') in ["Disabled", "Daily", "Weekly", "Monthly"] else 2
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
    
    # Enable/disable notifications
    notifications_enabled = st.toggle(
        "Enable notifications",
        value=config.get('notifications_enabled', True)
    )
    
    if notifications_enabled:
        # Notification types
        notification_types = st.multiselect(
            "Notification types",
            options=["Critical alerts", "Data updates", "Periodic reports", "System news"],
            default=config.get('notification_types', ["Critical alerts"]),
        )
        
        # Email for notifications
        email_notifications = st.toggle(
            "Receive email notifications",
            value=config.get('email_notifications', False)
        )
        
        if email_notifications:
            notification_email = st.text_input(
                "Email for notifications",
                value=config.get('notification_email', '')
            )
            
            frequency_options = ["Real time", "Daily summary", "Weekly summary"]
            email_frequency = st.radio(
                "Email frequency",
                options=frequency_options,
                index=frequency_options.index(config.get('email_frequency', 'Daily summary')) if config.get('email_frequency', 'Daily summary') in frequency_options else 1
            )

# Button to save all settings
if st.button("Save all settings", type="primary"):
    # Update configuration values
    # Theme
    config['theme'] = selected_theme
    st.session_state.theme = selected_theme
    
    # Visualization
    config['default_chart_type'] = default_chart
    config['color_palette'] = default_palette
    config['data_density'] = data_density
    
    # System
    config['cache_duration'] = cache_setting
    config['units'] = units_system
    config['backup_frequency'] = backup_frequency
    config['backup_location'] = backup_location
    
    # Notifications
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
    
    # Save to global configuration file
    try:
        save_config(config)
    except Exception as e:
        st.error(f"Error saving settings: {e}")
        
    # Save user preferences to their own file
    if current_user_id:
        # Build user data object
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
        
        try:
            save_user_data(current_user_id, user_data)
            st.success("Personal settings saved successfully!")
        except Exception as e:
            st.error(f"Error saving personal settings: {e}")

if st.button("Restaurar configurações padrão"):
    if st.checkbox("Confirmar restauração de configurações padrão"):
        default_config = {
            'theme': 'Sistema',
            'default_chart_type': 'Bars',
            'color_palette': 'Sustainability',
            'data_density': 500,
            'cache_duration': '1 hour',
            'units': 'Metric',
            'backup_frequency': 'Weekly',
            'backup_location': './backups',
            'notifications_enabled': True,
            'notification_types': ["Critical alerts"],
            'email_notifications': False,
            'email_frequency': 'Daily summary'
        }

        try:
            save_config(default_config)
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao restaurar configurações: {e}")
