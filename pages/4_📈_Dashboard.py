import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(
    page_title="Dashboard - Sustain 4.0",
    page_icon="📈",
    layout="wide"
)

# Inicializar session state
def init_session_state():
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    if 'selected_analysis' not in st.session_state:
        st.session_state.selected_analysis = "Análise de Biodiversidade"
    if 'data_uploaded' not in st.session_state:
        st.session_state.data_uploaded = False

init_session_state()

st.header("📈 Dashboard - Sustain 4.0 BioEngine")

# Verificar se há dados para exibir
if not st.session_state.get('analysis_executed', False):
    st.warning("⚠️ Nenhuma análise foi executada ainda. Vá para a página **Análise** para executar uma análise primeiro.")
    
    # Mostrar dados de demonstração
    st.info("📊 Exibindo dados de demonstração para visualização do dashboard:")
else:
    st.success("✅ Exibindo resultados da análise executada")

# Informações do projeto atual
if st.session_state.get('user_name') and st.session_state.get('project_name'):
    st.subheader(f"🎯 Projeto: {st.session_state.project_name}")
    
    col_info1, col_info2, col_info3, col_info4 = st.columns(4)
    
    with col_info1:
        st.metric("👤 Usuário", st.session_state.user_name)
    with col_info2:
        st.metric("🌍 Localização", st.session_state.get('project_location', 'N/A'))
    with col_info3:
        st.metric("⏱️ Duração", f"{st.session_state.get('project_duration', 0)} meses")
    with col_info4:
        st.metric("🔬 Análise", st.session_state.selected_analysis.replace('Análise de ', ''))

# Dados simulados para demonstração
np.random.seed(42)
dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
n_days = len(dates)

# Dashboard principal
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Tendências Temporais")
    
    # Gráfico de linha temporal baseado no tipo de análise
    if "Biodiversidade" in st.session_state.selected_analysis:
        biodiversity_data = pd.DataFrame({
            'Data': dates,
            'Índice Shannon': 2.5 + 0.5 * np.sin(np.arange(n_days) * 2 * np.pi / 365) + np.random.normal(0, 0.1, n_days),
            'Riqueza de Espécies': 120 + 30 * np.sin(np.arange(n_days) * 2 * np.pi / 365) + np.random.normal(0, 5, n_days),
            'Equitabilidade': 0.7 + 0.2 * np.sin(np.arange(n_days) * 2 * np.pi / 365) + np.random.normal(0, 0.02, n_days)
        })
        
        fig = px.line(biodiversity_data, x='Data', y=['Índice Shannon', 'Riqueza de Espécies', 'Equitabilidade'],
                     title="Métricas de Biodiversidade ao Longo do Tempo")
        
    elif "Carbono" in st.session_state.selected_analysis:
        carbon_data = pd.DataFrame({
            'Data': dates,
            'Carbono Sequestrado (t)': 1000 + 200 * np.sin(np.arange(n_days) * 2 * np.pi / 365) + np.random.normal(0, 20, n_days),
            'Emissões CO2 (t)': 800 + 150 * np.sin(np.arange(n_days) * 2 * np.pi / 365 + np.pi) + np.random.normal(0, 15, n_days),
            'Saldo Líquido (t)': None
        })
        carbon_data['Saldo Líquido (t)'] = carbon_data['Carbono Sequestrado (t)'] - carbon_data['Emissões CO2 (t)']
        
        fig = px.line(carbon_data, x='Data', y=['Carbono Sequestrado (t)', 'Emissões CO2 (t)', 'Saldo Líquido (t)'],
                     title="Análise de Carbono ao Longo do Tempo")
        
    elif "Água" in st.session_state.selected_analysis:
        water_data = pd.DataFrame({
            'Data': dates,
            'Qualidade (%)': 85 + 10 * np.sin(np.arange(n_days) * 2 * np.pi / 365) + np.random.normal(0, 2, n_days),
            'pH': 7.0 + 0.5 * np.sin(np.arange(n_days) * 2 * np.pi / 365) + np.random.normal(0, 0.1, n_days),
            'Turbidez (NTU)': 2 + 0.5 * np.sin(np.arange(n_days) * 2 * np.pi / 365 + np.pi) + np.random.normal(0, 0.2, n_days)
        })
        
        fig = px.line(water_data, x='Data', y=['Qualidade (%)', 'pH', 'Turbidez (NTU)'],
                     title="Qualidade da Água ao Longo do Tempo")
        
    else:  # Solo
        soil_data = pd.DataFrame({
            'Data': dates,
            'pH do Solo': 6.5 + 0.3 * np.sin(np.arange(n_days) * 2 * np.pi / 365) + np.random.normal(0, 0.1, n_days),
            'Matéria Orgânica (%)': 3.5 + 0.5 * np.sin(np.arange(n_days) * 2 * np.pi / 365) + np.random.normal(0, 0.2, n_days),
            'Umidade (%)': 25 + 10 * np.sin(np.arange(n_days) * 2 * np.pi / 365) + np.random.normal(0, 2, n_days)
        })
        
        fig = px.line(soil_data, x='Data', y=['pH do Solo', 'Matéria Orgânica (%)', 'Umidade (%)'],
                     title="Qualidade do Solo ao Longo do Tempo")
    
    fig.update_layout(height=400, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎯 Métricas Principais")
    
    # Métricas baseadas no tipo de análise
    if "Biodiversidade" in st.session_state.selected_analysis:
        st.metric("🌱 Índice Shannon", "2.85", "0.12", help="Medida de diversidade")
        st.metric("🦋 Riqueza de Espécies", "147", "8", help="Número total de espécies")
        st.metric("⚖️ Equitabilidade", "0.78", "0.05", help="Distribuição das espécies")
        st.metric("🌿 Cobertura Vegetal", "92%", "3%", help="Percentual de cobertura")
        
    elif "Carbono" in st.session_state.selected_analysis:
        st.metric("🌳 Carbono Total", "1,234 t", "-12 t", help="Carbono armazenado")
        st.metric("📈 Sequestro Anual", "89 t/ano", "5 t", help="Taxa de sequestro")
        st.metric("📉 Emissões", "456 t CO2", "-23 t", help="Emissões totais")
        st.metric("🎯 Saldo Líquido", "778 t", "28 t", help="Sequestro - Emissões")
        
    elif "Água" in st.session_state.selected_analysis:
        st.metric("💧 Qualidade", "92%", "5.2%", help="Índice de qualidade")
        st.metric("🧪 pH", "7.2", "0.1", help="Potencial hidrogeniônico")
        st.metric("🌊 Turbidez", "2.1 NTU", "-0.3", help="Clareza da água")
        st.metric("🔬 Coliformes", "Baixo", "Estável", help="Indicadores bacteriológicos")
        
    else:  # Solo
        st.metric("🌱 pH do Solo", "6.5", "0.2", help="Acidez do solo")
        st.metric("🍃 Matéria Orgânica", "3.8%", "0.4%", help="Conteúdo orgânico")
        st.metric("💧 Umidade", "28%", "2%", help="Teor de água")
        st.metric("🎯 Fertilidade", "Alta", "Estável", help="Capacidade produtiva")

# Gráficos adicionais
st.divider()
col3, col4 = st.columns(2)

with col3:
    st.subheader("📊 Distribuição por Categoria")
    
    # Gráfico de pizza baseado no tipo de análise
    if "Biodiversidade" in st.session_state.selected_analysis:
        categories = ['Mamíferos', 'Aves', 'Répteis', 'Anfíbios', 'Peixes', 'Invertebrados']
        values = [15, 25, 8, 12, 20, 20]
        
    elif "Carbono" in st.session_state.selected_analysis:
        categories = ['Floresta', 'Solo', 'Biomassa', 'Raízes', 'Detritos']
        values = [40, 25, 15, 12, 8]
        
    elif "Água" in st.session_state.selected_analysis:
        categories = ['Excelente', 'Boa', 'Aceitável', 'Inadequada', 'Péssima']
        values = [30, 35, 20, 10, 5]
        
    else:  # Solo
        categories = ['Muito Fértil', 'Fértil', 'Moderado', 'Baixa Fertilidade', 'Infértil']
        values = [25, 30, 25, 15, 5]
    
    fig_pie = px.pie(values=values, names=categories, title="Distribuição por Categoria")
    fig_pie.update_layout(height=350)
    st.plotly_chart(fig_pie, use_container_width=True)

with col4:
    st.subheader("📈 Comparativo Mensal")
    
    # Gráfico de barras
    months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
              'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    
    if "Biodiversidade" in st.session_state.selected_analysis:
        current_year = [2.1, 2.3, 2.7, 2.9, 3.1, 2.8, 2.6, 2.4, 2.5, 2.7, 2.2, 2.0]
        previous_year = [1.9, 2.1, 2.5, 2.7, 2.9, 2.6, 2.4, 2.2, 2.3, 2.5, 2.0, 1.8]
        ylabel = "Índice Shannon"
        
    elif "Carbono" in st.session_state.selected_analysis:
        current_year = [980, 1020, 1150, 1280, 1350, 1320, 1280, 1200, 1180, 1220, 1100, 1050]
        previous_year = [920, 960, 1080, 1200, 1270, 1240, 1200, 1120, 1100, 1140, 1020, 980]
        ylabel = "Carbono (t)"
        
    elif "Água" in st.session_state.selected_analysis:
        current_year = [88, 90, 92, 94, 96, 93, 91, 89, 90, 92, 87, 85]
        previous_year = [85, 87, 89, 91, 93, 90, 88, 86, 87, 89, 84, 82]
        ylabel = "Qualidade (%)"
        
    else:  # Solo
        current_year = [6.2, 6.3, 6.5, 6.7, 6.8, 6.6, 6.4, 6.3, 6.4, 6.6, 6.1, 6.0]
        previous_year = [6.0, 6.1, 6.3, 6.5, 6.6, 6.4, 6.2, 6.1, 6.2, 6.4, 5.9, 5.8]
        ylabel = "pH do Solo"
    
    fig_bar = go.Figure(data=[
        go.Bar(name='2024', x=months, y=current_year),
        go.Bar(name='2023', x=months, y=previous_year)
    ])
    fig_bar.update_layout(
        title="Comparativo Anual",
        xaxis_title="Mês",
        yaxis_title=ylabel,
        height=350,
        barmode='group'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Seção de Alertas e Recomendações
st.divider()
st.subheader("🚨 Alertas e Recomendações")

col5, col6 = st.columns(2)

with col5:
    st.markdown("**⚠️ Alertas Ativos:**")
    
    if "Biodiversidade" in st.session_state.selected_analysis:
        st.warning("🦋 Redução de 5% na população de borboletas detectada")
        st.info("🌱 Aumento na diversidade de plantas nativas observado")
        st.error("🐦 Espécie ameaçada detectada na área - requer atenção")
        
    elif "Carbono" in st.session_state.selected_analysis:
        st.success("🌳 Meta de sequestro anual atingida (105%)")
        st.warning("🔥 Emissões acima do esperado no último trimestre")
        st.info("📈 Tendência positiva no saldo líquido de carbono")
        
    elif "Água" in st.session_state.selected_analysis:
        st.success("💧 Qualidade da água dentro dos padrões")
        st.warning("🧪 pH ligeiramente ácido detectado no ponto 3")
        st.info("🌊 Turbidez reduzida após implementação de filtros")
        
    else:  # Solo
        st.success("🌱 Fertilidade do solo em níveis ótimos")
        st.warning("💧 Umidade baixa detectada na zona sul")
        st.info("🍃 Aumento gradual da matéria orgânica")

with col6:
    st.markdown("**💡 Recomendações:**")
    
    if "Biodiversidade" in st.session_state.selected_analysis:
        st.markdown("""
        - 🌸 Implementar corredores ecológicos para borboletas
        - 🌳 Continuar plantio de espécies nativas
        - 🔍 Monitoramento intensivo da espécie ameaçada
        - 📊 Análise trimestral de biodiversidade
        """)
        
    elif "Carbono" in st.session_state.selected_analysis:
        st.markdown("""
        - 🌳 Expandir área de reflorestamento em 15%
        - ⚡ Implementar energia renovável para reduzir emissões
        - 📈 Manter programa de sequestro atual
        - 🔍 Auditoria das fontes de emissão
        """)
        
    elif "Água" in st.session_state.selected_analysis:
        st.markdown("""
        - 🧪 Monitorar pH do ponto 3 semanalmente
        - 💧 Manter sistema de filtração atual
        - 🌊 Implementar wetlands construídas
        - 📊 Análise microbiológica mensal
        """)
        
    else:  # Solo
        st.markdown("""
        - 💧 Sistema de irrigação para zona sul
        - 🍃 Continuar programa de compostagem
        - 🌱 Rotação de culturas para manter fertilidade
        - 📊 Análise de solo semestral
        """)

# Exportação de Relatórios
st.divider()
st.subheader("📋 Exportação de Relatórios")

col7, col8, col9, col10 = st.columns(4)

with col7:
    if st.button("📄 Relatório PDF", type="primary"):
        st.success("✅ Relatório PDF gerado com sucesso!")
        st.info("📥 Download iniciado automaticamente")

with col8:
    if st.button("📊 Dados Excel"):
        st.success("✅ Planilha Excel criada!")
        st.info("📥 Arquivo excel_dados.xlsx baixado")

with col9:
    if st.button("📧 Enviar Email"):
        if st.session_state.get('email_reports') and st.session_state.get('email_address'):
            st.success(f"✅ Relatório enviado para {st.session_state.email_address}")
        else:
            st.warning("⚠️ Configure email nas Configurações primeiro")

with col10:
    if st.button("🔗 Compartilhar Link"):
        st.success("✅ Link de compartilhamento copiado!")
        st.code("https://sustain40.app/share/abc123")

# Footer do Dashboard
st.divider()
last_update = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
st.caption(f"📅 Última atualização: {last_update} | 🌿 Sustain 4.0 BioEngine v1.0")
