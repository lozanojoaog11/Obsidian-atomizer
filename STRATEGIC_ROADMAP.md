# 🎯 Roadmap Estratégico: Cerebrum Multi-Agent System

## Decisões Arquiteturais Críticas

### 1. **Modelo de Deployment**

#### Opção A: Standalone Desktop App (Recomendado para MVP)
**Prós:**
- ✅ Privacidade total (processamento local)
- ✅ Funciona offline
- ✅ Integração direta com vault Obsidian
- ✅ Sem custo de infraestrutura

**Contras:**
- ❌ Instalação mais complexa
- ❌ Menos escalável
- ❌ Difícil monetização

**Stack:**
- Electron + React (frontend)
- Python backend empacotado (PyInstaller)
- LLMs locais (Ollama) + opção de API

#### Opção B: Web App + Local Sync
**Prós:**
- ✅ Acesso de qualquer lugar
- ✅ Updates automáticos
- ✅ Fácil onboarding
- ✅ Modelo SaaS (monetização)

**Contras:**
- ❌ Requer upload de dados
- ❌ Depende de internet
- ❌ Custos de infraestrutura

**Stack:**
- React + Vite (frontend)
- FastAPI (backend) em cloud
- Sync via Git/Dropbox API

#### Opção C: Hybrid (Melhor a Longo Prazo)
- Web app para interface
- Local agent executor (via Docker)
- API gateway para orquestração

---

### 2. **Modelo de IA**

#### Opção A: Cloud-Only (Gemini/OpenAI)
**Prós:**
- ✅ Melhor qualidade
- ✅ Desenvolvimento mais rápido
- ✅ Sem necessidade de GPU

**Contras:**
- ❌ Custo por request
- ❌ Preocupações de privacidade
- ❌ Depende de internet

**Custo Estimado:**
- 100 notas/mês: ~$5-10
- 1000 notas/mês: ~$50-100

#### Opção B: Local-First (Ollama/LM Studio)
**Prós:**
- ✅ Privacidade total
- ✅ Custo zero após setup
- ✅ Funciona offline

**Contras:**
- ❌ Requer GPU potente
- ❌ Qualidade inferior
- ❌ Setup mais complexo

**Hardware Mínimo:**
- GPU: 8GB VRAM (RTX 3060)
- RAM: 16GB
- Storage: 50GB

#### Opção C: Hybrid (Recomendado)
- Local para tarefas simples (linking, curadoria)
- Cloud para tarefas complexas (síntese, análise)
- Usuário escolhe o balanço

```python
# Config híbrido
class AIConfig:
    local_model = "llama3-8b"  # Para tasks rápidas
    cloud_model = "gemini-2.5-pro"  # Para tasks complexas

    task_routing = {
        "simple_linking": "local",
        "content_generation": "cloud",
        "summarization": "local",
        "synthesis": "cloud",
    }
```

---

### 3. **Modelo de Dados**

#### Estrutura de Vault Esperada

```
vault/
├── .cerebrum/                    # Metadata do sistema
│   ├── config.yaml               # Configurações
│   ├── embeddings.db             # Cache de embeddings
│   ├── graph.json                # Grafo de conhecimento
│   └── templates/                # Templates customizados
├── 00-Inbox/                     # Notas não processadas
├── 01-Fleeting/                  # Ideias rápidas
├── 02-Literature/                # Notas de fontes
├── 03-Permanent/                 # Notas evergreen
├── 04-MOCs/                      # Maps of Content
├── 05-Projects/                  # Notas de projetos
└── 99-Meta/                      # Dashboards e relatórios
    ├── daily-reports/
    ├── weekly-insights/
    └── knowledge-health.md
```

#### Schema de Frontmatter Padrão

```yaml
---
# Core Metadata
id: uuid-v4
type: concept | literature | project | moc | fleeting
status: seedling | budding | evergreen | crystallized
created: ISO8601
modified: ISO8601

# Content Classification
domain: [neuroscience, philosophy]
tags: [neuro/plasticity, research]
complexity: low | medium | high

# Knowledge Management
confidence: 0.0-1.0
evidence_strength: low | medium | high
source: "Title or URL"
authors: ["Name"]

# Review System
review_count: 0
last_reviewed: ISO8601
next_review: ISO8601
review_interval: 7d | 14d | 30d

# Relationships (managed by agents)
prerequisite: [["Note Slug"]]
supports: [["Note Slug"]]
extends: [["Note Slug"]]
contradicts: [["Note Slug"]]

# Quality Metrics (computed)
link_count: 0
centrality_score: 0.0
cluster_id: "cluster-name"
---
```

---

## Roadmap de Desenvolvimento

### **Fase 0: Validação (2 semanas)**

**Objetivo:** Validar conceito com usuários reais

**Tarefas:**
- [ ] Criar landing page explicativa
- [ ] Fazer 20 entrevistas com usuários de Obsidian
- [ ] Validar dores e necessidades
- [ ] Priorizar agentes baseado em feedback

**Perguntas-Chave:**
1. Qual a maior dor na gestão de conhecimento hoje?
2. Quanto tempo gasta organizando notas/semana?
3. Pagaria por uma solução? Quanto?
4. Preferência: app local vs. web?
5. Preocupação com privacidade (1-10)?

---

### **Fase 1: MVP - Single Agent (4 semanas)**

**Objetivo:** Provar conceito técnico com 1 agente funcional

**Escopo:**
- ✅ Apenas Destilador Agent
- ✅ Input: texto ou PDF
- ✅ Output: notas atômicas em Markdown
- ✅ UI básica (React)
- ✅ Backend (FastAPI + Gemini)

**Arquitetura Mínima:**

```
cerebrum-mvp/
├── backend/
│   ├── main.py                  # FastAPI app
│   ├── agents/
│   │   └── distiller.py         # Único agente
│   ├── services/
│   │   ├── llm.py               # Gemini integration
│   │   └── markdown.py          # Markdown utils
│   └── models/
│       └── note.py
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── InputForm.tsx
│   │   │   └── NotePreview.tsx
│   │   └── services/
│   │       └── api.ts
└── docker-compose.yml           # Para rodar local
```

**Critérios de Sucesso:**
- [ ] Processar 1 PDF em < 2min
- [ ] Gerar 5-10 notas atômicas
- [ ] Frontmatter válido
- [ ] 10 usuários beta testarem

---

### **Fase 2: Multi-Agent Core (6 semanas)**

**Objetivo:** Implementar orquestração multi-agente

**Novos Agentes:**
- ✅ Conector (linking semântico)
- ✅ Templário (templates dinâmicos)
- ✅ Curador (health checks básicos)

**Novas Features:**
- ✅ LangGraph para orquestração
- ✅ Vector DB (ChromaDB)
- ✅ Graph analysis (NetworkX)
- ✅ WebSocket para updates em tempo real

**Critérios de Sucesso:**
- [ ] Processar vault de 100 notas
- [ ] Sugerir 20+ novos links
- [ ] Detectar 2+ MOC oportunidades
- [ ] 50 usuários ativos

---

### **Fase 3: Intelligence Layer (8 semanas)**

**Objetivo:** Adicionar capacidades avançadas

**Novos Agentes:**
- ✅ Arquiteto (análise estrutural)
- ✅ Sintetizador (insights emergentes)
- ✅ Professor (learning paths)

**Novas Features:**
- ✅ Graph visualization (React Flow)
- ✅ Dashboard analytics
- ✅ Spaced repetition
- ✅ Cron jobs (manutenção automática)

**Critérios de Sucesso:**
- [ ] Processar vault de 1000+ notas
- [ ] Gerar 5 insights emergentes/semana
- [ ] Dashboard com métricas úteis
- [ ] 200 usuários pagantes

---

### **Fase 4: Ecosystem & Scale (12 semanas)**

**Objetivo:** Criar ecossistema completo

**Features:**
- ✅ Plugin nativo do Obsidian
- ✅ Integração com Readwise, Zotero
- ✅ Marketplace de templates
- ✅ API pública para extensões
- ✅ Modo colaborativo (teams)

**Critérios de Sucesso:**
- [ ] 1000+ usuários ativos
- [ ] 50+ templates na marketplace
- [ ] 10+ integrações
- [ ] MRR de $10k+

---

## Modelo de Monetização

### **Freemium Tiering**

#### 🆓 Free Tier
- Destilador agent (básico)
- Até 50 notas processadas/mês
- Templates padrão
- Sem suporte

#### ⭐ Pro - $12/mês
- Todos os agentes
- 500 notas/mês
- Templates avançados
- Graph analytics
- Priority support
- Sync em cloud

#### 🚀 Team - $49/mês (até 5 membros)
- Tudo do Pro
- Notas ilimitadas
- Shared vaults
- Custom templates
- API access
- White-label option

#### 🏢 Enterprise - Custom
- On-premise deployment
- SSO/SAML
- Dedicated support
- Custom integrations
- SLA

---

## Stack Tecnológico Final

### **Backend**

```python
# Backend Core
fastapi==0.104.0
uvicorn[standard]==0.24.0
pydantic==2.5.0

# Agent Orchestration
langgraph==0.0.40
langchain==0.1.0
langchain-google-genai==0.0.6

# Data & Intelligence
chromadb==0.4.18
sentence-transformers==2.2.2
networkx==3.2
python-louvain==0.16
spacy==3.7.2

# Utilities
pypdf2==3.0.1
python-frontmatter==1.0.0
watchdog==3.0.0
apscheduler==3.10.4

# Database
sqlalchemy==2.0.23
alembic==1.13.0
redis==5.0.1

# Deployment
docker==6.1.3
kubernetes==28.1.0
```

### **Frontend**

```json
{
  "dependencies": {
    "react": "^19.1.1",
    "react-dom": "^19.1.1",
    "@tanstack/react-query": "^5.14.0",
    "zustand": "^4.4.7",

    "reactflow": "^11.10.0",
    "@visx/visx": "^3.8.0",
    "@monaco-editor/react": "^4.6.0",

    "@google/genai": "^1.15.0",
    "react-markdown": "^9.0.1",

    "tailwindcss": "^3.4.0",
    "framer-motion": "^10.16.16"
  }
}
```

### **Infrastructure**

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./vault:/app/vault
    depends_on:
      - chromadb
      - redis

  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8100:8000"
    volumes:
      - chroma_data:/chroma/chroma

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  chroma_data:
```

---

## Riscos e Mitigações

### **Risco 1: Custo de API**
**Problema:** Gemini API pode ficar caro com scale
**Mitigação:**
- Cache agressivo de embeddings
- Usar Gemini Flash para tarefas simples
- Opção de LLMs locais
- Rate limiting por tier

### **Risco 2: Qualidade das Notas**
**Problema:** LLM pode gerar notas ruins
**Mitigação:**
- Validação com schemas Pydantic
- Feedback loop do usuário
- A/B testing de prompts
- Human-in-the-loop para casos críticos

### **Risco 3: Escalabilidade (Vaults grandes)**
**Problema:** Processar 10,000+ notas pode ser lento
**Mitigação:**
- Processamento incremental
- Indexação eficiente
- Lazy loading de grafos
- Background jobs

### **Risco 4: Privacidade**
**Problema:** Usuários podem não querer enviar dados para cloud
**Mitigação:**
- Oferecer modo 100% local
- Encriptação end-to-end
- Compliance com GDPR/LGPD
- Transparência sobre uso de dados

### **Risco 5: Competição**
**Problema:** Notion AI, Mem.ai, Reflect já existem
**Mitigação:**
- Foco em Obsidian (comunidade fiel)
- Open-source core (community-driven)
- Especialização em Zettelkasten
- Qualidade superior de linking

---

## Métricas de Sucesso

### **Product Metrics**

| Métrica | Mês 1 | Mês 3 | Mês 6 | Mês 12 |
|---------|-------|-------|-------|--------|
| Usuários Ativos | 50 | 200 | 500 | 2000 |
| Notas Processadas | 5k | 50k | 200k | 1M |
| Retention (D7) | 30% | 40% | 50% | 60% |
| NPS | 40 | 50 | 60 | 70 |

### **Business Metrics**

| Métrica | Mês 1 | Mês 3 | Mês 6 | Mês 12 |
|---------|-------|-------|-------|--------|
| MRR | $0 | $500 | $2k | $10k |
| Free → Paid | 5% | 10% | 15% | 20% |
| Churn | 15% | 10% | 8% | 5% |
| LTV/CAC | 1x | 2x | 3x | 5x |

### **Technical Metrics**

| Métrica | Target |
|---------|--------|
| Processing Time (100 notas) | < 5min |
| API Response Time | < 2s |
| Uptime | > 99.5% |
| Error Rate | < 1% |

---

## Primeiros Passos (Esta Semana)

### **Dia 1-2: Setup Inicial**
- [ ] Criar repo no GitHub
- [ ] Setup monorepo (backend + frontend)
- [ ] Configurar Docker
- [ ] Criar projeto no Google AI Studio

### **Dia 3-4: Backend MVP**
- [ ] Implementar rota `/ingest/text`
- [ ] Criar Destilador agent básico
- [ ] Testar com 1 exemplo

### **Dia 5-7: Frontend MVP**
- [ ] Criar UI de upload
- [ ] Mostrar progresso
- [ ] Preview de notas geradas
- [ ] Download em ZIP

---

## Recursos Necessários

### **Time (Ideal)**
- 1 Full-stack developer (você)
- 1 ML engineer (part-time, para otimizar prompts)
- 1 Designer (part-time, para UX)

### **Budget Inicial (Mês 1-3)**
- Gemini API: $100-300/mês
- Cloud hosting (AWS/GCP): $50-100/mês
- Design (Figma, assets): $200
- **Total: ~$500-800/mês**

### **Ferramentas**
- ✅ Google AI Studio (Gemini API)
- ✅ Cursor/VS Code (desenvolvimento)
- ✅ Figma (design)
- ✅ GitHub (code + issues)
- ✅ Vercel/Railway (hosting)

---

## Próximas Decisões Necessárias

1. **Deployment Model:**
   - [ ] Desktop app vs. Web app vs. Hybrid?

2. **AI Strategy:**
   - [ ] Cloud-only vs. Local-first vs. Hybrid?

3. **Pricing:**
   - [ ] Freemium vs. Paid-only vs. Open-core?

4. **Target Market:**
   - [ ] Pesquisadores acadêmicos?
   - [ ] Profissionais de conhecimento (consultores, escritores)?
   - [ ] Estudantes?
   - [ ] Todos acima?

5. **Go-to-Market:**
   - [ ] Comunidade Obsidian (Reddit, Discord)?
   - [ ] Product Hunt launch?
   - [ ] Content marketing (YouTube, blog)?

---

## Questões para Discutir

1. **Visão de Longo Prazo:**
   - Esse é um produto vs. uma empresa?
   - Open-source vs. Closed-source?
   - Solo founder vs. buscar co-founders?

2. **Foco Inicial:**
   - Qual agente é mais valioso para MVP?
   - Qual caso de uso atacar primeiro?

3. **Tecnologia:**
   - Vale a pena usar LangGraph ou criar orquestração custom?
   - ChromaDB vs. Pinecone vs. Weaviate?

4. **UX:**
   - Quanto de automação vs. controle manual?
   - Dashboard vs. CLI vs. Plugin Obsidian?

---

**Pronto para começar? 🚀**

Recomendo:
1. Validar visão com 5-10 usuários de Obsidian
2. Build MVP da Fase 1 (4 semanas)
3. Testar com 20 beta testers
4. Iterar baseado em feedback
5. Decidir sobre expansão
