# 🌿Sustain 4.0 - BioEngine

Uma plataforma integrada de análise de sustentabilidade ambiental, fornecendo uma interface intuitiva para pesquisadores e analistas ambientais.

## Execute app

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sustain4o-bioengine.streamlit.app/)

## Características

- 🔒 Sistema de autenticação de usuários
- 📊 Visualização de dados ambientais
- 📁 Gestão de projetos com persistência de dados
- ⚙️ Configurações personalizadas por usuário
- 🌍 Suporte a diferentes tipos de projetos ambientais

## Sistema de Persistência de Dados

O sistema implementa persistência de dados para as seguintes informações:

- Projetos criados pelo usuário
- Preferências personalizadas (tema, notificações, etc.)
- Configurações do sistema
- Estado da sessão entre logins

Os dados são armazenados nos seguintes locais:

- `config.yaml` - Configurações globais e informações de usuário
- `data/[username].json` - Dados específicos por usuário (projetos, preferências, etc.)
