import streamlit as st
import pandas as pd
import json
import os
import yaml
from yaml.loader import SafeLoader
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import base64
import io

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

# Function to generate PDF report for project
def generate_project_pdf(project_data, project_name):
    """Generate a PDF report with project information"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=15,
        textColor=colors.darkgreen
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    normal_style.spaceAfter = 6
    
    # Title
    story.append(Paragraph(f"Project Report: {project_name}", title_style))
    story.append(Spacer(1, 12))
    
    # Generated timestamp
    generated_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(f"<i>Generated on: {generated_time}</i>", normal_style))
    story.append(Spacer(1, 20))
    
    # Project Information Section
    story.append(Paragraph("Project Information", heading_style))
    
    # Create data for basic information table
    basic_info = [
        ['Project Code', project_data.get('key_code', 'N/A')],
        ['Goal Statement', project_data.get('goal_statement', project_data.get('description', 'N/A'))],
        ['Intended Application', project_data.get('intended_application', 'N/A')],
        ['Type of LCA Study', project_data.get('type_of_lca', project_data.get('type', 'N/A'))],
        ['Methodology', project_data.get('methodology', 'N/A')],
        ['Scale', project_data.get('scale', 'N/A')],
        ['Level of Detail', project_data.get('level_of_detail', 'N/A')],
        ['Product/System', project_data.get('product_system', 'N/A')],
        ['System Boundaries', project_data.get('system_boundaries', 'N/A')],
        ['Region', project_data.get('region', 'N/A')]
    ]
    
    # Format Reference Flow
    ref_flow = project_data.get('reference_flow', 'N/A')
    ref_unit = project_data.get('reference_flow_unit', '')
    ref_time = project_data.get('reference_flow_time_unit') or project_data.get('reference_flow_description', '')
    if ref_flow != 'N/A' and ref_unit and ref_time:
        reference_flow_display = f"{ref_flow} {ref_unit}/{ref_time}"
    else:
        reference_flow_display = str(ref_flow)
    basic_info.append(['Reference Flow', reference_flow_display])
    
    # Format Functional Unit
    functional_unit_unit = project_data.get('functional_unit_unit')
    functional_unit_object = project_data.get('functional_unit_object')
    if functional_unit_unit and functional_unit_object:
        functional_unit_display = f"{functional_unit_unit} of {functional_unit_object}"
    else:
        functional_unit_display = project_data.get('functional_unit', 'N/A')
    basic_info.append(['Functional Unit', functional_unit_display])
    
    # Create table for basic information
    basic_table = Table(basic_info, colWidths=[2*inch, 4*inch])
    basic_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    story.append(basic_table)
    story.append(Spacer(1, 20))
    
    # Absolute Sustainability Section (if applicable)
    if project_data.get('sharing_principle') and project_data.get('reason_sharing_principle'):
        story.append(Paragraph("Absolute Sustainability Study", heading_style))
        
        abs_sustainability_info = [
            ['Absolute Sustainability Study', 'Yes'],
            ['Sharing Principle', project_data.get('sharing_principle', 'N/A')],
            ['Reason for Sharing Principle', project_data.get('reason_sharing_principle', 'N/A')]
        ]
        
        abs_table = Table(abs_sustainability_info, colWidths=[2*inch, 4*inch])
        abs_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        story.append(abs_table)
        story.append(Spacer(1, 20))
    
    # LCI Status Section
    story.append(Paragraph("Life Cycle Inventory (LCI) Status", heading_style))
    
    # Check if LCI was started
    project_key = project_data.get('key_code', project_data['name'])
    lci_initiated = st.session_state.get('lci_started', {}).get(project_key, False)
    has_lci_data = project_data.get('lci_data') is not None
    
    lci_status = "Not Started"
    if has_lci_data:
        lci_status = "Completed - Data Available"
    elif lci_initiated:
        # Check user level if available
        user_level = st.session_state.get('user_lci_level', {}).get(project_key, 0)
        level_descriptions = {
            0: "Level 0 - Process identification needed",
            1: "Level 1 - Data collection needed", 
            2: "Level 2 - Partial data available",
            3: "Level 3 - Ready for data input"
        }
        lci_status = f"In Progress - {level_descriptions.get(user_level, 'Unknown level')}"
    
    story.append(Paragraph(f"<b>Current LCI Status:</b> {lci_status}", normal_style))
    story.append(Spacer(1, 12))
    
    # Timestamps
    story.append(Paragraph("Project Timeline", heading_style))
    timeline_info = [
        ['Created', project_data.get('created_at', 'N/A')],
        ['Last Updated', project_data.get('updated_at', 'N/A')]
    ]
    
    timeline_table = Table(timeline_info, colWidths=[2*inch, 4*inch])
    timeline_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    story.append(timeline_table)
    story.append(Spacer(1, 30))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    story.append(Paragraph("Generated by Sustain 4.0 BioEngine", footer_style))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
