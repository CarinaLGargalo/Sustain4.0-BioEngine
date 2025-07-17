# Sustain 4.0 - BioEngine

## Como Executar o Aplicativo

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar o Aplicativo
```bash
streamlit run streamlit_app.py
```

### 3. Navegação
O aplicativo será aberto no navegador (geralmente em `http://localhost:8501`).

Use a **sidebar** para navegar entre as páginas:
- **🌿 Sustain 4.0 - BioEngine**: Página principal com informações gerais
- **🏠 Home**: Configure informações do usuário e projeto
- **📊 Análise**: Execute análises de dados ambientais
- **⚙️ Configurações**: Ajuste preferências do sistema
- **📈 Dashboard**: Visualize resultados e métricas

### 4. Funcionalidades

#### Página Home
- Configuração de informações pessoais
- Definição de dados do projeto
- Localização e duração do projeto

#### Página Análise
- Upload de arquivos CSV
- Configuração de parâmetros de modelos
- Execução de análises de sustentabilidade
- Visualização de resultados

#### Página Configurações
- Preferências de interface (tema, idioma)
- Configurações de análise padrão
- Gerenciamento de dados e cache
- Exportação/importação de configurações

#### Página Dashboard
- Visualizações interativas com Plotly
- Métricas em tempo real
- Alertas e recomendações
- Exportação de relatórios

### 5. Persistência de Dados
Todos os dados são mantidos usando `st.session_state`, permitindo:
- Navegação entre páginas sem perda de dados
- Compartilhamento de informações entre seções
- Configurações persistentes durante a sessão

### 6. Estrutura do Projeto
```
Sustain4.0-BioEngine/
├── streamlit_app.py          # Página principal
├── requirements.txt          # Dependências
├── README.md                # Este arquivo
├── INSTRUCTIONS.md          # Instruções detalhadas
└── pages/                   # Páginas do aplicativo
    ├── 1_🏠_Home.py         # Configurações do usuário
    ├── 2_📊_Análise.py      # Análises de dados
    ├── 3_⚙️_Configurações.py # Configurações do sistema
    └── 4_📈_Dashboard.py    # Dashboard de resultados
```

### 7. Tipos de Análise Suportados
- **Análise de Biodiversidade**: Índices de diversidade, riqueza de espécies
- **Análise de Carbono**: Sequestro, emissões, saldo líquido
- **Análise de Água**: Qualidade, pH, turbidez
- **Análise de Solo**: Fertilidade, pH, matéria orgânica

### 8. Dicas de Uso
1. Comece pela página **Home** para configurar suas informações
2. Use a página **Análise** para fazer upload de dados e executar análises
3. Configure preferências na página **Configurações**
4. Visualize resultados no **Dashboard**
5. Todos os dados permanecem salvos durante a navegação entre páginas

### 9. Formato de Dados
Para upload de dados, use arquivos CSV com:
- Primeira linha contendo nomes das colunas
- Dados numéricos usando ponto (.) como separador decimal
- Mínimo de 50 amostras para melhores resultados

### 10. Funcionalidades Avançadas
- Exportação de configurações em JSON
- Importação de configurações salvas
- Limpeza seletiva de cache
- Validação cruzada para modelos ML
- Configurações de backup automático
