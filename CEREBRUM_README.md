# 🧠 Cerebrum: Sistema Multi-Agentes de Refinaria de Conhecimento

> Transformando o Obsidian-atomizer em uma refinaria cognitiva completa

---

## 📋 Visão Geral

**Cerebrum** é a evolução do Obsidian-atomizer para um **sistema multi-agentes inteligente** que não apenas atomiza conhecimento, mas o **cultiva, conecta, sintetiza e evolui** de forma contínua e escalável.

### 🎯 Problema que Resolve

Usuários de Obsidian enfrentam desafios ao escalar seus "second brains":
- ⚠️ Notas órfãs sem conexões
- ⚠️ Conhecimento fragmentado e difícil de sintetizar
- ⚠️ Manutenção manual consome muito tempo
- ⚠️ Difícil encontrar insights emergentes
- ⚠️ Sem sistema para evoluir notas de "seedling" para "evergreen"

### ✨ Solução Proposta

Um **ecossistema de 7 agentes especializados** que trabalham em orquestração:

1. **🏛️ Arquiteto** - Planeja estrutura do vault
2. **⚗️ Destilador** - Atomiza conhecimento em notas cristalinas
3. **🔗 Conector** - Cria conexões semânticas inteligentes
4. **🧹 Curador** - Mantém saúde do vault continuamente
5. **🔮 Sintetizador** - Gera insights emergentes cross-domain
6. **👨‍🏫 Professor** - Cria learning paths e flashcards
7. **📐 Templário** - Gerencia templates dinâmicos

---

## 📚 Documentação

### **[1. VISION_MULTI_AGENT.md](./VISION_MULTI_AGENT.md)**
**Leia primeiro!** Documento completo da visão do sistema.

**Conteúdo:**
- Descrição detalhada de cada agente
- Recursos avançados de Markdown/Obsidian a explorar
- Orquestração entre agentes
- Diferenciais competitivos
- Casos de uso práticos

**Tempo de leitura:** ~20 min

---

### **[2. ARCHITECTURE_PROPOSAL.md](./ARCHITECTURE_PROPOSAL.md)**
Proposta técnica detalhada de implementação.

**Conteúdo:**
- Stack tecnológico (Python, React, LangGraph)
- Estrutura de pastas (monorepo)
- Fluxos de dados detalhados
- Sistema de templates dinâmicos
- Sistema de agendamento (cron jobs)
- API endpoints
- WebSocket para updates em tempo real
- Performance & escalabilidade

**Tempo de leitura:** ~30 min

---

### **[3. EXAMPLE_AGENT_FLOW.md](./EXAMPLE_AGENT_FLOW.md)**
Exemplo prático passo-a-passo de processamento.

**Conteúdo:**
- Cenário: Processar paper acadêmico sobre neuroplasticidade
- 8 passos detalhados com código
- Resultado final no vault
- Métricas de sucesso

**Tempo de leitura:** ~25 min

**💡 Dica:** Leia este para entender concretamente como o sistema funciona!

---

### **[4. STRATEGIC_ROADMAP.md](./STRATEGIC_ROADMAP.md)**
Roadmap de desenvolvimento e estratégia de negócio.

**Conteúdo:**
- Decisões arquiteturais críticas
- Roadmap em 4 fases (MVP → Scale)
- Modelo de monetização (Freemium)
- Riscos e mitigações
- Métricas de sucesso
- Primeiros passos práticos

**Tempo de leitura:** ~25 min

---

## 🚀 Quick Start (Como Começar)

### **Opção 1: Explorar a Visão**
```bash
# Leia na ordem:
1. VISION_MULTI_AGENT.md       # Entenda o conceito
2. EXAMPLE_AGENT_FLOW.md       # Veja exemplo prático
3. STRATEGIC_ROADMAP.md        # Veja como implementar
```

### **Opção 2: Começar a Implementar (MVP)**

**Semana 1-2: Validação**
- [ ] Entrevistar 10-20 usuários de Obsidian
- [ ] Validar dores e priorizar agentes
- [ ] Decidir: Desktop vs. Web vs. Hybrid

**Semana 3-6: MVP (Single Agent)**
```bash
# Setup
git checkout -b feature/cerebrum-mvp
mkdir -p backend/{agents,services,models} frontend/src/{components,services}

# Backend
cd backend
poetry init
poetry add fastapi uvicorn langchain-google-genai pydantic

# Implementar apenas Destilador Agent
# Ver: ARCHITECTURE_PROPOSAL.md seção "Fase 1"
```

**Semana 7-12: Multi-Agent Core**
```bash
# Adicionar LangGraph + ChromaDB
poetry add langgraph chromadb sentence-transformers

# Implementar Conector + Templário + Curador
# Ver: ARCHITECTURE_PROPOSAL.md seção "Fase 2"
```

---

## 💡 Conceitos-Chave

### **Multi-Agent Orchestration**
Cada agente é especializado e trabalha em pipeline:
```
Input → Arquiteto → Destilador → Templário → Conector → Curador → Output
```

### **Knowledge Graph**
Vault é representado como grafo:
- **Nós** = Notas
- **Arestas** = Links semânticos (typed: supports, extends, contradicts)
- **Análise** = Centralidade, comunidades, gaps

### **Progressive Elaboration**
Notas evoluem em estágios:
```
🌱 Seedling → 🌿 Budding → 🌳 Evergreen → 💎 Crystallized
```

### **Templates Dinâmicos**
Templates se adaptam ao contexto:
```python
template = select_template(
    note_type="concept",
    domain="neuroscience",
    context={
        "related_notes": ["LTP", "Memory"],
        "complexity": "high"
    }
)
```

---

## 🎨 Diferenciais vs. Competidores

### vs. **Obsidian Puro**
- ✅ IA especializada em Zettelkasten
- ✅ Manutenção proativa automática
- ✅ Insights emergentes cross-domain

### vs. **Notion AI**
- ✅ Foco em pensamento conectivo (não apenas busca)
- ✅ Propriedade total dos dados (Markdown local)
- ✅ Especialização profunda (templates, taxonomias)

### vs. **Mem.ai / Reflect**
- ✅ Multi-agentes especializados
- ✅ Gestão escalável (1000+ notas)
- ✅ Open-source e extensível

---

## 📊 Modelo de Negócio

### **Freemium Tiers**

| Tier | Preço | Features |
|------|-------|----------|
| 🆓 Free | $0 | Destilador básico, 50 notas/mês |
| ⭐ Pro | $12/mês | Todos agentes, 500 notas/mês, analytics |
| 🚀 Team | $49/mês | Ilimitado, shared vaults, API |
| 🏢 Enterprise | Custom | On-premise, SSO, SLA |

**Estimativa de Receita (Ano 1):**
- 2000 usuários ativos
- 20% conversão free → paid
- MRR: $10k/mês
- ARR: $120k/ano

---

## 🛠️ Stack Tecnológico

### **Backend**
```python
FastAPI + LangGraph + Gemini 2.5 Pro
ChromaDB + NetworkX + Spacy
```

### **Frontend**
```typescript
React 19 + Vite + Zustand
React Flow (graphs) + Monaco Editor
```

### **Infrastructure**
```yaml
Docker + Kubernetes
PostgreSQL + Redis
Vercel (frontend) + Railway (backend)
```

---

## 🎯 Roadmap (12 meses)

### **Fase 1: MVP** (Mês 1-2)
- [x] Destilador agent funcional
- [ ] UI básica
- [ ] 10 beta testers

### **Fase 2: Multi-Agent** (Mês 3-4)
- [ ] Conector + Templário + Curador
- [ ] LangGraph orchestration
- [ ] 50 usuários ativos

### **Fase 3: Intelligence** (Mês 5-8)
- [ ] Arquiteto + Sintetizador + Professor
- [ ] Graph visualization
- [ ] 200 usuários pagantes

### **Fase 4: Ecosystem** (Mês 9-12)
- [ ] Plugin Obsidian nativo
- [ ] Marketplace de templates
- [ ] 1000+ usuários, $10k MRR

---

## 🤝 Contribuindo

### **Estamos em fase de ideação!**

Quer ajudar a construir o Cerebrum?

1. **Feedback:** Leia a visão e compartilhe pensamentos
2. **Validação:** Teste hipóteses com usuários
3. **Design:** Ajude a pensar UX/UI
4. **Code:** Contribua com implementação (em breve)

---

## 🔗 Links Úteis

### **Inspirações**
- [Zettelkasten Method](https://zettelkasten.de/)
- [Andy Matuschak's Notes](https://notes.andymatuschak.org/)
- [LangGraph Docs](https://python.langchain.com/docs/langgraph)
- [Obsidian Plugins](https://obsidian.md/plugins)

### **Competidores para Estudar**
- [Mem.ai](https://mem.ai)
- [Reflect](https://reflect.app)
- [Notion AI](https://notion.so/ai)
- [Readwise Reader](https://readwise.io/read)

---

## 📞 Contato

**Criador:** [Seu nome]
**Email:** [seu email]
**GitHub:** [seu github]
**Discord:** [Cerebrum Community] (em breve)

---

## 📄 Licença

**Ainda a definir:**
- Open-source (MIT/Apache)?
- Open-core (core open, premium closed)?
- Closed-source?

---

## 🙏 Agradecimentos

- Comunidade Obsidian
- LangChain/LangGraph team
- Google Gemini team
- Todos os pioneers do Zettelkasten

---

**Status:** 💡 Ideação / Planejamento

**Próximos Passos:**
1. Validar visão com usuários (20 entrevistas)
2. Definir decisões arquiteturais críticas
3. Build MVP (Fase 1)

**Última Atualização:** 2025-01-15

---

**🧠 "Knowledge is a network, not a library. Let's build yours together."**
