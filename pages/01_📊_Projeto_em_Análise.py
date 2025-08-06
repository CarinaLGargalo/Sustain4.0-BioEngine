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
            st.session_state.show_edit_form = True

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
    # Mostrar informações do projeto apenas se NÃO estivermos editando
    if not st.session_state.get('show_edit_form', False):
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
            # Compatibilidade com projetos antigos que usavam 'reference_flow_description'
            ref_time = selected_project.get('reference_flow_time_unit') or selected_project.get('reference_flow_description', '')
            if ref_flow != 'N/A' and ref_unit and ref_time:
                reference_flow_display = f"{ref_flow} {ref_unit}/{ref_time}"
            else:
                reference_flow_display = ref_flow
            st.markdown(f"**🔄 Reference Flow:** {reference_flow_display}")
            st.markdown(f"**🏭 System Boundaries:** {selected_project.get('system_boundaries', 'N/A')}")
            st.markdown(f"**🎛️ Product/System:** {selected_project.get('product_system', 'N/A')}")
            
            # Exibir Functional Unit - compatibilidade com projetos antigos e novos
            functional_unit_unit = selected_project.get('functional_unit_unit')
            functional_unit_object = selected_project.get('functional_unit_object')
            if functional_unit_unit and functional_unit_object:
                functional_unit_display = f"{functional_unit_unit} of {functional_unit_object}"
            else:
                # Compatibilidade com projetos antigos
                functional_unit_display = selected_project.get('functional_unit', 'N/A')
            st.markdown(f"**📐 Functional Unit:** {functional_unit_display}")
            
            st.markdown(f"**🌍 Region:** {selected_project.get('region', 'N/A')}")
        
        # Informações de Absolute Sustainability (se aplicável)
        if selected_project.get('sharing_principle') and selected_project.get('reason_sharing_principle'):
            st.markdown("---")
            st.markdown("**🌱 Absolute Sustainability Study:** Yes")
            st.markdown(f"**📊 Sharing Principle:** {selected_project.get('sharing_principle', 'N/A')}")
            st.markdown(f"**💡 Reason:** {selected_project.get('reason_sharing_principle', 'N/A')}")
        
        # Mostrar figura do System Boundaries se disponível
        if selected_project.get('system_boundaries_figure'):
            with st.expander("🖼️ System Boundaries Figure"):
                try:
                    st.image(selected_project['system_boundaries_figure'], caption="System Boundaries Diagram")
                except:
                    st.info("Figura salva mas não pode ser exibida no momento.")
        
        st.markdown("---")
        
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

# Inicializar estado para edição se não existir
if 'show_edit_form' not in st.session_state:
    st.session_state.show_edit_form = False

# Formulário de edição (se estiver editando)
if st.session_state.get('show_edit_form') and selected_project:
    
    # Importar funções necessárias do utils
    from utils import save_user_data
    
    # Inicializar valores no session_state para edição se não existirem
    if 'edit_product_system' not in st.session_state:
        # Mapear valores antigos para novos valores simplificados
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
        # Verificar se tem os campos separados, senão tentar extrair do campo funcional_unit antigo
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
    
    # Layout: Form à esquerda, campos dinâmicos à direita
    edit_form_col, edit_dynamic_col = st.columns([2, 1])
    
    with edit_form_col:
        with st.form(key="edit_project_form_analysis", border=False):
            st.markdown("### ✏️ Editar Projeto")
            # Campos básicos
            edit_name = st.text_input("Project Name", value=selected_project['name'])
            edit_goal = st.text_input("Goal Statement", value=selected_project.get('goal_statement', selected_project.get('description', '')))
            edit_application = st.text_input("Intended Application", value=selected_project.get('intended_application', ''))
            
            col1, col2 = st.columns(2)
            with col1:
                # Tratamento seguro para selectbox com índices
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
                # Compatibilidade com projetos antigos que usavam 'reference_flow_description'
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
            
            # Botões do formulário sem aninhamento de colunas
            submit_edit = st.form_submit_button("💾 Salvar Alterações", use_container_width=True)
            cancel_edit = st.form_submit_button("❌ Cancelar", use_container_width=True)
    
    with edit_dynamic_col:
        st.markdown("### Configurações do Produto")
        
        # Product system fora do form para permitir reatividade
        edit_product = st.selectbox("Product/system to be studied", 
                                    ["Biofuels", "Food Products", "Building Materials", 
                                     "Electronics", "Chemicals", "Energy Systems"],
                                    key="edit_product_system")
        
        # Functional Unit também fora do form para reatividade
        st.write("**Functional Unit**")
        
        # Options para Unit baseadas no product system
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
    
    # Processar submit do formulário
    # Processar submit do formulário
    if submit_edit:
        # Encontrar o índice do projeto atual na lista de projetos do usuário
        user_projects = st.session_state.user_projects.get(username, [])
        project_index = None
        for idx, project in enumerate(user_projects):
            if project.get('key_code') == selected_project.get('key_code'):
                project_index = idx
                break
        
        if project_index is not None:
            # Atualizar projeto
            st.session_state.user_projects[username][project_index] = {
                'name': edit_name,
                'key_code': selected_project.get('key_code', '000000'),  # Manter código existente
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
            
            # Atualizar também o projeto atual na sessão
            st.session_state.current_project = st.session_state.user_projects[username][project_index]
            
            # Salvar dados
            user_data = {
                'projects': st.session_state.user_projects[username],
                'preferences': {
                    'theme': st.session_state.theme,
                    'notifications': st.session_state.notifications
                },
                'last_update': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            save_user_data(username, user_data)
            
            st.success("✅ Projeto atualizado com sucesso!")
            st.session_state.show_edit_form = False
            st.rerun()
        else:
            st.error("❌ Erro ao encontrar o projeto para atualização.")
    
    if cancel_edit:
        st.session_state.show_edit_form = False
        st.rerun()
