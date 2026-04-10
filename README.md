# 🌿Sustain 4.0 - BioEngine

Uma plataforma integrada de análise de sustentabilidade ambiental, fornecendo uma interface intuitiva para pesquisadores e analistas ambientais.

## Execute app

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sustain4o-bioengine.streamlit.app/)

## Características

- 🔒 Autenticação com Google OIDC (`st.login`, `st.user`, `st.logout`)
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

- `config.yaml` - Somente configurações não sensíveis do aplicativo
- `data/app_data.db` - Banco SQLite com perfis e projetos por `user_id` (OIDC `sub`)

## Configuração de Autenticação (Google OIDC)

As credenciais e segredos de autenticação não devem ficar em `config.yaml`.

1. Copie `.streamlit/secrets.toml.example` para `.streamlit/secrets.toml`.
2. Preencha `client_id`, `client_secret` e `cookie_secret`.
3. Ajuste `redirect_uri` para o ambiente (local ou produção).
4. Mantenha `server_metadata_url` apontando para o provedor OIDC.

Exemplo:

```toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "<long-random-secret>"
client_id = "<google-client-id>"
client_secret = "<google-client-secret>"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

`.streamlit/secrets.toml` está ignorado no versionamento por segurança.
