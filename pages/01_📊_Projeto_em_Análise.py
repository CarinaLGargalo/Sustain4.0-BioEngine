import streamlit as st

# Configuração da página (DEVE ser o primeiro comando do Streamlit)
st.set_page_config(
    page_title="Projeto em Análise - Sustain 4.0",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Importar outras bibliotecas depois da configuração da página
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Background customizado com opacidade de 30%
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
</style>
"""
st.markdown(page_bg__img, unsafe_allow_html=True)

# Importar funções do módulo de utilitários
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import check_authentication

# Verificação de autenticação
if not st.session_state.get('authenticated', False):
    st.info("🔐 Por favor, faça login na página principal.")
    st.stop()

# Verificar se há projetos disponíveis
username = st.session_state.username
user_projects = st.session_state.user_projects.get(username, [])

if not user_projects:
    st.warning("Você ainda não tem projetos. Crie um projeto na página principal.")
    st.stop()

# Verificar se há um projeto pré-selecionado da página principal
selected_project = None
selected_project_name = None

if st.session_state.get('current_project'):
    # Usar projeto selecionado da página principal
    selected_project = st.session_state.current_project
    selected_project_name = selected_project['name']
else:
    # Selecionar projeto manualmente
    project_names = [project['name'] for project in user_projects]
    selected_project_name = st.selectbox("Selecione um projeto para análise:", project_names)
    
    # Encontrar o projeto selecionado
    selected_project = next((p for p in user_projects if p['name'] == selected_project_name), None)
    
    # Salvar no session state
    if selected_project:
        st.session_state.current_project = selected_project

# Cabeçalho da página com nome do projeto
col1, col2, col3, col4 = st.columns([4, 1, 1, 1])

with col1:
    if selected_project_name:
        st.header(f"📊 {selected_project_name}")
    else:
        st.header("📊 Projeto em Análise")

with col2:
    # Espaçamento
    st.write("")

with col3:
    # Botão para editar projeto (apenas se houver projeto selecionado)
    if st.session_state.get('current_project'):
        if st.button("✏️ Editar Projeto", use_container_width=True):
            st.info("🚧 Redirecionando para edição... (em desenvolvimento)")

with col4:
    # Botão para voltar à página principal
    if st.button("🏠 Voltar ao Início", use_container_width=True):
        st.switch_page("streamlit_app.py")

st.markdown('---')

# Mostrar informações do projeto se selecionado
if st.session_state.get('current_project'):
    selected_project = st.session_state.current_project
    selected_project_name = selected_project['name']

# Verificar se temos um projeto selecionado para análise
if selected_project:
    # Exibir informações do projeto
    st.subheader(f"Informações do Projeto")
    
    # Informações básicas do projeto LCA
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**🔑 Código do Projeto:** {selected_project.get('key_code', 'N/A')}")
        st.markdown(f"**🎯 Goal Statement:** {selected_project.get('goal_statement', selected_project.get('description', 'N/A'))}")
        st.markdown(f"**📋 Intended Application:** {selected_project.get('intended_application', 'N/A')}")
        st.markdown(f"**� Type of LCA Study:** {selected_project.get('type_of_lca', selected_project.get('type', 'N/A'))}")
        st.markdown(f"**⚖️ Methodology:** {selected_project.get('methodology', 'N/A')}")
        st.markdown(f"**📏 Scale:** {selected_project.get('scale', 'N/A')}")
    
    with col2:
        st.markdown(f"**📊 Level of Detail:** {selected_project.get('level_of_detail', 'N/A')}")
        # Formatar Reference Flow com todas as informações
        ref_flow = selected_project.get('reference_flow', 'N/A')
        ref_unit = selected_project.get('reference_flow_unit', '')
        ref_time = selected_project.get('reference_flow_description', '')
        if ref_flow != 'N/A' and ref_unit and ref_time:
            reference_flow_display = f"{ref_flow} {ref_unit}/{ref_time}"
        else:
            reference_flow_display = ref_flow
        st.markdown(f"**🔄 Reference Flow:** {reference_flow_display}")
        st.markdown(f"**🏭 System Boundaries:** {selected_project.get('system_boundaries', 'N/A')}")
        st.markdown(f"**🎛️ Product/System:** {selected_project.get('product_system', 'N/A')}")
        st.markdown(f"**📐 Functional Unit:** {selected_project.get('functional_unit', 'N/A')}")
        st.markdown(f"**🌍 Region:** {selected_project.get('region', 'N/A')}")
    
    # Informações de Absolute Sustainability (se aplicável)
    if selected_project.get('sharing_principle') or selected_project.get('reason_sharing_principle'):
        with st.expander("🌱 Absolute Sustainability Study"):
            st.markdown(f"**Sharing Principle:** {selected_project.get('sharing_principle', 'N/A')}")
            if selected_project.get('reason_sharing_principle'):
                st.markdown(f"**Reason:** {selected_project.get('reason_sharing_principle')}")
    
    # Mostrar figura do System Boundaries se disponível
    if selected_project.get('system_boundaries_figure'):
        with st.expander("🖼️ System Boundaries Figure"):
            try:
                st.image(selected_project['system_boundaries_figure'], caption="System Boundaries Diagram")
            except:
                st.info("Figura salva mas não pode ser exibida no momento.")
    
    st.markdown("---")
    
    # Criar abas para diferentes análises LCA
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 LCA Overview", "🔍 Goal & Scope", "📊 Inventory Analysis", "🌍 Impact Assessment", "📋 Interpretation"])
    
    with tab1:
        st.write("### LCA Project Overview")
        
        # Métricas principais do LCA
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="Project Progress", value="65%", delta="5%")
        with col2:
            st.metric(label="Data Quality", value="B+", delta="Improving")
        with col3:
            st.metric(label="Impact Categories", value="12", delta="2")
        with col4:
            st.metric(label="Study Duration", value="45 days", delta="2 days")
        
        # Gráfico de progresso do estudo LCA
        st.write("### Study Progress Timeline")
        
        # Dados fictícios para demonstração do progresso
        phases = ['Goal & Scope', 'Inventory Analysis', 'Impact Assessment', 'Interpretation']
        progress = [100, 85, 45, 15]  # Porcentagem de conclusão
        
        progress_fig = px.bar(
            x=phases,
            y=progress,
            color=progress,
            color_continuous_scale=['red', 'yellow', 'green'],
            title="LCA Study Phases Completion (%)",
            labels={'x': 'LCA Phases', 'y': 'Completion (%)'}
        )
        
        progress_fig.update_layout(
            xaxis_title="LCA Phases",
            yaxis_title="Completion (%)",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(progress_fig, use_container_width=True)
        
        # Recent Activities
        st.write("### Recent Project Activities")
        activities = [
            {"date": "2025-08-01", "phase": "Inventory Analysis", "activity": "Data collection for energy inputs completed"},
            {"date": "2025-07-28", "phase": "Impact Assessment", "activity": "Climate change impact calculation updated"},
            {"date": "2025-07-25", "phase": "Goal & Scope", "activity": "System boundaries refined based on stakeholder feedback"}
        ]
        
        for activity in activities:
            st.info(f"**{activity['date']}** - [{activity['phase']}] {activity['activity']}")
            
    with tab2:
        st.write("### Goal & Scope Definition")
        
        # Goal Statement expandido
        st.write("#### 🎯 Study Goal")
        st.write(f"**Goal Statement:** {selected_project.get('goal_statement', 'Not defined')}")
        st.write(f"**Intended Application:** {selected_project.get('intended_application', 'Not specified')}")
        
        # Scope Definition
        st.write("#### 🔍 Study Scope")
        
        scope_col1, scope_col2 = st.columns(2)
        
        with scope_col1:
            st.write(f"**Product/System:** {selected_project.get('product_system', 'Not defined')}")
            st.write(f"**Functional Unit:** {selected_project.get('functional_unit', 'Not defined')}")
            # Formatar Reference Flow com todas as informações
            ref_flow = selected_project.get('reference_flow', 'Not defined')
            ref_unit = selected_project.get('reference_flow_unit', '')
            ref_time = selected_project.get('reference_flow_description', '')
            if ref_flow != 'Not defined' and ref_unit and ref_time:
                reference_flow_display = f"{ref_flow} {ref_unit}/{ref_time}"
            else:
                reference_flow_display = ref_flow
            st.write(f"**Reference Flow:** {reference_flow_display}")
            
        with scope_col2:
            st.write(f"**System Boundaries:** {selected_project.get('system_boundaries', 'Not defined')}")
            st.write(f"**Methodology:** {selected_project.get('methodology', 'Not defined')}")
            st.write(f"**Geographic Scope:** {selected_project.get('region', 'Not defined')}")
        
        # Impact Categories (simulado)
        st.write("#### 🌍 Impact Categories Selected")
        impact_categories = [
            "Climate Change", "Ozone Depletion", "Acidification", "Eutrophication",
            "Photochemical Ozone Creation", "Resource Depletion", "Human Toxicity",
            "Ecotoxicity", "Land Use", "Water Use", "Fossil Fuel Depletion", "Biodiversity"
        ]
        
        selected_impacts = st.multiselect(
            "Select impact categories for this study:",
            impact_categories,
            default=impact_categories[:6]  # Default selection
        )
        
        if selected_impacts:
            st.success(f"Selected {len(selected_impacts)} impact categories for assessment.")
            
    with tab3:
        st.write("### Life Cycle Inventory (LCI) Analysis")
        
        # Inventory data overview
        st.write("#### 📋 Inventory Data Collection Status")
        
        # Simulated inventory data
        inventory_data = {
            'Process Category': ['Energy', 'Materials', 'Transportation', 'Waste', 'Water', 'Land Use'],
            'Data Quality': ['A', 'B', 'A', 'C', 'B', 'B'],
            'Completeness (%)': [95, 85, 90, 70, 80, 75],
            'Data Sources': ['Primary', 'Secondary', 'Primary', 'Estimated', 'Secondary', 'Secondary']
        }
        
        inventory_df = pd.DataFrame(inventory_data)
        st.dataframe(inventory_df, hide_index=True)
        
        # Data quality visualization
        st.write("#### 📊 Data Quality Assessment")
        
        quality_fig = px.scatter(
            inventory_df,
            x='Process Category',
            y='Completeness (%)',
            color='Data Quality',
            size='Completeness (%)',
            color_discrete_map={'A': 'green', 'B': 'yellow', 'C': 'red'},
            title="Data Quality vs Completeness by Process Category"
        )
        
        st.plotly_chart(quality_fig, use_container_width=True)
        
        # Input/Output flows (simplified example)
        st.write("#### 🔄 Key Input/Output Flows")
        
        flows_col1, flows_col2 = st.columns(2)
        
        with flows_col1:
            st.write("**Main Inputs:**")
            st.write("• Energy: 150 MJ")
            st.write("• Raw Materials: 25 kg")
            st.write("• Water: 100 L")
            st.write("• Land: 2 m²")
            
        with flows_col2:
            st.write("**Main Outputs:**")
            st.write("• Product: 1 unit")
            st.write("• CO₂ emissions: 12 kg")
            st.write("• Wastewater: 80 L")
            st.write("• Solid waste: 3 kg")
            
    with tab4:
        st.write("### Life Cycle Impact Assessment (LCIA)")
        
        # Impact assessment results (simulated)
        st.write("#### 🌍 Environmental Impact Results")
        
        # Simulated impact data
        impact_data = {
            'Impact Category': ['Climate Change', 'Acidification', 'Eutrophication', 'Ozone Depletion', 'Resource Depletion'],
            'Impact Value': [125.5, 8.2, 0.45, 2.1e-6, 0.025],
            'Unit': ['kg CO₂-eq', 'kg SO₂-eq', 'kg PO₄³⁻-eq', 'kg CFC-11-eq', 'kg Sb-eq'],
            'Contribution (%)': [35, 15, 20, 5, 25]
        }
        
        impact_df = pd.DataFrame(impact_data)
        st.dataframe(impact_df, hide_index=True)
        
        # Impact contribution chart
        st.write("#### 📊 Impact Category Contributions")
        
        contribution_fig = px.pie(
            impact_df,
            values='Contribution (%)',
            names='Impact Category',
            title="Relative Contribution of Impact Categories"
        )
        
        st.plotly_chart(contribution_fig, use_container_width=True)
        
        # Process contribution analysis
        st.write("#### 🏭 Process Contribution Analysis")
        
        process_contrib = {
            'Process': ['Energy Production', 'Material Extraction', 'Manufacturing', 'Transportation', 'End-of-Life'],
            'Climate Change (%)': [45, 25, 20, 8, 2],
            'Acidification (%)': [35, 30, 15, 15, 5],
            'Eutrophication (%)': [20, 40, 25, 10, 5]
        }
        
        process_df = pd.DataFrame(process_contrib)
        
        # Stacked bar chart
        process_fig = px.bar(
            process_df,
            x='Process',
            y=['Climate Change (%)', 'Acidification (%)', 'Eutrophication (%)'],
            title="Process Contribution to Selected Impact Categories"
        )
        
        st.plotly_chart(process_fig, use_container_width=True)
        
    with tab5:
        st.write("### Interpretation & Results")
        
        # Key findings
        st.write("#### 🔍 Key Findings")
        
        findings = [
            "Energy production phase contributes most significantly to climate change impact (45%)",
            "Material extraction phase shows highest contribution to eutrophication potential",
            "Transportation has relatively low impact across all categories (<15%)",
            "Data quality is good overall, with most categories having A or B grade data"
        ]
        
        for i, finding in enumerate(findings, 1):
            st.write(f"{i}. {finding}")
        
        # Sensitivity analysis
        st.write("#### 📈 Sensitivity Analysis")
        
        sensitivity_data = {
            'Parameter': ['Energy Mix', 'Material Type', 'Transportation Distance', 'End-of-Life Scenario'],
            'Base Case Impact': [125.5, 125.5, 125.5, 125.5],
            'Optimistic': [95.2, 110.3, 120.1, 122.8],
            'Pessimistic': [155.8, 140.7, 131.2, 128.9]
        }
        
        sens_df = pd.DataFrame(sensitivity_data)
        
        sens_fig = px.bar(
            sens_df,
            x='Parameter',
            y=['Optimistic', 'Base Case Impact', 'Pessimistic'],
            title="Sensitivity Analysis - Climate Change Impact (kg CO₂-eq)",
            barmode='group'
        )
        
        st.plotly_chart(sens_fig, use_container_width=True)
        
        # Conclusions and recommendations
        st.write("#### 💡 Conclusions & Recommendations")
        
        with st.expander("View Detailed Conclusions"):
            st.write("""
            **Main Conclusions:**
            1. The energy production phase is the primary hotspot for environmental impacts
            2. Switching to renewable energy sources could reduce climate change impact by 24%
            3. Material selection optimization shows significant potential for impact reduction
            4. Transportation optimization has limited impact reduction potential
            
            **Recommendations:**
            1. Prioritize renewable energy sources in the energy mix
            2. Investigate alternative materials with lower environmental footprint
            3. Improve data quality for waste treatment processes
            4. Consider regional variations in energy mixes for different geographic applications
            """)
        
        # Action items
        st.write("#### ✅ Action Items")
        
        action_items = [
            {"action": "Update energy mix data with regional renewable percentages", "priority": "High", "status": "In Progress"},
            {"action": "Collect primary data for waste treatment processes", "priority": "Medium", "status": "Planned"},
            {"action": "Conduct uncertainty analysis for key parameters", "priority": "High", "status": "Not Started"},
            {"action": "Prepare final report and recommendations", "priority": "Low", "status": "Not Started"}
        ]
        
        for item in action_items:
            status_color = {"In Progress": "🟡", "Planned": "🔵", "Not Started": "🔴", "Completed": "🟢"}
            priority_icon = {"High": "🔥", "Medium": "⚡", "Low": "📝"}
            
            st.write(f"{status_color.get(item['status'], '⚪')} {priority_icon.get(item['priority'], '📝')} {item['action']} - *{item['status']}*")
    
    # Seção para notas e observações
    st.write("### 📝 Project Notes & Observations")
    
    if 'notes' not in st.session_state:
        st.session_state.notes = {}
    
    if selected_project_name not in st.session_state.notes:
        st.session_state.notes[selected_project_name] = ""
    
    notes = st.text_area(
        "Adicione observações sobre este projeto:",
        value=st.session_state.notes[selected_project_name],
        height=150
    )
    
    if notes != st.session_state.notes[selected_project_name]:
        st.session_state.notes[selected_project_name] = notes
        st.success("Observações salvas!")
        
else:
    st.error("Projeto não encontrado. Por favor, selecione um projeto válido.")
