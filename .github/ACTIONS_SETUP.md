# GitHub Actions Setup Guide

## Configurar Deploy Automático

### 1. Secrets Necessários

Vá em: **GitHub → Settings → Secrets and variables → Actions → New repository secret**

#### Para Vercel (Frontend):

1. Instale Vercel CLI: `npm i -g vercel`
2. Faça login: `vercel login`
3. Link o projeto: `vercel link`
4. Obtenha os IDs: `vercel project ls`

Adicione estes secrets:
```
VERCEL_TOKEN=your_token_here
VERCEL_ORG_ID=team_xxxxxxxxxxxxx
VERCEL_PROJECT_ID=prj_xxxxxxxxxxxxx
BACKEND_URL=https://api.melhorpreco.com
```

#### Para Railway (Backend):

1. Acesse: https://railway.app/account/tokens
2. Crie um novo token
3. Obtenha o Project ID do dashboard

Adicione estes secrets:
```
RAILWAY_TOKEN=your_token_here
RAILWAY_PROJECT_ID=your_project_id
```

#### Para Render (Backend - Alternativa):

1. Acesse: https://dashboard.render.com/account/api-keys
2. Crie uma API Key
3. Obtenha o Service ID do seu serviço

Adicione estes secrets:
```
RENDER_API_KEY=your_api_key
RENDER_SERVICE_ID=srv-xxxxxxxxxxxxx
```

#### Para Netlify (Frontend - Alternativa):

1. Acesse: https://app.netlify.com/user/applications#personal-access-tokens
2. Crie um novo token
3. Obtenha o Site ID do seu site

Adicione estes secrets:
```
NETLIFY_AUTH_TOKEN=your_token
NETLIFY_SITE_ID=your_site_id
```

### 2. Testar Workflows

#### Testar CI (Push):
```bash
git add .
git commit -m "Test CI workflow"
git push
```

Verifique em: https://github.com/erichno/appPrecos/actions

#### Testar CD (Deploy):
O deploy automático acontece quando você faz push na branch `main`

#### Testar PR Preview:
```bash
git checkout -b feature/test
git push -u origin feature/test
# Crie um Pull Request no GitHub
```

### 3. Status Badges

Adicione ao README.md:

```markdown
[![CI Status](https://github.com/erichno/appPrecos/workflows/CI%20-%20Continuous%20Integration/badge.svg)](https://github.com/erichno/appPrecos/actions)
[![Deploy Status](https://github.com/erichno/appPrecos/workflows/CD%20-%20Deploy%20to%20Production/badge.svg)](https://github.com/erichno/appPrecos/actions)
```

### 4. Troubleshooting

**Erro: "Repository not found"**
- Verifique se o token tem permissão `repo`

**Erro: "Resource not accessible by integration"**
- Vá em Settings → Actions → General
- Em "Workflow permissions", selecione "Read and write permissions"

**Build falha no CI:**
- Veja os logs detalhados na aba Actions
- Verifique se todas as dependências estão em requirements.txt/package.json

**Deploy falha:**
- Verifique se os secrets estão configurados corretamente
- Teste o deploy manualmente primeiro

### 5. Workflows Disponíveis

#### CI (`.github/workflows/ci.yml`)
- ✅ Lint Python (Ruff)
- ✅ Lint JavaScript (ESLint)
- ✅ Build backend
- ✅ Build frontend
- ✅ Security scan (Trivy)
- 🔄 Roda em: Push, Pull Request

#### CD (`.github/workflows/cd-deploy.yml`)
- 🚀 Deploy backend (Railway/Render)
- 🚀 Deploy frontend (Vercel/Netlify)
- 🔍 Health checks pós-deploy
- 🔄 Roda em: Push na main

#### PR Preview (`.github/workflows/pr-preview.yml`)
- 👀 Deploy de preview para PRs
- 💬 Comenta URL de preview no PR
- 🔄 Roda em: Pull Requests

### 6. Comandos Úteis

```bash
# Ver status dos workflows
gh workflow list

# Ver runs de um workflow
gh run list --workflow=ci.yml

# Ver logs de um run
gh run view <run-id> --log

# Disparar workflow manualmente
gh workflow run cd-deploy.yml
```

### 7. Custos

- **GitHub Actions**: 2000 minutos grátis/mês (plano free)
- **Vercel**: Unlimited deploys (plano hobby free)
- **Railway**: $5 crédito grátis/mês
- **Render**: Free tier disponível
- **Netlify**: 300 minutos build/mês (plano free)

---

## 🎉 Pronto!

Agora seus deploys são automáticos:
- ✅ Push na `main` → Deploy em produção
- ✅ Pull Request → Preview deploy
- ✅ Qualquer commit → CI tests
