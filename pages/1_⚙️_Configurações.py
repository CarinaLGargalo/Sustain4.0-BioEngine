import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Configurações - Sustain 4.0",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state= "collapsed"
)

# Verificação de autenticação
if not st.session_state.get('authenticated', False):
    st.success("🔐Por favor, faça login na página principal.")
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

st.header("⚙️ Configurações do Sustain 4.0 - BioEngine")

# Verificar se acabou de fazer login
if st.session_state.get('login_time'):
    st.balloons()  # Efeito visual de celebração
