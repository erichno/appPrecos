# 🛒 MelhorPreço - Comparador de Preços de Supermercados

[![CI Status](https://github.com/erichno/appPrecos/workflows/CI%20-%20Continuous%20Integration/badge.svg)](https://github.com/erichno/appPrecos/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![React 19](https://img.shields.io/badge/react-19.0-blue.svg)](https://react.dev/)

> Encontre os melhores preços de produtos em supermercados da sua cidade! 🎯

## 📋 Sobre o Projeto

**MelhorPreço** é uma aplicação web/mobile (PWA) que permite aos usuários comparar preços de produtos em diferentes supermercados de forma rápida e intuitiva. O sistema combina dados de três fontes:

- 🤖 **Web Scraping** automatizado (quando permitido)
- 🔌 **APIs de parceiros** (supermercados com integração)
- 👥 **Crowdsourcing** (usuários contribuem com preços)

## ✨ Features

### 🎯 Core MVP (Implementado)

- ✅ **Busca Inteligente**: Autocomplete com normalização de texto, correção de digitação e sinônimos
- ✅ **Comparação de Preços**: Visualize o menor preço em destaque com ranking de supermercados
- ✅ **Histórico de Preços**: Gráficos interativos mostrando variação de preços nos últimos 30 dias
- ✅ **Geolocalização**: Selecione sua cidade para ver preços locais
- ✅ **Autenticação**: Sistema de login/registro com JWT
- ✅ **Favoritos**: Salve produtos e supermercados favoritos
- ✅ **Alertas de Preço**: Receba notificações quando o preço baixar
- ✅ **Crowdsourcing**: Usuários podem enviar preços com fotos de etiquetas

### 🚀 Em Desenvolvimento

- 🔜 Upload de fotos com validação OCR
- 🔜 Sistema de gamificação e reputação
- 🔜 Notificações push
- 🔜 App nativo (React Native)
- 🔜 Integração com APIs de supermercados
- 🔜 Sistema de moderação de preços

## 🛠️ Stack Tecnológica

### Backend
- **Framework**: FastAPI 0.110.1
- **Banco de Dados**: MongoDB (Motor async driver)
- **Autenticação**: JWT + bcrypt
- **Validação**: Pydantic v2
- **Python**: 3.11

### Frontend
- **Framework**: React 19
- **Roteamento**: React Router 7
- **Estilo**: Tailwind CSS 3.4
- **UI Components**: Radix UI
- **Gráficos**: Recharts 3.6
- **Notificações**: Sonner
- **HTTP Client**: Axios

### DevOps & CI/CD
- **CI/CD**: GitHub Actions
- **Containerização**: Docker (opcional)
- **Deploy**: Vercel (frontend) + Railway/Render (backend)
- **Monitoramento**: Sentry (opcional)

## 📦 Instalação

### Pré-requisitos

- Python 3.11+
- Node.js 20+
- MongoDB 7.0+
- Yarn 1.22+

### 1. Clone o repositório

```bash
git clone https://github.com/erichno/appPrecos.git
cd appPrecos
```

### 2. Configure o Backend

```bash
cd backend

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas configurações

# Execute seed data (popular banco)
python scripts/seed_data.py

# Inicie o servidor
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

**Backend rodando em**: http://localhost:8001

### 3. Configure o Frontend

```bash
cd frontend

# Instale dependências
yarn install

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env:
# REACT_APP_BACKEND_URL=http://localhost:8001

# Inicie o app
yarn start
```

**Frontend rodando em**: http://localhost:3000

## 🔧 Configuração

### Backend `.env`

```bash
MONGO_URL=mongodb://localhost:27017
DB_NAME=melhorpreco_db
SECRET_KEY=your-secret-key-change-in-production
CORS_ORIGINS=http://localhost:3000,https://melhorpreco.com
```

### Frontend `.env`

```bash
REACT_APP_BACKEND_URL=http://localhost:8001
```

## 🗄️ Banco de Dados

### Seed Data

O projeto inclui dados fictícios para desenvolvimento:

- **1 cidade**: São Paulo
- **5 supermercados**: Pão de Açúcar, Carrefour, Extra, Dia%, Assaí
- **50 produtos**: Categorias variadas (laticínios, grãos, bebidas, higiene, etc)
- **200+ ofertas**: Preços variados com promoções

Execute:
```bash
cd backend
python scripts/seed_data.py
```

### Modelo de Dados

```
Users → Favoritos, Alertas
Cities → Localização
Supermarkets → Endereço, Horários, Avaliações
Products → Categorias, Marcas, EAN
Offers → Preços por mercado + data de coleta
PriceHistory → Histórico para gráficos
```

## 🚀 Deploy

### GitHub Actions (Automático)

O projeto inclui 3 workflows:

1. **CI (Continuous Integration)**
   - Roda em cada push/PR
   - Testa backend (Python lint, testes)
   - Testa frontend (ESLint, build)
   - Scan de segurança

2. **CD (Continuous Deployment)**
   - Deploy automático na branch `main`
   - Backend → Railway/Render
   - Frontend → Vercel/Netlify

3. **PR Preview**
   - Deploy de preview para cada Pull Request

### Configurar Secrets no GitHub

Vá em: **Settings → Secrets and variables → Actions**

#### Para Vercel (Frontend):
```
VERCEL_TOKEN=your_vercel_token
VERCEL_ORG_ID=your_org_id
VERCEL_PROJECT_ID=your_project_id
BACKEND_URL=https://api.melhorpreco.com
```

#### Para Railway (Backend):
```
RAILWAY_TOKEN=your_railway_token
RAILWAY_PROJECT_ID=your_project_id
```

#### Para Render (Backend):
```
RENDER_API_KEY=your_render_api_key
RENDER_SERVICE_ID=your_service_id
```

### Deploy Manual

#### Frontend (Vercel)
```bash
cd frontend
vercel --prod
```

#### Backend (Railway)
```bash
cd backend
railway up
```

## 📚 API Endpoints

### Autenticação
```
POST   /api/auth/register   - Criar conta
POST   /api/auth/login      - Login
GET    /api/auth/me         - Perfil do usuário
```

### Cidades
```
GET    /api/cities          - Listar cidades
GET    /api/cities/{id}     - Buscar cidade por ID
```

### Produtos
```
GET    /api/products/search?q={query}&city_id={id}  - Buscar produtos
GET    /api/products/{id}                            - Detalhes do produto
GET    /api/products/{id}/history?days=30            - Histórico de preços
```

### Ofertas
```
GET    /api/offers?product_id={id}&city_id={id}     - Ofertas de um produto
POST   /api/offers                                    - Criar oferta (crowdsourcing)
```

### Supermercados
```
GET    /api/supermarkets?city_id={id}               - Listar supermercados
GET    /api/supermarkets/{id}                        - Detalhes do supermercado
```

### Usuário
```
GET    /api/users/me/favorites                       - Listar favoritos
POST   /api/users/me/favorites                       - Adicionar favorito
DELETE /api/users/me/favorites/{type}/{id}           - Remover favorito

GET    /api/users/me/alerts                          - Listar alertas
POST   /api/users/me/alerts                          - Criar alerta
DELETE /api/users/me/alerts/{id}                     - Deletar alerta
```

**Documentação interativa**: http://localhost:8001/docs

## 🧪 Testes

### Backend
```bash
cd backend
pytest tests/ -v --cov
```

### Frontend
```bash
cd frontend
yarn test --coverage
```

### E2E (Playwright)
```bash
cd frontend
npx playwright test
```

## 📊 Estrutura do Projeto

```
appPrecos/
├── .github/
│   └── workflows/          # GitHub Actions
│       ├── ci.yml
│       ├── cd-deploy.yml
│       └── pr-preview.yml
├── backend/
│   ├── models/             # Modelos Pydantic
│   ├── routes/             # Endpoints da API
│   ├── services/           # Lógica de negócio
│   ├── scripts/            # Scripts utilitários
│   ├── server.py           # App principal
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── pages/          # Páginas/rotas
│   │   ├── context/        # Context API
│   │   ├── services/       # API client
│   │   └── App.js
│   └── package.json
└── README.md
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Regras

- ✅ Código deve passar no CI (lint + testes)
- ✅ Adicione testes para novas features
- ✅ Atualize a documentação
- ✅ Siga o padrão de código existente

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Erich** - [erichno](https://github.com/erichno)

## 🙏 Agradecimentos

- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Radix UI](https://www.radix-ui.com/)

## 📧 Contato

Dúvidas ou sugestões? Abra uma [issue](https://github.com/erichno/appPrecos/issues)!

---

**⭐ Se este projeto foi útil, dê uma estrela no GitHub!**
