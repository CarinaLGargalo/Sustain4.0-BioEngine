import streamlit as st  # type: ignore
import pandas as pd  # type: ignore
from pathlib import Path

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Sustain 4.0 - BioEngine",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Background customizado com opacidade de 40%
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

/* Garantir que o conteúdo aparece sobre o fundo */
[data-testid="stToolbar"] {
    z-index: 1;
}

/* Estilo para expander com fundo branco */
.stExpander {
    background-color: white !important;
    border-radius: 8px !important;
    border: 1px solid #e6e6e6 !important;
}

.stExpander > div > div {
    background-color: white !important;
}

.stExpander [data-testid="stExpanderHeader"] {
    background-color: white !important;
}

.stExpander [data-testid="stExpanderContent"] {
    background-color: white !important;
}
</style>
"""
st.markdown(page_bg__img, unsafe_allow_html=True)

# Importar funções do módulo utils
from utils import (  # type: ignore
    ensure_data_dir,
    ensure_path_within_data,
    save_user_data,
    check_authentication,
    init_session_state,
    auto_save_user_data,
    clear_app_session_state,
)

# Inicializar session state
init_session_state()

def login_page():
    """Displays the OIDC login page."""

    def _oidc_auth_configured():
        try:
            auth_config = st.secrets.get("auth", {})
            required_keys = ("redirect_uri", "cookie_secret", "client_id", "client_secret", "server_metadata_url")
            missing_keys = [key for key in required_keys if not auth_config.get(key)]
            return missing_keys == []
        except Exception:
            return False
    
    # Custom CSS to improve the login page visual
    st.markdown("""
    <style>

    /* Main title */
    .main-title {
        background: linear-gradient(135deg, #2c3e50, #27ae60, #3498db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        font-size: 3em !important;
        font-weight: 800 !important;
        margin-bottom: 30px !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    /* Messages */
    .stSuccess {
        background: linear-gradient(135deg, #2ecc71, #27ae60) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 15px 20px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(46, 204, 113, 0.3) !important;
    }

    .stError {
        background: linear-gradient(135deg, #e74c3c, #c0392b) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 15px 20px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3) !important;
    }

    .stInfo {
        background: linear-gradient(135deg, #3498db, #2980b9) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 15px 20px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3) !important;
    }

    /* Platform description */
    .platform-description {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 20px;
        margin-top: 30px;
        border-left: 4px solid #2ecc71;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        font-size: 1.1em;
        line-height: 1.6;
        color: #2c3e50;
    }

    /* Icons and emojis */
    .icon-enhancement {
        font-size: 1.2em;
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create layout with a central column
    col1, center_col, col3 = st.columns([1, 2, 1])
    
    # All content goes in the central column
    with center_col:
        # Main container with custom style
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Styled main title
        st.markdown(
            '<h1 class="main-title">🌿 Sustain4.0 BioEngine</h1>',
            unsafe_allow_html=True
        )
        
        st.markdown("### Login")
        st.info("Use your Google account to access Sustain4.0 BioEngine.")
        if not _oidc_auth_configured():
            st.error("Missing OIDC configuration. Add the five keys under [auth] in Streamlit Cloud Secrets or .streamlit/secrets.toml: redirect_uri, cookie_secret, client_id, client_secret, and server_metadata_url.")
            st.stop()

        if st.button("🔐 Continue with Google", type="primary", use_container_width=True):
            st.login()

        # Close main container
        st.markdown('</div>', unsafe_allow_html=True)

        # Styled platform description
        st.markdown("""
        <div class="platform-description">
            <h4>🌿 About Sustain4.0 BioEngine</h4>
            <p>Discover our next-generation, open-source software designed to make LCA for bioprocesses more powerful, accurate, and accessible. We are building this platform from the ground up in order to handle the unique complexities of bio-based systems and provide meaningful environmental sustainability insights. Key features include: </p>
            <ul>
                <li>🛠️ <strong>Open-Source & Specialized</strong> - A fully open-source platform specifically designed for conducting Life Cycle Assessments (LCA) of bioprocesses. </li>
                <li> 📈 <strong>Advanced & Dynamic Analysis</strong> - Our software is built for the future of process monitoring. It's designed to connect with online data ingestion pipelines and allows for soft sensor integration. This enables dynamic, near real-time LCA, moving your analysis beyond static, one-size-fits-all results. </li>
                <li>⚗️ <strong>Tackling Bioprocess Complexity</strong>
                  <ul>
                    <li>Bridging data gaps with built-in estimation tools.</li>
                    <li>Quantifying and handling uncertainty through sensitivity and Monte Carlo analyses.</li>
                  </ul>
                </li>
                <li>🌎 <strong>Sustainability within Planetary Boundaries</strong> - A key feature is the integration of Absolute Environmental Sustainability Assessment (AESA). This allows you to evaluate your bioprocess's performance not just relatively, but against the absolute carrying capacity of the Earth as defined by the Planetary Boundaries framework. </li>
                <li>📑 <strong>Interpretable plotting and Comprehensive Reporting</strong> - Easily export your findings into a detailed report (or plots), summarizing your methodology, data, and results for clear communication and documentation.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Check authentication before showing main content
if not check_authentication():
    login_page()
    st.stop()  # Stop execution here if not authenticated



# Main application content

# Auto-save user data

auto_save_user_data()

# Check if just logged in (only once)
current_time = pd.Timestamp.now()
login_time = st.session_state.get('login_time')

# Only show balloons if:
# 1. User logged in recently (in the last 6 seconds)
# 2. We haven't shown balloons yet
if login_time and (current_time - login_time).total_seconds() < 5:
    st.balloons()  # Celebration visual effect

# Here will be placed the header with the user name and logout button

colt1, colt2, colt3 = st.columns([7, 2, 1])

with colt1:
    st.subheader(f"🌿 Welcome, {st.session_state.get('user_name', '')}!")

with colt2:
    # Button to create new project
    if st.button("🧭 Create New Project", use_container_width=True):
        st.session_state.show_project_form = True

with colt3:
    # Logout button
    if st.button("Logout", use_container_width=True):
        # Save user data before logging out
        current_user_id = st.session_state.get('user_id')
        
        # Retrieve existing projects
        user_projects = st.session_state.user_projects.get(current_user_id, [])
        
        # Save user data before logging out
        user_data = {
            'projects': user_projects,
            'preferences': {
                'theme': st.session_state.theme,
                'notifications': st.session_state.notifications
            },
            'last_update': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            'logout_time': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save data
        if current_user_id:
            save_user_data(current_user_id, user_data)

        st.logout()
        clear_app_session_state()
        init_session_state()
        st.rerun()

st.markdown('---')

# # Create layout with two main columns
# main_col1, main_col2 = st.columns([1, 1])

# with main_col2:

# Initialize states for project creation
if 'show_project_form' not in st.session_state:
    st.session_state.show_project_form = False

# Initialize states for project deletion
if 'selected_project' not in st.session_state:
    st.session_state.selected_project = None
if 'deleting_project' not in st.session_state:
    st.session_state.deleting_project = None
if 'show_delete_confirm' not in st.session_state:
    st.session_state.show_delete_confirm = False

# Project creation form (if creating)
if st.session_state.show_project_form:
    st.subheader("New Project")
    st.write('Fill in the fields below to configure your new project.')
    
    # Initialize values in session_state if they don't exist
    if 'form_product_system' not in st.session_state:
        st.session_state.form_product_system = "Biofuels"
    if 'form_functional_unit_unit' not in st.session_state:
        st.session_state.form_functional_unit_unit = "L"
    if 'form_functional_unit_object' not in st.session_state:
        st.session_state.form_functional_unit_object = "biofuel"
    
    # Layout: Form on the left, dynamic fields on the right
    form_col, dynamic_col = st.columns([2, 1])
    
    with form_col:
        with st.form(key="new_project_form"):
            project_name = st.text_input("Project Name", placeholder="Enter a name for the project")
            goal_statement = st.text_input("Goal Statement", placeholder="Declare the objective of the study")
            intended_application = st.text_input("Intended Application", placeholder="Describe the intended application")
            
            col1, col2 = st.columns(2)
            with col1:
                level_of_detail = st.selectbox("Level of Detail", 
                                             ["Screening", "Streamlined", "Detailed"])
                type_of_lca = st.selectbox("Type of LCA study", 
                                         ["Prospective", "Traditional", "AESA"])
            with col2:
                methodology = st.selectbox("Methodology", 
                                         ["Attributional", "Consequential"])
                scale = st.selectbox("Scale", 
                                   ["lab", "pilot", "industrial"])
            
            # Reference Flow
            st.write("**Reference Flow**")
            ref_col1, ref_col2, ref_col3 = st.columns([1, 2, 2])
            with ref_col1:
                reference_flow = st.number_input("Amount", placeholder="ex: 1000", min_value=0, step=1)
            with ref_col2:
                reference_flow_unit = st.selectbox("Unit", ["kg", "L", "m³", "MJ"])
            with ref_col3:
                reference_flow_time_unit = st.selectbox("Time Unit", ["hour", "day", "month", "year"])

            system_boundaries = st.selectbox("System Boundaries", 
                                           ["gate-to-gate", "cradle-to-gate", "cradle-to-grave", "cradle-to-cradle"])
            
            # System Boundaries Figure upload (optional)
            system_boundaries_figure = st.file_uploader("System Boundaries Figure Upload (optional)", 
                                                       type=['png', 'jpg', 'jpeg', 'pdf'], 
                                                       help="Upload a figure illustrating the system boundaries")
            
            region = st.selectbox("Region", 
                                ["Brazil", "Portugal", "Denmark", "UK", "Germany", "USA", "New Zealand"])
            
            # Absolute Sustainability Study expander
            with st.expander("**Absolute Sustainability Study?**"):
                sharing_principle = st.selectbox("Sharing Principle", 
                                               ["Equal per Capita", "Grandfathering", "Economic Share", "Needs-Based"])
                reason_sharing_principle = st.text_input("Reason for Sharing Principle", 
                                                        placeholder="Explain the reason for the chosen sharing principle")
                
            submit_project = st.form_submit_button("Create", use_container_width=True)
    
    with dynamic_col:
        st.markdown("### Product Settings")
        
        # Product system outside the form to allow reactivity
        product_system = st.selectbox("Product/system to be studied", 
                                    ["Biofuels", "Food Products", "Building Materials", 
                                     "Electronics", "Chemicals", "Energy Systems"],
                                    key="form_product_system")
        
        # Functional Unit also outside the form to allow reactivity
        st.write("**Functional Unit**")
        
        # Unit options based on the product system
        unit_options_by_product = {
            "Biofuels": ["L", "MJ", "kg", "km"],
            "Food Products": ["kg", "meal", "kcal", "g"],
            "Building Materials": ["m²", "m³", "kg", "unit"],
            "Electronics": ["device", "year", "unit", "GB"],
            "Chemicals": ["kg", "mol", "L", "dose"],
            "Energy Systems": ["kWh", "MW", "year", "GJ"]
        }
        
        functional_unit_unit = st.selectbox("Unit", 
                                          unit_options_by_product.get(product_system, ["kg", "unit", "m²", "L"]),
                                          key="form_functional_unit_unit")
        
        # Object options based on the product system
        object_options_by_product = {
            "Biofuels": ["biofuel", "energy", "fuel", "driven"],
            "Food Products": ["product", "meal", "energy", "protein content"],
            "Building Materials": ["surface", "volume", "material", "functional unit area"],
            "Electronics": ["device", "use", "processing capacity", "storage capacity"],
            "Chemicals": ["chemical", "substance", "solution", "functional dose"],
            "Energy Systems": ["generated", "capacity", "operation", "energy"]
        }
        
        functional_unit_object = st.selectbox("Object", 
                                            object_options_by_product.get(product_system, ["product", "service", "material", "energy"]),
                                            key="form_functional_unit_object")
    
    # Process form submit
    if submit_project:
            if not project_name:
                st.error("Please enter at least the project name!")
            elif reference_flow <= 0:
                st.error("Please enter a valid value for the Reference Flow!")
            else:
                # Generate random 6-digit key code
                import random
                key_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                
                # Create new project in session
                current_user_id = st.session_state.get('user_id')
                if not current_user_id:
                    st.error("Could not determine authenticated user ID.")
                    st.stop()
                
                # Initialize user's project list if it doesn't exist yet
                if current_user_id not in st.session_state.user_projects:
                    st.session_state.user_projects[current_user_id] = []
                
                # Save figure if uploaded
                figure_path = None
                if system_boundaries_figure is not None:
                    # Create directory to save figures if it doesn't exist
                    figures_dir = ensure_path_within_data(ensure_data_dir() / "figures")
                    figures_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Save file with unique name
                    original_name = Path(system_boundaries_figure.name).name
                    safe_name = original_name.replace("..", "").replace("/", "_").replace("\\", "_")
                    figure_filename = f"{current_user_id}_{key_code}_{safe_name}"
                    figure_path = ensure_path_within_data(figures_dir / figure_filename)
                    
                    with open(figure_path, "wb") as f:
                        
                
                # Add the project to the user's list
                        f.write(system_boundaries_figure.getbuffer())
                
                # Add the project to the user's list
                new_project = {
                    'name': project_name,
                    'key_code': key_code,
                    'goal_statement': goal_statement,
                    'intended_application': intended_application,
                    'level_of_detail': level_of_detail,
                    'type_of_lca': type_of_lca,
                    'methodology': methodology,
                    'scale': scale,
                    'reference_flow': reference_flow,
                    'reference_flow_unit': reference_flow_unit,
                    'reference_flow_time_unit': reference_flow_time_unit,
                    'system_boundaries': system_boundaries,
                    'system_boundaries_figure': str(figure_path) if figure_path else None,
                    'product_system': st.session_state.form_product_system,
                    'functional_unit_unit': st.session_state.form_functional_unit_unit,
                    'functional_unit_object': st.session_state.form_functional_unit_object,
                    # Keep the old field for compatibility
                    'functional_unit': f"{st.session_state.form_functional_unit_unit} of {st.session_state.form_functional_unit_object}",
                    'region': region,
                    'sharing_principle': sharing_principle,
                    'reason_sharing_principle': reason_sharing_principle,
                    'created_at': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                st.session_state.user_projects[current_user_id].append(new_project)
                
                # Save user data
                user_data = {
                    'projects': st.session_state.user_projects[current_user_id],
                    'preferences': {
                        'theme': st.session_state.theme,
                        'notifications': st.session_state.notifications
                    },
                    'last_update': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                save_user_data(current_user_id, user_data)
                
                st.success(f"Project '{project_name}' created successfully! Code: {key_code}")
                st.session_state.show_project_form = False  # Close form after saving
                st.rerun()  # Reload page to show the new project


if not st.session_state.show_project_form:
    # Create layout with two main columns with separator: projects on the left, resume project on the right
    main_col1, separator_col, main_col2 = st.columns([2, 0.1, 2])

    with main_col1:
        st.subheader("My Projects")
        current_user_id = st.session_state.get('user_id')
        user_projects = st.session_state.user_projects.get(current_user_id, [])

        # Initialize state for selected project
        if 'selected_project' not in st.session_state:
            st.session_state.selected_project = None

        if not user_projects:
            st.info("You don't have any projects yet. Create one!")
        # CSS personalizado para melhorar o visual dos cards
        st.markdown("""
        <style>
        .project-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #dee2e6;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }
        .project-card:hover {
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }
        .project-title {
            color: #2c3e50;
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .project-type {
            color: #6c757d;
            font-size: 0.9em;
            margin-bottom: 4px;
        }
        .project-date {
            color: #6c757d;
            font-size: 0.9em;
            margin-bottom: 8px;
        }
        .project-description {
            color: #495057;
            font-size: 0.85em;
            font-style: italic;
            margin-top: 8px;
            padding: 8px;
            background-color: rgba(255,255,255,0.7);
            border-radius: 6px;
            border-left: 3px solid #28a745;
        }
        
        /* Resume Project Card */
        .resume-project-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #dee2e6;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        .resume-project-card:hover {
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }
        .resume-title {
            color: #2c3e50;
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .resume-project-name {
            color: #2c3e50;
            font-size: 1.1em;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .resume-project-info {
            color: #6c757d;
            font-size: 0.9em;
            margin-bottom: 6px;
        }
        .resume-project-description {
            color: #495057;
            font-size: 0.85em;
            font-style: italic;
            margin-top: 10px;
            padding: 10px;
            background-color: rgba(255,255,255,0.8);
            border-radius: 6px;
            border-left: 3px solid #28a745;
        }
        .resume-created-at {
            color: #6c757d;
            font-size: 0.8em;
            margin-top: 8px;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display projects in enhanced clickable cards
        for idx, project in enumerate(user_projects):
            with st.container():
                # Custom HTML for the card
                card_html = f"""
                <div class="project-card">
                    <div class="project-title">📁 {project['name']}</div>
                    <div class="project-type">🔑 <strong>Code:</strong> {project.get('key_code', 'N/A')}</div>
                    <div class="project-type">🎯 <strong>Goal:</strong> {project.get('goal_statement', project.get('description', 'N/A'))}</div>
                    <div class="project-type">🔬 <strong>LCA Type:</strong> {project.get('type_of_lca', project.get('type', 'N/A'))}</div>
                    <div class="project-date">📅 <strong>Created on:</strong> {project.get('created_at', 'N/A')}</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
                # Action buttons (removed edit button)
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    # Button to open project on analysis page
                    if st.button("✅ Start", key=f"open_project_{idx}", use_container_width=True):
                        # Save selected project in session state
                        st.session_state.selected_project = idx
                        st.session_state.current_project = user_projects[idx]
                        
                        # Save user data before navigating
                        user_data = {
                            'projects': st.session_state.user_projects[current_user_id],
                            'preferences': {
                                'theme': st.session_state.theme,
                                'notifications': st.session_state.notifications
                            },
                            'selected_project_index': idx,
                            'last_update': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        save_user_data(current_user_id, user_data)
                        
                        # Redirect to analysis page
                        st.switch_page("pages/01_📊_Projeto_em_Análise.py")
                        
                with col2:
                    # Button to delete project
                    if st.button("🗑️ Delete", key=f"delete_project_{idx}", use_container_width=True):
                        st.session_state.deleting_project = idx
                        st.session_state.show_delete_confirm = True
                        st.rerun()
                
                # Delete confirmation (if deleting this specific project)
                if (st.session_state.get('show_delete_confirm') and 
                    st.session_state.get('deleting_project') == idx):
                    
                    st.markdown("---")
                    st.warning(f"⚠️ Are you sure you want to delete the project '{project['name']}'?")
                    
                    confirm_col1, confirm_col2 = st.columns(2)
                    with confirm_col1:
                        if st.button("🗑️ Yes, Delete", type="primary", use_container_width=True, key=f"confirm_delete_{idx}"):
                            # Remove project
                            st.session_state.user_projects[current_user_id].pop(idx)
                            
                            # Adjust selected project index if necessary
                            if st.session_state.selected_project == idx:
                                st.session_state.selected_project = None
                            elif st.session_state.selected_project is not None and st.session_state.selected_project > idx:
                                st.session_state.selected_project -= 1
                            
                            # Save data
                            user_data = {
                                'projects': st.session_state.user_projects[current_user_id],
                                'preferences': {
                                    'theme': st.session_state.theme,
                                    'notifications': st.session_state.notifications
                                },
                                'last_update': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            save_user_data(current_user_id, user_data)
                            
                            st.success("Project deleted successfully!")
                            st.session_state.show_delete_confirm = False
                            st.session_state.deleting_project = None
                            st.rerun()
                    
                    with confirm_col2:
                        if st.button("❌ Cancel", use_container_width=True, key=f"cancel_delete_{idx}"):
                            st.session_state.show_delete_confirm = False
                            st.session_state.deleting_project = None
                            st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)  # Spacing between cards

    # Separator column with vertical line
    with separator_col:
        if st.session_state.selected_project is not None:    
            st.markdown("""
            <div style="
                display: flex;
                justify-content: center;
                align-items: center;
                height: 800px;
                width: 100%;
            ">
                <div style="
                    height: 600px;
                    border-left: 2px solid #e0e0e0;
                    opacity: 0.6;
                "></div>
            </div>
            """, unsafe_allow_html=True)

    with main_col2:
        # Show "Resume Project" only when there is a selected project
        if st.session_state.selected_project is not None:
            st.subheader("Recent")
            selected_idx = st.session_state.selected_project
            if selected_idx < len(user_projects):
                selected_project = user_projects[selected_idx]
                
                # Custom HTML for resume project card
                resume_card_html = f"""
                <div class="resume-project-card">
                    <div class="resume-project-name">📁 {selected_project['name']}</div>
                    <div class="resume-project-info">🔑 <strong>Code:</strong> {selected_project.get('key_code', 'N/A')}</div>
                    <div class="resume-project-info">🎯 <strong>Goal:</strong> {selected_project.get('goal_statement', selected_project.get('description', 'N/A'))}</div>
                    <div class="resume-project-info">🔬 <strong>LCA Type:</strong> {selected_project.get('type_of_lca', selected_project.get('type', 'N/A'))}</div>
                    <div class="resume-project-info">⚖️ <strong>Methodology:</strong> {selected_project.get('methodology', 'N/A')}</div>
                    <div class="resume-project-info">🌍 <strong>Region:</strong> {selected_project.get('region', 'N/A')}</div>
                    {f'<div class="resume-created-at">Created on: {selected_project["created_at"]}</div>' if selected_project.get('created_at') else ''}
                </div>
                """
                st.markdown(resume_card_html, unsafe_allow_html=True)
                
                # Centered action button
                if st.button("🔄️ Resume Project", use_container_width=True, key="analysis_active", type="secondary"):
                    # Open project on analysis page
                    st.session_state.current_project = selected_project
                    user_data = {
                        'projects': st.session_state.user_projects[current_user_id],
                        'preferences': {
                            'theme': st.session_state.theme,
                            'notifications': st.session_state.notifications
                        },
                        'selected_project_index': selected_idx,
                        'last_update': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    save_user_data(current_user_id, user_data)
                    st.switch_page("pages/01_📊_Projeto_em_Análise.py")