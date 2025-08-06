import streamlit as st
import pandas as pd
import json
import os
import yaml
from yaml.loader import SafeLoader
from pathlib import Path

# Function to check authentication
def check_authentication():
    """Checks if user is authenticated"""
    return st.session_state.get('authenticated', False)

# Create data directory if it doesn't exist
def ensure_data_dir():
    """Ensures that the data directory exists"""
    data_dir = Path("./data")
    if not data_dir.exists():
        data_dir.mkdir()
    return data_dir

# Function to save user data
def save_user_data(username, data):
    """Saves user data to a JSON file"""
    data_dir = ensure_data_dir()
    user_file = data_dir / f"{username}.json"
    
    with open(user_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, default=str, ensure_ascii=False, indent=2)
        
# Function to load user data
def load_user_data(username):
    """Loads user data from a JSON file"""
    data_dir = ensure_data_dir()
    user_file = data_dir / f"{username}.json"
    
    if user_file.exists():
        try:
            with open(user_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading user data: {e}")
            return {}
    else:
        return {}

# Function to load configuration
@st.cache_data
def load_config():
    """Loads user configuration from YAML file"""
    try:
        with open('config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)
        return config
    except FileNotFoundError:
        # Default configuration if file doesn't exist
        return {
            'credentials': {'usernames': {}},
            'cookie': {
                'expiry_days': 30,
                'key': 'sustain40_bioengine_key',
                'name': 'sustain40_cookie'
            },
            'preauthorized': {'emails': []}
        }

# Function to save configuration
def save_config(config):
    """Saves user configuration to YAML file"""
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

# Initialize session state
def init_session_state():
    """Initializes session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    if 'notifications' not in st.session_state:
        st.session_state.notifications = True
    if 'theme' not in st.session_state:
        st.session_state.theme = "Light"
    if 'user_projects' not in st.session_state:
        st.session_state.user_projects = {}  # Dictionary to store projects by username
    if 'last_save_time' not in st.session_state:
        st.session_state.last_save_time = pd.Timestamp.now()

# Function to load user data when logging in
def load_user_data_on_login(username):
    """Loads user data and updates session_state"""
    user_data = load_user_data(username)
    
    # Load projects
    if 'projects' in user_data:
        st.session_state.user_projects[username] = user_data['projects']
    
    # Load previously selected project (if it exists)
    if 'selected_project_index' in user_data:
        projects = st.session_state.user_projects.get(username, [])
        selected_idx = user_data['selected_project_index']
        if 0 <= selected_idx < len(projects):
            st.session_state.selected_project = selected_idx
            st.session_state.current_project = projects[selected_idx]
    
    # Load personal settings
    if 'preferences' in user_data:
        preferences = user_data['preferences']
        if 'theme' in preferences:
            st.session_state.theme = preferences['theme']
        if 'notifications' in preferences:
            st.session_state.notifications = preferences['notifications']
    
    # Load other custom information
    if 'custom_data' in user_data:
        st.session_state.custom_data = user_data['custom_data']

# Function to auto-save user data
def auto_save_user_data():
    """Auto-save user data every 5 minutes"""
    if not st.session_state.get('username'):
        return
        
    current_time = pd.Timestamp.now()
    last_save = st.session_state.get('last_save_time', pd.Timestamp.now())
    
    # Check if at least 5 minutes have passed since the last save
    if (current_time - last_save).total_seconds() >= 300:  # 300 seconds = 5 minutes
        username = st.session_state.username
        
        # Retrieve existing projects
        user_projects = st.session_state.user_projects.get(username, [])
        
        # Data to be saved
        user_data = {
            'projects': user_projects,
            'preferences': {
                'theme': st.session_state.theme,
                'notifications': st.session_state.notifications
            },
            'last_update': current_time.strftime("%Y-%m-%d %H:%M:%S"),
            'auto_saved': True
        }
        
        # Save user data
        save_user_data(username, user_data)
        st.session_state.last_save_time = current_time
