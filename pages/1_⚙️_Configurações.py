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
    st.info("🔐Por favor, faça login na página principal.")
    st.stop()

st.header("⚙️ Configurações")
