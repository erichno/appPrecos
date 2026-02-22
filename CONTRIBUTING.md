# Contribuindo para MelhorPreço

Obrigado por considerar contribuir! 🎉

## Como Contribuir

### 1. Fork & Clone

```bash
git clone https://github.com/SEU_USUARIO/appPrecos.git
cd appPrecos
```

### 2. Crie uma Branch

```bash
git checkout -b feature/minha-feature
# ou
git checkout -b fix/meu-bugfix
```

**Convenção de nomes**:
- `feature/` - Novas funcionalidades
- `fix/` - Correções de bugs
- `docs/` - Documentação
- `refactor/` - Refatoração
- `test/` - Testes

### 3. Desenvolva

Siga as diretrizes:

#### Backend (Python)
- Use type hints
- Docstrings em funções públicas
- Siga PEP 8
- Execute `ruff check .` antes de commitar

#### Frontend (React)
- Componentes funcionais com hooks
- Props com PropTypes ou TypeScript
- CSS com Tailwind (evite inline styles)
- Execute `yarn lint` antes de commitar

### 4. Testes

Adicione testes para novas features:

```bash
# Backend
cd backend
pytest tests/ -v

# Frontend
cd frontend
yarn test
```

### 5. Commit

Use commits semânticos:

```bash
git commit -m "feat: adiciona filtro por categoria"
git commit -m "fix: corrige erro na busca"
git commit -m "docs: atualiza README"
```

**Prefixos**:
- `feat:` - Nova feature
- `fix:` - Bug fix
- `docs:` - Documentação
- `style:` - Formatação
- `refactor:` - Refatoração
- `test:` - Testes
- `chore:` - Manutenção

### 6. Push & Pull Request

```bash
git push origin feature/minha-feature
```

Abra um Pull Request em:
https://github.com/erichno/appPrecos/compare

**Checklist do PR**:
- [ ] CI passa (lint + testes)
- [ ] Código revisado
- [ ] Documentação atualizada
- [ ] Testes adicionados
- [ ] Screenshots (se UI)

## Código de Conduta

Seja respeitoso e colaborativo. Não toleramos:
- Linguagem ofensiva
- Assédio
- Discriminação

## Dúvidas?

Abra uma [issue](https://github.com/erichno/appPrecos/issues) ou entre em contato!
