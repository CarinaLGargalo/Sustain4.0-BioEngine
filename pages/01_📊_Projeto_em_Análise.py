import streamlit as st

# Page configuration (MUST be the first Streamlit command)
st.set_page_config(
    page_title="Project Analysis - Sustain 4.0",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import other libraries after page configuration
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

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

/* Style for expander with white background */
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

# Import functions from utilities module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import check_authentication

# Authentication verification
if not st.session_state.get('authenticated', False):
    st.info("🔐 Please login on the main page.")
    st.stop()

# Check if there are available projects
username = st.session_state.username
user_projects = st.session_state.user_projects.get(username, [])

if not user_projects:
    st.warning("You don't have any projects yet. Create a project on the main page.")
    st.stop()

# Check if there is a pre-selected project from the main page
selected_project = None
selected_project_name = None

if st.session_state.get('current_project'):
    # Use project selected from main page
    selected_project = st.session_state.current_project
    selected_project_name = selected_project['name']
else:
    # Select project manually
    project_names = [project['name'] for project in user_projects]
    selected_project_name = st.selectbox("Select a project for analysis:", project_names)
    
    # Find the selected project
    selected_project = next((p for p in user_projects if p['name'] == selected_project_name), None)
    
    # Save in session state
    if selected_project:
        st.session_state.current_project = selected_project

# Page header with project name
col1, col2, col3, col4 = st.columns([4, 1, 1, 1])

with col1:
    if selected_project_name:
        st.header(f"📊 {selected_project_name}")
    else:
        st.header("📊 Project Analysis")

with col2:
    # Spacing
    st.write("")

with col3:
    # Button to edit project (only if there is a selected project)
    if st.session_state.get('current_project'):
        if st.button("✏️ Edit Project", use_container_width=True):
            st.session_state.show_edit_form = True

with col4:
    # Button to return to main page
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("streamlit_app.py")

st.markdown('---')

# Show project information if selected
if st.session_state.get('current_project'):
    selected_project = st.session_state.current_project
    selected_project_name = selected_project['name']

# Check if we have a selected project for analysis
if selected_project:
    # Show project information only if we are NOT editing
    if not st.session_state.get('show_edit_form', False):
        # Display project information
        st.subheader(f"Project Information")
        
        # Basic LCA project information in 3 columns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**🔑 Project Code:** {selected_project.get('key_code', 'N/A')}")
            st.markdown(f"**🎯 Goal Statement:** {selected_project.get('goal_statement', selected_project.get('description', 'N/A'))}")
            st.markdown(f"**📋 Intended Application:** {selected_project.get('intended_application', 'N/A')}")
            st.markdown(f"**📊 Type of LCA Study:** {selected_project.get('type_of_lca', selected_project.get('type', 'N/A'))}")
            st.markdown(f"**⚖️ Methodology:** {selected_project.get('methodology', 'N/A')}")
        
        with col2:
            st.markdown(f"**📏 Scale:** {selected_project.get('scale', 'N/A')}")
            st.markdown(f"**📊 Level of Detail:** {selected_project.get('level_of_detail', 'N/A')}")
            # Format Reference Flow with all information
            ref_flow = selected_project.get('reference_flow', 'N/A')
            ref_unit = selected_project.get('reference_flow_unit', '')
            # Compatibility with old projects that used 'reference_flow_description'
            ref_time = selected_project.get('reference_flow_time_unit') or selected_project.get('reference_flow_description', '')
            if ref_flow != 'N/A' and ref_unit and ref_time:
                reference_flow_display = f"{ref_flow} {ref_unit}/{ref_time}"
            else:
                reference_flow_display = ref_flow
            st.markdown(f"**🔄 Reference Flow:** {reference_flow_display}")
            st.markdown(f"**🏭 System Boundaries:** {selected_project.get('system_boundaries', 'N/A')}")
            st.markdown(f"**🎛️ Product/System:** {selected_project.get('product_system', 'N/A')}")
        
        with col3:
            # Display Functional Unit - compatibility with old and new projects
            functional_unit_unit = selected_project.get('functional_unit_unit')
            functional_unit_object = selected_project.get('functional_unit_object')
            if functional_unit_unit and functional_unit_object:
                functional_unit_display = f"{functional_unit_unit} of {functional_unit_object}"
            else:
                # Compatibility with old projects
                functional_unit_display = selected_project.get('functional_unit', 'N/A')
            st.markdown(f"**📐 Functional Unit:** {functional_unit_display}")
            st.markdown(f"**🌍 Region:** {selected_project.get('region', 'N/A')}")
            
            # Absolute Sustainability information (if applicable)
            if selected_project.get('sharing_principle') and selected_project.get('reason_sharing_principle'):
                st.markdown("**🌱 Absolute Sustainability Study:** Yes")
                st.markdown(f"**📊 Sharing Principle:** {selected_project.get('sharing_principle', 'N/A')}")
                st.markdown(f"**💡 Reason:** {selected_project.get('reason_sharing_principle', 'N/A')}")
            else:
                st.markdown("**🌱 Absolute Sustainability Study:** No")
                st.markdown("")
                st.markdown("")
        
        # Initialize state for LCI if it doesn't exist
        if 'lci_started' not in st.session_state:
            st.session_state.lci_started = {}
        
        # Check if LCI was started for this project
        project_key = selected_project.get('key_code', selected_project['name'])
        lci_initiated = st.session_state.lci_started.get(project_key, False)
        
        # Check if LCI data already exists saved in the project
        has_lci_data = selected_project.get('lci_data') is not None
        
        # Continue to LCI / LCI Data section
        st.markdown("---")
        
        if not lci_initiated and not has_lci_data:
            # Show LCI unlock section with progress visual
            st.markdown("### 📋 Life Cycle Inventory (LCI)")
            
            # Subtle container with elegant style for the unlock phase
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #f8f9fd 0%, #f0f4f7 100%);
                padding: 25px;
                border-radius: 12px;
                text-align: center;
                color: #2c3e50;
                margin: 15px 0;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
                border: 1px solid #e3eaf0;
                position: relative;
                overflow: hidden;
            ">
                <div style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 3px;
                    background: linear-gradient(90deg, #28a745, #20c997);
                "></div>
                <h3 style="margin: 10px 0 15px 0; font-size: 1.6em; color: #2c3e50;">🔓 Ready to Unlock Phase 2</h3>
                <p style="font-size: 1.1em; margin: 0 0 15px 0; color: #5a6c7d;">
                    ✨ Great progress! Phase 1 completed successfully.
                </p>                        
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Main unlock button with special style

            if st.button("Continue to LCI", use_container_width=True, type="primary", key="unlock_lci_btn"):
                st.session_state.lci_started[project_key] = True
                # Show unlock animation
                st.balloons()
                st.success("🎉 LCI Phase Unlocked! Welcome to Phase 2!")
                import time
                time.sleep(2)  # Short pause for animation
                st.rerun()
        
        else:
            # Show LCI section with level system
            st.markdown("### 📋 Life Cycle Inventory (LCI)")
            
            # Initialize user level if it doesn't exist
            if 'user_lci_level' not in st.session_state:
                st.session_state.user_lci_level = {}
            
            if project_key not in st.session_state.user_lci_level:
                st.session_state.user_lci_level[project_key] = 0  # Default level
            
            current_level = st.session_state.user_lci_level[project_key]
            
            # Interface for level selection
            st.markdown("#### 🎯 LCI Assessment Level")
            
            level_descriptions = {
                0: "**Level 0** - I don't know the process needed to reach the desired product",
                1: "**Level 1** - I know the process but don't have the flow data for each part",
                2: "**Level 2** - I know the process and have partial flow data",
                3: "**Level 3** - I know the process and have all necessary flow data"
            }
            
            # Show level descriptions in cards
            for level, description in level_descriptions.items():
                if level == current_level:
                    st.success(f"✅ Current Level: {description}")
                else:
                    st.info(description)
            
            st.markdown("---")
            
            # Level selector
            col_level1, col_level2 = st.columns([2, 1])
            
            with col_level1:
                st.markdown("**Select your current LCI knowledge level:**")
                level_options = [
                    "Level 0 - Don't know the process",
                    "Level 1 - Know process, no data",
                    "Level 2 - Know process, partial data", 
                    "Level 3 - Know process, have all data"
                ]
                
                selected_level_text = st.selectbox(
                    "LCI Level",
                    level_options,
                    index=current_level,
                    key=f"lci_level_selector_{project_key}"
                )
                
                # Extract the selected level number
                selected_level = int(selected_level_text.split()[1])
                
                # Update level if changed
                if selected_level != current_level:
                    st.session_state.user_lci_level[project_key] = selected_level
                    st.rerun()
            
            with col_level2:
                st.markdown("**Current Status:**")
                if current_level == 0:
                    st.error("🔍 Process Identification Needed")
                elif current_level == 1:
                    st.warning("📊 Data Collection Needed")
                elif current_level == 2:
                    st.warning("📈 Partial Data Available")
                else:
                    st.success("✅ Ready for LCI Input")
            
            st.markdown("---")
            
            # Buttons based on current level
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            
            with col_btn2:
                if current_level == 0:
                    if st.button("🔍 Identify your LCI Process", use_container_width=True, type="primary"):
                        st.info("🚧 Process identification functionality will be available soon!")
                        
                elif current_level == 1:
                    if st.button("� Go to LCI Data Generation", use_container_width=True, type="primary"):
                        st.info("🚧 LCI data generation functionality will be available soon!")
                        
                elif current_level == 2:
                    if st.button("📈 Go to Missing LCI Data Generation", use_container_width=True, type="primary"):
                        st.info("🚧 Missing LCI data generation functionality will be available soon!")
                        
                elif current_level == 3:
                    if st.button("➕ Add Your LCI Data", use_container_width=True, type="primary"):
                        st.info("🚧 LCI data input functionality will be available soon!")
            
            # Additional information based on level
            st.markdown("---")
            st.markdown("#### 💡 Next Steps")
            
            if current_level == 0:
                st.markdown("""
                **Process Identification Phase:**
                - Map out the complete production process
                - Identify all input and output flows
                - Define system boundaries clearly
                - Create process flow diagrams
                """)
                
            elif current_level == 1:
                st.markdown("""
                **Data Collection Phase:**
                - Gather quantitative data for all process inputs
                - Collect emission factors and conversion rates
                - Document energy consumption patterns
                - Compile waste and by-product information
                """)
                
            elif current_level == 2:
                st.markdown("""
                **Data Completion Phase:**
                - Identify missing data gaps
                - Prioritize critical missing information
                - Use estimation methods or literature values
                - Validate partial data consistency
                """)
                
            else:
                st.markdown("""
                **Data Input Phase:**
                - Input all collected LCI data
                - Organize data by process stages
                - Verify data quality and completeness
                - Prepare for impact assessment
                """)

        st.markdown("---")

        # Show System Boundaries figure if available
        if selected_project.get('system_boundaries_figure'):
            with st.expander("**System Boundaries Figure**"):
                try:
                    st.image(selected_project['system_boundaries_figure'], caption="System Boundaries Diagram")
                except:
                    st.info("Figure saved but cannot be displayed at the moment.")

        # Section for notes and observations
        st.write("### 📝 Project Notes & Observations")
        
        if 'notes' not in st.session_state:
            st.session_state.notes = {}
        
        if selected_project_name not in st.session_state.notes:
            st.session_state.notes[selected_project_name] = ""
        
        notes = st.text_area(
            "Add observations about this project:",
            value=st.session_state.notes[selected_project_name],
            height=150
        )
        
        if notes != st.session_state.notes[selected_project_name]:
            st.session_state.notes[selected_project_name] = notes
            st.success("Observations saved!")

# Initialize state for editing if it doesn't exist
if 'show_edit_form' not in st.session_state:
    st.session_state.show_edit_form = False

# Edit form (if editing)
if st.session_state.get('show_edit_form') and selected_project:
    
    # Import necessary functions from utils
    from utils import save_user_data
    
    # Initialize values in session_state for editing if they don't exist
    if 'edit_product_system' not in st.session_state:
        # Map old values to new simplified values
        current_product = selected_project.get('product_system', 'Biofuels')
        product_mapping = {
            "Option A - Biofuels": "Biofuels",
            "Option B - Food Products": "Food Products", 
            "Option C - Building Materials": "Building Materials",
            "Option D - Electronics": "Electronics",
            "Option E - Chemicals": "Chemicals",
            "Option F - Energy Systems": "Energy Systems"
        }
        st.session_state.edit_product_system = product_mapping.get(current_product, current_product)
    if 'edit_functional_unit_unit' not in st.session_state:
        # Check if it has separate fields, otherwise try to extract from old functional_unit field
        if selected_project.get('functional_unit_unit'):
            st.session_state.edit_functional_unit_unit = selected_project['functional_unit_unit']
        else:
            # Tentar extrair do campo functional_unit antigo (formato: "L of biofuel")
            functional_unit = selected_project.get('functional_unit', 'kg of product')
            try:
                unit_part = functional_unit.split(' of ')[0].strip()
                st.session_state.edit_functional_unit_unit = unit_part
            except:
                st.session_state.edit_functional_unit_unit = 'kg'
    if 'edit_functional_unit_object' not in st.session_state:
        # Verificar se tem os campos separados, senão tentar extrair do campo funcional_unit antigo
        if selected_project.get('functional_unit_object'):
            st.session_state.edit_functional_unit_object = selected_project['functional_unit_object']
        else:
            # Tentar extrair do campo functional_unit antigo (formato: "L of biofuel")
            functional_unit = selected_project.get('functional_unit', 'kg of product')
            try:
                object_part = functional_unit.split(' of ')[1].strip()
                st.session_state.edit_functional_unit_object = object_part
            except:
                st.session_state.edit_functional_unit_object = 'product'
    
    # Layout: Form on left, dynamic fields on right
    edit_form_col, edit_dynamic_col = st.columns([2, 1])
    
    with edit_form_col:
        with st.form(key="edit_project_form_analysis", border=False):
            st.markdown("### ✏️ Edit Project")
            # Basic fields
            edit_name = st.text_input("Project Name", value=selected_project['name'])
            edit_goal = st.text_input("Goal Statement", value=selected_project.get('goal_statement', selected_project.get('description', '')))
            edit_application = st.text_input("Intended Application", value=selected_project.get('intended_application', ''))
            
            col1, col2 = st.columns(2)
            with col1:
                # Safe handling for selectbox with indices
                level_options = ["Screening", "Streamlined", "Detailed"]
                current_level = selected_project.get('level_of_detail', 'Screening')
                level_index = level_options.index(current_level) if current_level in level_options else 0
                edit_level = st.selectbox("Level of Detail", 
                                        level_options,
                                        index=level_index)
                
                lca_type_options = ["Prospective", "Traditional", "AESA"]
                current_lca_type = selected_project.get('type_of_lca', selected_project.get('type', 'Traditional'))
                lca_type_index = lca_type_options.index(current_lca_type) if current_lca_type in lca_type_options else 1
                edit_lca_type = st.selectbox("Type of LCA study", 
                                           lca_type_options,
                                           index=lca_type_index)
                
                methodology_options = ["Attributional", "Consequential"]
                current_methodology = selected_project.get('methodology', 'Attributional')
                methodology_index = methodology_options.index(current_methodology) if current_methodology in methodology_options else 0
                edit_methodology = st.selectbox("Methodology", 
                                               methodology_options,
                                               index=methodology_index)
                
                scale_options = ["lab", "pilot", "industrial"]
                current_scale = selected_project.get('scale', 'lab')
                scale_index = scale_options.index(current_scale) if current_scale in scale_options else 0
                edit_scale = st.selectbox("Scale", 
                                         scale_options,
                                         index=scale_index)
            with col2:
                # Reference Flow - sem subcolunas para evitar aninhamento
                st.write("**Reference Flow**")
                edit_reference_flow = st.number_input("Amount", 
                                                    value=float(selected_project.get('reference_flow', 0)), 
                                                    min_value=0.0, step=1.0, key="edit_ref_flow_analysis")
                
                unit_options = ["kg", "L", "m³", "MJ"]
                current_unit = selected_project.get('reference_flow_unit', 'kg')
                unit_index = unit_options.index(current_unit) if current_unit in unit_options else 0
                edit_reference_flow_unit = st.selectbox("Reference Flow Unit", 
                                                       unit_options,
                                                       index=unit_index)
                
                time_options = ["hour", "day", "month", "year"]
                # Compatibility with old projects that used 'reference_flow_description'
                current_time = selected_project.get('reference_flow_time_unit') or selected_project.get('reference_flow_description', 'day')
                time_index = time_options.index(current_time) if current_time in time_options else 1
                edit_reference_flow_time_unit = st.selectbox("Time Unit", 
                                                              time_options,
                                                              index=time_index)
                
                boundaries_options = ["gate-to-gate", "cradle-to-gate", "cradle-to-grave", "cradle-to-cradle"]
                current_boundaries = selected_project.get('system_boundaries', 'gate-to-gate')
                boundaries_index = boundaries_options.index(current_boundaries) if current_boundaries in boundaries_options else 0
                edit_boundaries = st.selectbox("System Boundaries", 
                                              boundaries_options,
                                              index=boundaries_index)
                
                region_options = ["Brazil", "Portugal", "Denmark", "UK", "Germany", "USA", "New Zealand"]
                current_region = selected_project.get('region', 'Brazil')
                region_index = region_options.index(current_region) if current_region in region_options else 0
                edit_region = st.selectbox("Region", 
                                          region_options,
                                          index=region_index)
            
            # Absolute Sustainability Study
            with st.expander("**Absolute Sustainability Study?**"):
                sharing_options = ["Equal per Capita", "Grandfathering", "Economic Share", "Needs-Based"]
                current_sharing = selected_project.get('sharing_principle', 'Equal per Capita')
                sharing_index = sharing_options.index(current_sharing) if current_sharing in sharing_options else 0
                edit_sharing = st.selectbox("Sharing Principle", 
                                           sharing_options,
                                           index=sharing_index)
                edit_reason_sharing = st.text_input("Reason for Sharing Principle", 
                                                   value=selected_project.get('reason_sharing_principle', ''))
            
            # Form buttons without column nesting
            submit_edit = st.form_submit_button("💾 Save Changes", use_container_width=True)
            cancel_edit = st.form_submit_button("❌ Cancel", use_container_width=True)
    
    with edit_dynamic_col:
        st.markdown("### Product Settings")
        
        # Product system outside form to allow reactivity
        edit_product = st.selectbox("Product/system to be studied", 
                                    ["Biofuels", "Food Products", "Building Materials", 
                                     "Electronics", "Chemicals", "Energy Systems"],
                                    key="edit_product_system")
        
        # Functional Unit also outside form for reactivity
        st.write("**Functional Unit**")
        
        # Options for Unit based on product system
        unit_options_by_product = {
            "Biofuels": ["L", "MJ", "kg", "km"],
            "Food Products": ["kg", "meal", "kcal", "g"],
            "Building Materials": ["m²", "m³", "kg", "unit"],
            "Electronics": ["device", "year", "unit", "GB"],
            "Chemicals": ["kg", "mol", "L", "dose"],
            "Energy Systems": ["kWh", "MW", "year", "GJ"]
        }
        
        edit_functional_unit_unit = st.selectbox("Unit", 
                                               unit_options_by_product.get(edit_product, ["kg", "unit", "m²", "L"]),
                                               key="edit_functional_unit_unit")
        
        # Options para Object baseadas no product system
        object_options_by_product = {
            "Biofuels": ["biofuel", "energy", "fuel", "driven"],
            "Food Products": ["product", "meal", "energy", "protein content"],
            "Building Materials": ["surface", "volume", "material", "functional unit area"],
            "Electronics": ["device", "use", "processing capacity", "storage capacity"],
            "Chemicals": ["chemical", "substance", "solution", "functional dose"],
            "Energy Systems": ["generated", "capacity", "operation", "energy"]
        }
        
        edit_functional_unit_object = st.selectbox("Object", 
                                                 object_options_by_product.get(edit_product, ["product", "service", "material", "energy"]),
                                                 key="edit_functional_unit_object")
    
    # Process form submission
    # Process form submission
    if submit_edit:
        # Find the index of current project in the user's project list
        user_projects = st.session_state.user_projects.get(username, [])
        project_index = None
        for idx, project in enumerate(user_projects):
            if project.get('key_code') == selected_project.get('key_code'):
                project_index = idx
                break
        
        if project_index is not None:
            # Update project
            st.session_state.user_projects[username][project_index] = {
                'name': edit_name,
                'key_code': selected_project.get('key_code', '000000'),  # Keep existing code
                'goal_statement': edit_goal,
                'intended_application': edit_application,
                'level_of_detail': edit_level,
                'type_of_lca': edit_lca_type,
                'methodology': edit_methodology,
                'scale': edit_scale,
                'reference_flow': edit_reference_flow,
                'reference_flow_unit': edit_reference_flow_unit,
                'reference_flow_time_unit': edit_reference_flow_time_unit,
                'system_boundaries': edit_boundaries,
                'system_boundaries_figure': selected_project.get('system_boundaries_figure'),  # Manter figura existente
                'product_system': st.session_state.edit_product_system,
                'functional_unit_unit': st.session_state.edit_functional_unit_unit,
                'functional_unit_object': st.session_state.edit_functional_unit_object,
                # Manter o campo antigo para compatibilidade
                'functional_unit': f"{st.session_state.edit_functional_unit_unit} of {st.session_state.edit_functional_unit_object}",
                'region': edit_region,
                'sharing_principle': edit_sharing,
                'reason_sharing_principle': edit_reason_sharing,
                'created_at': selected_project.get('created_at', pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")),
                'updated_at': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Also update current project in session
            st.session_state.current_project = st.session_state.user_projects[username][project_index]
            
            # Save data
            user_data = {
                'projects': st.session_state.user_projects[username],
                'preferences': {
                    'theme': st.session_state.theme,
                    'notifications': st.session_state.notifications
                },
                'last_update': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            save_user_data(username, user_data)
            
            st.success("✅ Project updated successfully!")
            st.session_state.show_edit_form = False
            st.rerun()
        else:
            st.error("❌ Error finding project for update.")
    
    if cancel_edit:
        st.session_state.show_edit_form = False
        st.rerun()
