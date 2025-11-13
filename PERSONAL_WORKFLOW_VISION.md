# 🧠 Cerebrum Personal: Refinaria de Conhecimento Local

> Sistema multi-agentes pessoal para curadoria intensiva de conhecimento em Obsidian

---

## 🎯 Filosofia

**Você não quer um produto. Você quer uma extensão do seu cérebro.**

- ✅ **Local-first**: Tudo roda na sua máquina
- ✅ **Privacy-first**: Seus dados nunca saem do seu computador
- ✅ **Simple-first**: Ferramentas diretas, sem overhead
- ✅ **Power-first**: Máxima capacidade de curadoria e refinamento
- ✅ **Fast-first**: Workflows rápidos, não interfaces bonitas

---

## 🛠️ Arquitetura Ultra-Simples

```
seu-vault/
├── .cerebrum/                    # Motor do sistema
│   ├── agents/                   # Scripts Python dos agentes
│   ├── config.yaml               # Suas preferências
│   └── embeddings.db             # Cache local
├── 00-Inbox/                     # Input bruto
├── 03-Permanent/                 # Notas refinadas
└── 99-Meta/                      # Dashboards
```

### **Setup Mínimo**

```bash
# 1. Instalar Ollama (LLM local)
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2:latest
ollama pull nomic-embed-text  # Para embeddings

# 2. Instalar dependências Python (mínimas!)
pip install chromadb sentence-transformers python-frontmatter rich click

# 3. Inicializar Cerebrum no seu vault
cd ~/seu-vault
python -m cerebrum init
```

**Pronto. 3 comandos e você está rodando.**

---

## 🤖 Agentes: Versão Minimalista

### **1. Destilador (`cerebrum distill`)**

**O que faz:**
- Lê PDF/texto/markdown do inbox
- Usa Ollama local para atomizar
- Cria notas estruturadas em Permanent
- Adiciona embeddings ao cache

**Uso:**
```bash
# Processar um arquivo
cerebrum distill inbox/paper.pdf

# Processar tudo no inbox
cerebrum distill inbox/

# Com template específico
cerebrum distill inbox/artigo.md --template academic
```

**Output:**
```
✓ Lendo: paper.pdf (12 páginas)
✓ Extraindo conceitos... (encontrados 8)
✓ Gerando notas atômicas...
  → 03-Permanent/neuroplasticidade-ltp.md
  → 03-Permanent/consolidacao-memoria.md
  → ...
✓ 8 notas criadas em 45s
```

---

### **2. Conector (`cerebrum link`)**

**O que faz:**
- Analisa seu vault
- Usa embeddings locais para similaridade
- Sugere links entre notas
- Atualiza automaticamente

**Uso:**
```bash
# Sugerir links para uma nota específica
cerebrum link 03-Permanent/ltp.md

# Analisar vault inteiro
cerebrum link --all --threshold 0.75

# Modo interativo (você aprova cada link)
cerebrum link --interactive
```

**Output:**
```
Analisando: ltp.md
✓ Embeddings carregados (1.2k notas)
✓ Encontradas 12 conexões potenciais

Sugestões:
  1. [[Consolidação de Memória]] (0.89) - supports
  2. [[Plasticidade Sináptica]] (0.82) - extends
  3. [[Neurotransmissores]] (0.78) - prerequisite

Aplicar? [Y/n/i(interactive)]
```

---

### **3. Curador (`cerebrum curate`)**

**O que faz:**
- Health check do vault
- Detecta notas órfãs, duplicadas
- Agenda revisões (spaced repetition)
- Gera relatório Markdown

**Uso:**
```bash
# Health check completo
cerebrum curate

# Só encontrar órfãs
cerebrum curate --orphans

# Agendar revisões
cerebrum curate --schedule-reviews

# Gerar dashboard
cerebrum curate --dashboard > 99-Meta/health.md
```

**Output:**
```
📊 Vault Health Report

Total de notas: 1,243
├─ Evergreen: 342 (27%)
├─ Seedling: 901 (73%)
└─ Órfãs: 18 (1.4%)

⚠️ Ações Necessárias:
  • 18 notas órfãs precisam de links
  • 45 notas > 30 dias sem revisão
  • 3 pares de notas possivelmente duplicadas

Próximas revisões (7 dias):
  • [[Conceito X]] - 5 revisões → evergreen
  • [[Teoria Y]] - 3 revisões
```

---

### **4. Sintetizador (`cerebrum synthesize`)**

**O que faz:**
- Analisa padrões no vault
- Detecta clusters de conceitos
- Sugere MOCs
- Gera insights emergentes

**Uso:**
```bash
# Analisar últimas N notas
cerebrum synthesize --recent 30

# Análise de domínio específico
cerebrum synthesize --tag neuroscience

# Gerar MOC automático
cerebrum synthesize --create-moc "Neuroplasticidade"
```

**Output:**
```
🔮 Análise de Padrões (últimas 30 notas)

Clusters detectados:
  1. Neuroplasticidade (8 notas, densidade: 0.72)
     → Sugestão: criar MOC
  2. Aprendizagem Motora (5 notas, densidade: 0.58)
  3. Sistemas Complexos (12 notas, densidade: 0.81)
     → Conexão emergente com "Neuroplasticidade"!

Insight Emergente:
  Padrão estrutural similar entre:
    - [[Neuroplasticidade]]
    - [[Sistemas Adaptativos]]
    - [[Metodologias Ágeis]]

  Conceito unificador detectado:
    "Feedback loops + Adaptação incremental"

  Criar nota? [[Meta-Padrão de Adaptação Evolutiva]] [Y/n]
```

---

## 💻 Interface: CLI First, GUI Opcional

### **Modo 1: CLI Puro (Recomendado)**

Tudo via terminal, super rápido:

```bash
# Workflow diário
cd ~/vault

# 1. Processar inbox
cerebrum distill inbox/ --auto

# 2. Conectar novas notas
cerebrum link --recent 10 --auto

# 3. Health check semanal
cerebrum curate --dashboard > 99-Meta/health-$(date +%Y-%m-%d).md

# 4. Buscar insights (quando quiser)
cerebrum synthesize --recent 50
```

---

### **Modo 2: VS Code Integration**

Comandos disponíveis na paleta do VS Code:

```json
// .vscode/tasks.json
{
  "tasks": [
    {
      "label": "Cerebrum: Distill Current File",
      "command": "cerebrum distill ${file}"
    },
    {
      "label": "Cerebrum: Link Current Note",
      "command": "cerebrum link ${file} --interactive"
    },
    {
      "label": "Cerebrum: Daily Curate",
      "command": "cerebrum curate"
    }
  ]
}
```

**Atalhos:**
- `Cmd+Shift+P` → "Cerebrum: Distill" → processa nota atual
- `Cmd+Shift+L` → Sugere links para nota aberta
- `Cmd+Shift+H` → Health check

---

### **Modo 3: Interface Web Básica (Opcional)**

Se quiser algo visual às vezes:

```bash
# Iniciar servidor local
cerebrum serve --port 3000

# Abre em http://localhost:3000
```

**Features mínimas:**
- Upload de PDF/texto → processa → mostra preview
- Visualização do grafo de conhecimento
- Dashboard de métricas
- Editor de templates

**Tecnologia:** FastAPI + HTMX (zero JavaScript complexo)

---

## 📐 Templates: Simples e Poderosos

### **Sistema de Templates**

```yaml
# .cerebrum/templates/concept.yaml
name: Conceito
description: Nota atômica de conceito
frontmatter:
  type: concept
  status: seedling
  tags: []

structure: |
  # {title}

  > [!abstract] Definição
  > {definition}

  ## Contexto

  {context}

  ## Conexões

  {connections}

  ## Aplicações

  {applications}

prompts:
  definition: "Defina '{title}' em 1-2 frases claras"
  context: "Explique o contexto e importância de '{title}'"
  applications: "Liste 3 aplicações práticas de '{title}'"
```

**Uso:**
```bash
# Criar nota com template
cerebrum create "Potenciação de Longo Prazo" --template concept

# Ou aplicar template em nota existente
cerebrum template ltp.md --apply concept
```

---

## 🔧 Configuração Pessoal

```yaml
# .cerebrum/config.yaml

# LLM Local
llm:
  provider: ollama
  model: llama3.2:latest
  temperature: 0.3

# Embeddings
embeddings:
  model: nomic-embed-text
  cache: .cerebrum/embeddings.db

# Vault Structure
vault:
  inbox: 00-Inbox
  permanent: 03-Permanent
  literature: 02-Literature
  mocs: 04-MOCs
  meta: 99-Meta

# Seus domínios de conhecimento
taxonomy:
  domains:
    - neuroscience
    - philosophy
    - systems-thinking
  tags:
    - neuro/cellular
    - neuro/cognitive
    - philosophy/epistemology
  stopwords: [a, o, e, de, em, para, com]

# Preferências de linking
linking:
  similarity_threshold: 0.75
  max_suggestions: 5
  auto_apply: false  # Sempre pedir confirmação

# Spaced repetition
reviews:
  seedling_interval: 7d
  budding_interval: 14d
  evergreen_interval: 30d

# Agentes ativos
agents:
  distiller: true
  linker: true
  curator: true
  synthesizer: true
```

---

## 🚀 Implementação Prática

### **Estrutura do Código**

```
cerebrum/
├── cerebrum/
│   ├── __init__.py
│   ├── cli.py                    # Click CLI
│   ├── agents/
│   │   ├── base.py               # Base agent class
│   │   ├── distiller.py          # ~200 linhas
│   │   ├── linker.py             # ~150 linhas
│   │   ├── curator.py            # ~180 linhas
│   │   └── synthesizer.py        # ~220 linhas
│   ├── intelligence/
│   │   ├── llm.py                # Ollama wrapper
│   │   └── embeddings.py         # Embedding service
│   ├── vault/
│   │   ├── manager.py            # File operations
│   │   ├── parser.py             # Frontmatter parsing
│   │   └── graph.py              # Graph analysis
│   └── utils/
│       ├── templates.py
│       └── config.py
├── pyproject.toml
└── README.md
```

### **Dependências Mínimas**

```toml
[tool.poetry.dependencies]
python = "^3.11"

# CLI
click = "^8.1.7"
rich = "^13.7.0"  # Pretty terminal output

# LLM Local
ollama = "^0.1.6"

# Embeddings & Similarity
chromadb = "^0.4.18"
sentence-transformers = "^2.2.2"

# Graph Analysis
networkx = "^3.2"

# Markdown & Files
python-frontmatter = "^1.0.0"
pypdf = "^3.17.0"
watchdog = "^3.0.0"

# Utils
pyyaml = "^6.0.1"
python-dateutil = "^2.8.2"
```

**Total: ~8 dependências principais. Zero overhead.**

---

## 📝 Workflow Pessoal Típico

### **Manhã: Captura**
```bash
# Processa tudo que você jogou no inbox ontem
cerebrum distill inbox/ --auto

# Revisa sugestões de links
cerebrum link --recent 10 --interactive
```

### **Tarde: Refinamento**
```bash
# Trabalha em uma nota específica
code 03-Permanent/minha-nota.md

# Enquanto edita, usa atalho para sugerir conexões
# Cmd+Shift+L → mostra links sugeridos inline
```

### **Noite: Reflexão**
```bash
# Analisa padrões da semana
cerebrum synthesize --recent 30

# Se encontrar insight interessante, cria nova nota
cerebrum create "Novo Insight" --template insight
```

### **Semanal: Curadoria**
```bash
# Health check completo
cerebrum curate --dashboard > 99-Meta/health-$(date +%Y-%m-%d).md

# Abre no Obsidian e revisa métricas
open 99-Meta/health-2025-01-15.md
```

---

## 🎨 Recursos Avançados (Depois)

Quando você quiser expandir:

### **1. Obsidian Plugin Bridge**
```javascript
// Plugin mínimo que chama CLI
class CerebrumPlugin {
  async onload() {
    this.addCommand({
      id: 'distill-current',
      name: 'Distill Current Note',
      callback: () => exec(`cerebrum distill ${this.app.workspace.getActiveFile()}`)
    });
  }
}
```

### **2. Git Hooks**
```bash
# .git/hooks/post-commit
#!/bin/bash
# Auto-link após cada commit
cerebrum link --recent 5 --auto
```

### **3. Alfred/Raycast Integration**
```bash
# Atalho global: Cmd+Shift+C
# → Abre quick input para criar nota
cerebrum quick-create --template fleeting
```

### **4. Watch Mode**
```bash
# Processa automaticamente arquivos novos no inbox
cerebrum watch inbox/ --auto-distill
```

---

## 💡 Por Que Essa Abordagem Funciona

### **1. Zero Fricção**
- Você não precisa "usar uma ferramenta"
- É só parte do seu workflow
- CLI = velocidade máxima

### **2. Controle Total**
- Você vê exatamente o que o agente faz
- Modo interativo para aprovar mudanças
- Configs em YAML legível

### **3. Privacy & Speed**
- Tudo local, zero latência de rede
- Embeddings cached, análise instantânea
- Seus dados nunca saem da máquina

### **4. Extensível**
- Python simples, fácil de hackear
- Adicione seus próprios agentes
- Templates customizáveis

### **5. Cresce Com Você**
- Começa simples (só distiller)
- Adiciona agentes conforme precisa
- Vault de 100 ou 10,000 notas funciona

---

## 🎯 Próximos Passos (Para Você)

### **Semana 1: MVP Funcional**
```bash
# Dia 1-2: Setup básico
- [ ] Instalar Ollama
- [ ] Criar estrutura cerebrum/
- [ ] Implementar CLI básico (Click)

# Dia 3-5: Distiller Agent
- [ ] Parser de PDF/Markdown
- [ ] Integração Ollama
- [ ] Geração de notas atômicas

# Dia 6-7: Testar no seu vault
- [ ] Processar 10 notas do inbox
- [ ] Iterar baseado no resultado
```

### **Semana 2-3: Linker + Curator**
```bash
- [ ] Implementar embeddings (ChromaDB)
- [ ] Linker agent (similaridade semântica)
- [ ] Curator agent (health checks)
- [ ] Dashboard básico
```

### **Semana 4+: Refinamento**
```bash
- [ ] Templates customizados
- [ ] VS Code integration
- [ ] Synthesizer agent
- [ ] Workflows automatizados
```

---

## 📊 Resultado Esperado

**Em 1 mês:**
- ✅ CLI funcional com 4 agentes
- ✅ Processando 10-20 notas/dia
- ✅ Vault com 500+ notas bem conectadas
- ✅ Dashboard de saúde automático
- ✅ Zero dependência de serviços externos

**Em 3 meses:**
- ✅ 2,000+ notas refinadas
- ✅ Sistema de revisão espaçada funcionando
- ✅ Insights emergentes semanais
- ✅ Segundo cérebro de altíssimo nível

---

## 🔥 Começar AGORA

```bash
# 1. Criar estrutura
mkdir -p cerebrum/{agents,intelligence,vault,utils}
touch cerebrum/cli.py

# 2. Setup inicial
cat > cerebrum/cli.py << 'EOF'
import click

@click.group()
def cli():
    """Cerebrum - Personal Knowledge Refinement"""
    pass

@cli.command()
@click.argument('input_path')
def distill(input_path):
    """Distill knowledge from input"""
    click.echo(f"Processing: {input_path}")
    # TODO: implement

if __name__ == '__main__':
    cli()
EOF

# 3. Testar
python cerebrum/cli.py distill test.md
```

**Quer que eu implemente o Distiller agent completo agora?**
