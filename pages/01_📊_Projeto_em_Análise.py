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
from utils import check_authentication, generate_project_pdf, save_user_data
from brightway_integration import (
    SustainExcelImporter, 
    generate_excel_template, 
    get_example_lci_file,
    generate_process_network_diagram
)

# Initialize session states
if 'show_edit_form' not in st.session_state:
    st.session_state.show_edit_form = False
if 'show_export' not in st.session_state:
    st.session_state.show_export = False
if 'show_level_3_interface' not in st.session_state:
    st.session_state.show_level_3_interface = False

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
col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])

with col1:
    if selected_project_name:
        st.header(f"📊 {selected_project_name}")
    else:
        st.header("📊 Project Analysis")

with col2:
    # Spacing
    st.write("")

with col3:
    # Button to export project (only if there is a selected project)
    if st.session_state.get('current_project'):
        if st.button("📄 Export", use_container_width=True):
            st.session_state.show_export = True

with col4:
    # Button to edit project (only if there is a selected project)
    if st.session_state.get('current_project'):
        if st.button("✏️ Edit", use_container_width=True):
            st.session_state.show_edit_form = True

with col5:
    # Button to return to main page
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("streamlit_app.py")

st.markdown('---')

# Handle Export functionality
if st.session_state.get('show_export') and st.session_state.get('current_project'):
    selected_project = st.session_state.current_project
    selected_project_name = selected_project['name']
    
    # Generate PDF
    try:
        pdf_buffer = generate_project_pdf(selected_project, selected_project_name)
        
        # Create download button
        st.success("✅ PDF report generated successfully!")
        
        # Filename with timestamp
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Project_Report_{selected_project_name.replace(' ', '_')}_{timestamp}.pdf"
        
        # Download button
        st.download_button(
            label="⬇️ Download PDF Report",
            data=pdf_buffer.getvalue(),
            file_name=filename,
            mime="application/pdf",
            use_container_width=True
        )
        
        # Reset export state after showing download
        if st.button("✅ Done", use_container_width=True):
            st.session_state.show_export = False
            st.rerun()
            
    except Exception as e:
        st.error(f"❌ Error generating PDF: {str(e)}")
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.show_export = False
            st.rerun()
    
    # Add some spacing
    st.markdown("---")

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
            
            # Check if LCI data already exists (user completed Level 3)
            if selected_project.get('lci_complete'):
                st.success("✅ **LCI Data Available** - Your inventory is ready for impact assessment!")
                
                lci_data = selected_project.get('lci_data', {})
                db_name = selected_project.get('lci_database_name', 'N/A')
                upload_date = selected_project.get('lci_upload_date', 'N/A')
                
                # Summary metrics
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                
                with col_m1:
                    activities_count = len(lci_data.get('activities', []))
                    st.metric("📦 Activities", activities_count)
                
                with col_m2:
                    exchanges_count = len(lci_data.get('exchanges', []))
                    st.metric("🔄 Exchanges", exchanges_count)
                
                with col_m3:
                    biosphere_count = sum(1 for e in lci_data.get('exchanges', []) 
                                         if e.get('type') in ['emission', 'resource'])
                    st.metric("🌍 Biosphere Flows", biosphere_count)
                
                with col_m4:
                    st.metric("💾 Database", db_name[:15] + "..." if len(db_name) > 15 else db_name)
                
                st.markdown("---")
                
                # Detailed information in expander
                with st.expander("📊 **View Detailed LCI Data**", expanded=False):
                    
                    tab_summary, tab_activities, tab_exchanges = st.tabs([
                        "📋 Summary", "🏭 Activities", "🔄 Exchanges"
                    ])
                    
                    with tab_summary:
                        st.markdown("#### Database Information")
                        col_info1, col_info2 = st.columns(2)
                        
                        with col_info1:
                            st.markdown(f"**Database Name:** {db_name}")
                            st.markdown(f"**Upload Date:** {upload_date}")
                            st.markdown(f"**Data Source:** {selected_project.get('lci_data_source', 'N/A')}")
                        
                        with col_info2:
                            metadata = lci_data.get('metadata', {})
                            st.markdown(f"**Functional Unit:** {metadata.get('functional_unit', 'N/A')}")
                            st.markdown(f"**Location:** {metadata.get('location', 'N/A')}")
                            st.markdown(f"**Time Period:** {metadata.get('time_period', 'N/A')}")
                        
                        st.markdown("---")
                        st.markdown("#### Process Activities Overview")
                        
                        activities = lci_data.get('activities', [])
                        if activities:
                            activities_df = pd.DataFrame(activities)
                            # Show key columns
                            display_cols = ['code', 'name', 'location', 'unit']
                            available_cols = [col for col in display_cols if col in activities_df.columns]
                            st.dataframe(
                                activities_df[available_cols],
                                use_container_width=True,
                                hide_index=True
                            )
                    
                    with tab_activities:
                        st.markdown("#### All Process Activities")
                        activities = lci_data.get('activities', [])
                        if activities:
                            activities_df = pd.DataFrame(activities)
                            st.dataframe(
                                activities_df,
                                use_container_width=True,
                                hide_index=True
                            )
                        else:
                            st.info("No activities data available")
                    
                    with tab_exchanges:
                        st.markdown("#### All Exchanges (Inputs & Outputs)")
                        exchanges = lci_data.get('exchanges', [])
                        if exchanges:
                            exchanges_df = pd.DataFrame(exchanges)
                            
                            # Filter options
                            col_filter1, col_filter2 = st.columns(2)
                            
                            with col_filter1:
                                exchange_types = ['All'] + list(exchanges_df['type'].unique()) if 'type' in exchanges_df.columns else ['All']
                                selected_type = st.selectbox("Filter by Type", exchange_types)
                            
                            with col_filter2:
                                if 'activity_code' in exchanges_df.columns:
                                    activity_codes = ['All'] + list(exchanges_df['activity_code'].unique())
                                    selected_activity = st.selectbox("Filter by Activity", activity_codes)
                                else:
                                    selected_activity = 'All'
                            
                            # Apply filters
                            filtered_df = exchanges_df.copy()
                            if selected_type != 'All' and 'type' in filtered_df.columns:
                                filtered_df = filtered_df[filtered_df['type'] == selected_type]
                            if selected_activity != 'All' and 'activity_code' in filtered_df.columns:
                                filtered_df = filtered_df[filtered_df['activity_code'] == selected_activity]
                            
                            st.dataframe(
                                filtered_df,
                                use_container_width=True,
                                hide_index=True
                            )
                            
                            st.caption(f"Showing {len(filtered_df)} of {len(exchanges_df)} exchanges")
                        else:
                            st.info("No exchanges data available")
                
                st.markdown("---")
                
                # Action buttons
                col_action1, col_action2, col_action3 = st.columns([1, 1, 1])
                
                with col_action1:
                    if st.button("🔄 Redo LCI Data", use_container_width=True, type="secondary"):
                        # Clear LCI data and restart
                        selected_project['lci_complete'] = False
                        selected_project['lci_data'] = None
                        selected_project['lci_database_name'] = None
                        selected_project['lci_upload_date'] = None
                        
                        # Update in user_projects
                        for idx, proj in enumerate(st.session_state.user_projects[username]):
                            if proj.get('key_code') == selected_project.get('key_code'):
                                st.session_state.user_projects[username][idx] = selected_project
                                break
                        
                        # Save to file
                        user_data = {
                            'projects': st.session_state.user_projects[username],
                            'preferences': {
                                'theme': st.session_state.get('theme', 'light'),
                                'notifications': st.session_state.get('notifications', True)
                            },
                            'last_update': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        save_user_data(username, user_data)
                        
                        st.success("🔄 LCI data cleared! You can now upload new data.")
                        import time
                        time.sleep(1)
                        st.rerun()
                
                with col_action2:
                    if st.button("📊 Run Impact Assessment", use_container_width=True, type="primary", disabled=True):
                        st.info("🚧 Impact assessment functionality will be available soon!")
                
                with col_action3:
                    if st.button("📥 Export LCI Data", use_container_width=True, disabled=True):
                        st.info("🚧 Export functionality will be available soon!")
            
            # Check if Level 3 interface should be shown
            elif st.session_state.get('show_level_3_interface'):
                # Show Level 3 interface (replaces level selection)
                st.markdown("#### ➕ Add Your Complete LCI Data")
                
                # Back button
                if st.button("⬅️ Back to Level Selection"):
                    st.session_state.show_level_3_interface = False
                    st.rerun()
                
                st.info("""
                📋 **You have all your LCI data?** Great! Upload it here.
                
                Your data should include:
                - All process activities
                - All inputs (materials, energy, water, etc.)
                - All outputs (products, emissions, waste, etc.)
                - Amounts with units
                """)
                
                # Step 1: Download template
                st.markdown("### 📥 Step 1: Get the Template")
                
                col_template, col_example = st.columns(2)
                
                with col_template:
                    # Generate template
                    template_buffer = generate_excel_template(selected_project)
                    
                    st.download_button(
                        label="⬇️ Download Excel Template",
                        data=template_buffer,
                        file_name="Sustain40_LCI_Template.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        help="Download the blank template to fill with your data"
                    )
                
                with col_example:
                    # Example file
                    example_buffer = get_example_lci_file()
                    
                    st.download_button(
                        label="📖 Download Example File",
                        data=example_buffer,
                        file_name="Sustain40_LCI_Example.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        help="Download an example file to see how to structure your data"
                    )
                
                st.markdown("---")
                
                # Step 2: Upload filled file
                st.markdown("### 📤 Step 2: Upload Your Data")
                
                uploaded_file = st.file_uploader(
                    "Upload your filled Excel file",
                    type=['xlsx', 'xls'],
                    help="Use the template above and fill with your LCI data",
                    key="lci_file_uploader"
                )
                
                if uploaded_file:
                    
                    # Save temporarily
                    import tempfile
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                        tmp.write(uploaded_file.getvalue())
                        tmp_path = tmp.name
                    
                    # Parse and validate
                    with st.spinner("🔍 Validating your data..."):
                        importer = SustainExcelImporter(tmp_path)
                        is_valid = importer.parse_excel()
                    
                    # Show validation results
                    if importer.validation_errors:
                        st.error("❌ Validation Errors Found:")
                        for error in importer.validation_errors:
                            st.error(error)
                        
                        st.info("💡 Please fix the errors in your Excel file and upload again.")
                        
                    else:
                        # Show warnings (non-blocking)
                        if importer.warnings:
                            with st.expander("⚠️ Warnings (non-critical)", expanded=False):
                                for warning in importer.warnings:
                                    st.warning(warning)
                        
                        st.success("✅ File validated successfully!")
                        
                        # Step 3: Preview data
                        st.markdown("---")
                        st.markdown("### 👁️ Step 3: Preview Your Data")
                        
                        tab_activities, tab_exchanges, tab_network = st.tabs([
                            "📋 Activities", "🔄 Exchanges", "🕸️ Network Diagram"
                        ])
                        
                        with tab_activities:
                            st.markdown("#### Process Activities")
                            activities_df = pd.DataFrame(importer.activities)
                            st.dataframe(
                                activities_df,
                                use_container_width=True,
                                hide_index=True
                            )
                            
                            col_m1, col_m2 = st.columns(2)
                            with col_m1:
                                st.metric("Total Activities", len(importer.activities))
                            with col_m2:
                                unique_locations = len(set(act['location'] for act in importer.activities))
                                st.metric("Locations", unique_locations)
                        
                        with tab_exchanges:
                            st.markdown("#### All Exchanges")
                            exchanges_df = pd.DataFrame(importer.exchanges)
                            
                            # Add color coding by type
                            st.dataframe(
                                exchanges_df,
                                use_container_width=True,
                                hide_index=True
                            )
                            
                            col_m1, col_m2, col_m3 = st.columns(3)
                            with col_m1:
                                st.metric("Total Exchanges", len(importer.exchanges))
                            with col_m2:
                                inputs = sum(1 for e in importer.exchanges if e['type'] == 'input')
                                st.metric("Inputs", inputs)
                            with col_m3:
                                emissions = sum(1 for e in importer.exchanges if e['type'] == 'emission')
                                st.metric("Emissions", emissions)
                        
                        with tab_network:
                            st.markdown("#### Process Flow Diagram")
                            
                            if len(importer.activities) > 0:
                                try:
                                    fig = generate_process_network_diagram(
                                        importer.activities,
                                        importer.exchanges
                                    )
                                    if fig:
                                        st.plotly_chart(fig, use_container_width=True)
                                    else:
                                        st.info("""
                                        📦 **Network diagram requires networkx package**
                                        
                                        Install with: `pip install networkx`
                                        
                                        The diagram will show process connections and flows between activities.
                                        """)
                                except Exception as e:
                                    st.warning(f"⚠️ Could not generate network diagram.\n\nDetails: {str(e)}")
                                    st.info("Install networkx package to enable this feature: `pip install networkx`")
                            else:
                                st.info("No activities to display")
                        
                        # Step 4: Create database
                        st.markdown("---")
                        st.markdown("### 💾 Step 4: Create LCA Database")
                        
                        st.info("""
                        ✨ **Almost there!** Click below to create your Brightway database.
                        
                        This will:
                        - Convert your data to Brightway format
                        - Link emissions to biosphere flows
                        - Validate all connections
                        - Make it ready for LCA calculations
                        """)
                        
                        db_name = st.text_input(
                            "Database Name",
                            value=f"lci_{selected_project['key_code']}",
                            help="Name for your Brightway database (no spaces)"
                        )
                        
                        # Replace spaces with underscores
                        db_name = db_name.replace(' ', '_')
                        
                        col_cancel, col_create = st.columns([1, 2])
                        
                        with col_cancel:
                            if st.button("❌ Cancel", use_container_width=True, key="cancel_db_creation"):
                                st.session_state.show_level_3_interface = False
                                st.rerun()
                        
                        with col_create:
                            if st.button("🚀 Create Database & Run LCA", type="primary", use_container_width=True):
                                
                                with st.spinner("Creating Brightway database..."):
                                    try:
                                        # Note: Brightway integration requires setup
                                        # For now, we'll save the data structure
                                        
                                        # Save parsed data to project
                                        selected_project['lci_database_name'] = db_name
                                        selected_project['lci_data'] = {
                                            'metadata': importer.metadata,
                                            'activities': importer.activities,
                                            'exchanges': importer.exchanges,
                                            'flow_mapping': importer.flow_mapping
                                        }
                                        selected_project['lci_data_source'] = 'user_upload'
                                        selected_project['lci_complete'] = True
                                        selected_project['lci_upload_date'] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                                        
                                        # Update project in user_projects
                                        for idx, proj in enumerate(st.session_state.user_projects[username]):
                                            if proj.get('key_code') == selected_project.get('key_code'):
                                                st.session_state.user_projects[username][idx] = selected_project
                                                break
                                        
                                        # Save to file
                                        user_data = {
                                            'projects': st.session_state.user_projects[username],
                                            'preferences': {
                                                'theme': st.session_state.get('theme', 'light'),
                                                'notifications': st.session_state.get('notifications', True)
                                            },
                                            'last_update': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                                        }
                                        save_user_data(username, user_data)
                                        
                                        st.success(f"✅ LCI data saved successfully!")
                                        
                                        # Show database info
                                        col_m1, col_m2, col_m3 = st.columns(3)
                                        
                                        with col_m1:
                                            st.metric("📦 Activities", len(importer.activities))
                                        with col_m2:
                                            st.metric("🔄 Exchanges", len(importer.exchanges))
                                        with col_m3:
                                            biosphere_count = sum(1 for e in importer.exchanges if e['type'] in ['emission', 'resource'])
                                            st.metric("🌍 Biosphere Flows", biosphere_count)
                                        
                                        st.balloons()
                                        
                                        # Info about next steps
                                        st.markdown("---")
                                        st.info("""
                                        ✨ **Your LCI data is ready!**
                                        
                                        **Next Steps:**
                                        1. Your data has been saved to the project
                                        2. When Brightway is fully configured, you'll be able to:
                                           - Calculate environmental impacts (GWP, water use, etc.)
                                           - Run uncertainty analysis
                                           - Compare scenarios
                                           - Generate detailed reports
                                        
                                        **Current Status:** ✅ Data validated and stored
                                        """)
                                        
                                        if st.button("✅ Done - Back to Project", use_container_width=True, type="primary"):
                                            st.session_state.show_level_3_interface = False
                                            st.rerun()
                                        
                                    except Exception as e:
                                        st.error(f"❌ Error saving database: {str(e)}")
                                        st.exception(e)
            
            else:
                # Show level selection interface
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
                        if st.button("📊 Go to LCI Data Generation", use_container_width=True, type="primary"):
                            st.info("🚧 LCI data generation functionality will be available soon!")
                            
                    elif current_level == 2:
                        if st.button("📈 Go to Missing LCI Data Generation", use_container_width=True, type="primary"):
                            st.info("🚧 Missing LCI data generation functionality will be available soon!")
                            
                    elif current_level == 3:
                        if st.button("➕ Add Your LCI Data", use_container_width=True, type="primary"):
                            st.session_state.show_level_3_interface = True
                            st.rerun()

        st.markdown("---")

# Edit form (if editing)
if st.session_state.get('show_edit_form') and selected_project:
    
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
