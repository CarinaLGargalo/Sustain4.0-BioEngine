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
    background: linear-gradient(rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.4)),
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

# Cabeçalho da página
st.header("📊 Projeto em Análise")

# Verificar se há projetos disponíveis
username = st.session_state.username
user_projects = st.session_state.user_projects.get(username, [])

if not user_projects:
    st.warning("Você ainda não tem projetos. Crie um projeto na página principal.")
    st.stop()

# Selecionar projeto para análise
project_names = [project['name'] for project in user_projects]
selected_project_name = st.selectbox("Selecione um projeto para análise:", project_names)

# Encontrar o projeto selecionado
selected_project = next((p for p in user_projects if p['name'] == selected_project_name), None)

if selected_project:
    # Exibir informações do projeto
    st.subheader(f"Análise do Projeto: {selected_project['name']}")
    
    # Criar abas para diferentes análises
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Visão Geral", "🌱 Biodiversidade", "🌡️ Carbono", "💧 Água"])
    
    with tab1:
        st.write("### Visão Geral do Projeto")
        
        # Informações básicas
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Tipo:** {selected_project['type']}")
            st.write(f"**Data de Início:** {selected_project['date'].split('T')[0] if isinstance(selected_project['date'], str) else selected_project['date']}")
            if 'description' in selected_project and selected_project['description']:
                st.write(f"**Descrição:** {selected_project['description']}")
                
        with col2:
            # Métricas de exemplo (substituir por dados reais quando disponíveis)
            st.metric(label="Índice de Sustentabilidade", value="78%", delta="4%")
            st.metric(label="Dias Ativos", value="45", delta="2")
            
        # Gráfico de exemplo
        st.write("### Tendências ao Longo do Tempo")
        
        # Dados fictícios para demonstração
        dates = pd.date_range(start='2025-01-01', periods=30, freq='D')
        metrics = {
            'Índice de Biodiversidade': np.random.normal(75, 5, 30).cumsum() / 50 + 70,
            'Captura de Carbono (kg)': np.random.normal(30, 10, 30).cumsum() / 10 + 100,
            'Qualidade da Água': np.random.normal(85, 3, 30).cumsum() / 100 + 80
        }
        
        demo_data = pd.DataFrame({
            'Data': dates,
            **metrics
        })
        
        # Permitir que o usuário escolha a métrica para visualizar
        metric_to_show = st.selectbox(
            "Selecione a métrica para visualizar:",
            list(metrics.keys())
        )
        
        # Criar gráfico
        fig = px.line(
            demo_data, 
            x='Data', 
            y=metric_to_show,
            markers=True,
            title=f"Evolução de {metric_to_show} ao Longo do Tempo"
        )
        
        fig.update_layout(
            xaxis_title="Data",
            yaxis_title=metric_to_show,
            height=400,
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Observações
        st.write("### Observações")
        
        # Dados fictícios para observações
        observations = [
            {"date": "2025-07-25", "text": "Aumento significativo na diversidade de espécies."},
            {"date": "2025-07-15", "text": "Implementação de novos métodos de coleta de dados."},
            {"date": "2025-07-10", "text": "Chuva forte impactou temporariamente as medições."}
        ]
        
        for obs in observations:
            st.info(f"**{obs['date']}:** {obs['text']}")
            
    with tab2:
        st.write("### Análise de Biodiversidade")
        
        if selected_project['type'] == "Análise de Biodiversidade":
            # Conteúdo específico para projetos de biodiversidade
            st.write("Aqui serão exibidos dados detalhados sobre biodiversidade do seu projeto.")
            
            # Gráfico de exemplo - diversidade de espécies
            species_data = {
                'Categoria': ['Plantas', 'Insetos', 'Aves', 'Mamíferos', 'Répteis', 'Anfíbios'],
                'Contagem': [45, 78, 23, 14, 8, 12],
                'Índice Shannon': [3.8, 4.2, 2.9, 2.7, 1.8, 2.1]
            }
            
            species_df = pd.DataFrame(species_data)
            
            # Gráfico de barras
            bar_fig = px.bar(
                species_df,
                x='Categoria',
                y='Contagem',
                color='Índice Shannon',
                color_continuous_scale='Viridis',
                title="Diversidade de Espécies por Categoria"
            )
            
            st.plotly_chart(bar_fig, use_container_width=True)
            
            # Mapa de calor (simulado)
            st.write("### Mapa de Distribuição de Espécies")
            st.write("Mapa interativo mostrando onde as diferentes espécies foram encontradas.")
            
            # Simulação de um mapa - substituir com dados reais e mapa real
            st.image("https://via.placeholder.com/800x400?text=Mapa+de+Distribuição+de+Espécies", 
                    caption="Mapa de distribuição de espécies (ilustrativo)")
        else:
            st.info("Este projeto não é focado em análise de biodiversidade. Selecione um projeto desse tipo para ver análises detalhadas.")
    
    with tab3:
        st.write("### Análise de Carbono")
        
        if selected_project['type'] == "Monitoramento de Carbono":
            # Conteúdo específico para projetos de carbono
            st.write("Aqui serão exibidos dados detalhados sobre carbono do seu projeto.")
            
            # Dados fictícios para demonstração
            carbon_data = {
                'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul'],
                'Emissão (ton CO2)': [120, 132, 145, 130, 125, 110, 105],
                'Captura (ton CO2)': [90, 95, 105, 115, 120, 125, 130]
            }
            
            carbon_df = pd.DataFrame(carbon_data)
            
            # Calculando balanço de carbono
            carbon_df['Balanço (ton CO2)'] = carbon_df['Emissão (ton CO2)'] - carbon_df['Captura (ton CO2)']
            
            # Gráfico de linha com duas métricas
            carbon_fig = go.Figure()
            
            carbon_fig.add_trace(go.Scatter(
                x=carbon_df['Mês'],
                y=carbon_df['Emissão (ton CO2)'],
                mode='lines+markers',
                name='Emissão CO2',
                line=dict(color='red')
            ))
            
            carbon_fig.add_trace(go.Scatter(
                x=carbon_df['Mês'],
                y=carbon_df['Captura (ton CO2)'],
                mode='lines+markers',
                name='Captura CO2',
                line=dict(color='green')
            ))
            
            carbon_fig.update_layout(
                title="Emissão vs. Captura de CO2",
                xaxis_title="Mês",
                yaxis_title="Toneladas de CO2",
                height=400,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(carbon_fig, use_container_width=True)
            
            # Balanço de carbono
            st.write("### Balanço de Carbono")
            
            # Gráfico de balanço
            balance_fig = px.bar(
                carbon_df,
                x='Mês',
                y='Balanço (ton CO2)',
                color='Balanço (ton CO2)',
                color_continuous_scale=['green', 'yellow', 'red'],
                title="Balanço Mensal de Carbono (Emissão - Captura)"
            )
            
            st.plotly_chart(balance_fig, use_container_width=True)
            
            # Métricas importantes
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="Emissão Total", 
                    value=f"{carbon_df['Emissão (ton CO2)'].sum()} ton",
                    delta="-3%"
                )
                
            with col2:
                st.metric(
                    label="Captura Total", 
                    value=f"{carbon_df['Captura (ton CO2)'].sum()} ton",
                    delta="8%"
                )
                
            with col3:
                balance = carbon_df['Emissão (ton CO2)'].sum() - carbon_df['Captura (ton CO2)'].sum()
                st.metric(
                    label="Balanço Final", 
                    value=f"{balance} ton",
                    delta="-15%" if balance < 0 else "15%",
                    delta_color="normal" if balance < 0 else "inverse"
                )
        else:
            st.info("Este projeto não é focado em monitoramento de carbono. Selecione um projeto desse tipo para ver análises detalhadas.")
    
    with tab4:
        st.write("### Análise de Qualidade da Água")
        
        if selected_project['type'] == "Qualidade da Água":
            # Conteúdo específico para projetos de qualidade da água
            st.write("Aqui serão exibidos dados detalhados sobre qualidade da água do seu projeto.")
            
            # Dados fictícios para demonstração
            water_data = {
                'Parâmetro': ['pH', 'Turbidez', 'Oxigênio Dissolvido', 'Nitratos', 'Fosfatos', 'Coliformes'],
                'Valor': [7.2, 12, 8.5, 4.3, 0.8, 230],
                'Limite': [6.5, 40, 5.0, 10.0, 1.0, 500],
                'Unidade': ['pH', 'NTU', 'mg/L', 'mg/L', 'mg/L', 'UFC/100mL']
            }
            
            water_df = pd.DataFrame(water_data)
            
            # Calcular porcentagem do limite
            water_df['% do Limite'] = (water_df['Valor'] / water_df['Limite'] * 100).round(1)
            
            # Criar tabela com dados
            st.write("### Parâmetros de Qualidade da Água")
            st.dataframe(water_df, hide_index=True)
            
            # Criar gráfico de gauge
            st.write("### Índice de Qualidade da Água")
            
            # Calcular IQA fictício
            iqa = 85  # 0-100
            
            gauge_fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = iqa,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Índice de Qualidade da Água"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "red"},
                        {'range': [50, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': iqa
                    }
                }
            ))
            
            gauge_fig.update_layout(height=300)
            st.plotly_chart(gauge_fig, use_container_width=True)
            
            # Tendências temporais
            st.write("### Tendências Temporais")
            
            # Criar dados fictícios para demonstração
            dates = pd.date_range(start='2025-01-01', periods=15, freq='D')
            ph_values = [7.1, 7.0, 7.2, 7.3, 7.1, 7.0, 6.9, 7.0, 7.1, 7.2, 7.4, 7.3, 7.2, 7.1, 7.0]
            oxygen_values = [8.3, 8.2, 8.4, 8.5, 8.6, 8.4, 8.2, 8.1, 8.3, 8.5, 8.7, 8.6, 8.5, 8.4, 8.3]
            
            trend_data = pd.DataFrame({
                'Data': dates,
                'pH': ph_values,
                'Oxigênio Dissolvido (mg/L)': oxygen_values
            })
            
            # Parâmetro a mostrar
            param_to_show = st.selectbox(
                "Selecione o parâmetro para visualizar:",
                ['pH', 'Oxigênio Dissolvido (mg/L)']
            )
            
            # Criar gráfico de linha
            trend_fig = px.line(
                trend_data,
                x='Data',
                y=param_to_show,
                markers=True,
                title=f"Tendência de {param_to_show} ao Longo do Tempo"
            )
            
            st.plotly_chart(trend_fig, use_container_width=True)
        else:
            st.info("Este projeto não é focado em qualidade da água. Selecione um projeto desse tipo para ver análises detalhadas.")
    
    # Seção para notas e observações
    st.write("### Notas e Observações")
    
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
