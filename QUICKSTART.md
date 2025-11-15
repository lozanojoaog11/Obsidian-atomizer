# 🚀 Cerebrum - Começar AGORA

Guia prático para ter seu sistema de refinaria de conhecimento rodando em **15 minutos**.

---

## Passo 1: Instalar Ollama (5 min)

### macOS / Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows
Baixe de: https://ollama.ai/download

### Verificar instalação
```bash
ollama --version
```

### Baixar modelo
```bash
# Modelo recomendado (rápido e bom)
ollama pull llama3.2:latest

# OU modelo maior (melhor qualidade, mais lento)
ollama pull llama3.1:8b
```

**Teste:**
```bash
ollama run llama3.2 "Olá"
# Deve responder em português
```

---

## Passo 2: Instalar Cerebrum (2 min)

```bash
# Clone ou navegue até o diretório
cd /caminho/para/Obsidian-atomizer

# Instalar em modo dev (editável)
pip install -e .

# Com suporte a LLM local
pip install -e ".[local]"
```

**Verificar:**
```bash
cerebrum --version
# Deve mostrar: 0.1.0
```

---

## Passo 3: Inicializar no seu Vault (1 min)

```bash
# Vá para seu vault do Obsidian
cd ~/Documents/ObsidianVault  # ajuste o caminho

# Inicialize Cerebrum
cerebrum init
```

**O que foi criado:**
```
ObsidianVault/
├── .cerebrum/
│   ├── config.yaml         # ← Edite suas preferências aqui
│   ├── embeddings.db
│   └── templates/
├── 00-Inbox/              # ← Cole arquivos aqui
├── 03-Permanent/          # ← Notas refinadas vão aqui
├── 04-MOCs/
└── 99-Meta/
```

---

## Passo 4: Configurar (Opcional, 2 min)

Edite `.cerebrum/config.yaml`:

```yaml
llm:
  provider: ollama
  model: llama3.2:latest    # ou llama3.1:8b
  temperature: 0.3

vault:
  inbox: 00-Inbox
  permanent: 03-Permanent

taxonomy:
  domains:
    - neurociencia          # ← Seus domínios
    - filosofia
    - sistemas
  tags:
    - neuro/celular         # ← Suas tags
    - filosofia/epistemologia
  stopwords: [a, o, e, de, em]  # ← Stopwords em pt-BR
```

---

## Passo 5: Primeiro Uso! (5 min)

### A. Criar arquivo de teste

```bash
# Criar nota simples para testar
cat > 00-Inbox/test.md << 'EOF'
# Neuroplasticidade

A neuroplasticidade é a capacidade do cérebro de se reorganizar formando novas conexões neurais ao longo da vida. Isso permite que os neurônios compensem lesões e doenças e ajustem suas atividades em resposta a novas situações ou mudanças no ambiente.

## Tipos

Existem dois tipos principais:
1. Plasticidade funcional - capacidade de mover funções de áreas danificadas para áreas não danificadas
2. Plasticidade estrutural - capacidade do cérebro de mudar sua estrutura física como resultado de aprendizado

## Importância

A neuroplasticidade é fundamental para:
- Aprendizado e memória
- Recuperação de lesões cerebrais
- Adaptação a novos ambientes
- Desenvolvimento cognitivo
EOF
```

### B. Processar com Cerebrum

```bash
cerebrum distill 00-Inbox/test.md
```

**Você verá algo como:**
```
🧠 Cerebrum Distiller

⠋ Processing test.md...

✓ Created 3 atomic notes:

  • Neuroplasticidade
    → 03-Permanent/neuroplasticidade.md
  • Plasticidade Funcional
    → 03-Permanent/plasticidade-funcional.md
  • Plasticidade Estrutural
    → 03-Permanent/plasticidade-estrutural.md

Total processing time: 12.3s
```

### C. Verificar resultado

```bash
# Listar notas criadas
ls -l 03-Permanent/

# Ver uma nota
cat 03-Permanent/neuroplasticidade.md
```

**Você verá algo como:**
```markdown
---
type: concept
status: seedling
created: '2025-01-15T10:30:00'
source: test.md
tags:
  - note
  - concept
confidence: 0.75
---

# Neuroplasticidade

> [!abstract] Definição
> A neuroplasticidade é a capacidade do cérebro de se reorganizar...

## Contexto

A neuroplasticidade é fundamental para entender como o cérebro...

## Conexões

- [[Plasticidade Funcional]]
- [[Plasticidade Estrutural]]
- Aprendizado e Memória

## Aplicações

...
```

---

## Workflows Práticos

### Workflow Diário

```bash
# Manhã: processar inbox
cd ~/ObsidianVault
cerebrum distill 00-Inbox/ --auto

# Tarde: refinar notas manualmente no Obsidian

# Noite: health check (quando implementado)
# cerebrum curate
```

### Processar PDF

```bash
# Baixe um paper acadêmico
# Coloque em 00-Inbox/paper.pdf

cerebrum distill 00-Inbox/paper.pdf
```

### Processar múltiplos arquivos

```bash
# Processar tudo no inbox
cerebrum distill 00-Inbox/ --auto

# Sem --auto, pede confirmação para cada arquivo
cerebrum distill 00-Inbox/
```

---

## Próximos Passos

### 1. Customizar Templates (Opcional)

Crie `.cerebrum/templates/academic.md`:

```markdown
---
type: literature
domain: {domain}
---

# 📚 {title}

> [!info] Fonte
> **Autores:** {authors}
> **Ano:** {year}

## Resumo

{summary}

## Conceitos-Chave

{concepts}

## Insights

{insights}
```

Usar:
```bash
cerebrum distill paper.pdf --template academic
```

### 2. Integração com VS Code

Adicione ao `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Cerebrum: Distill Current File",
      "type": "shell",
      "command": "cerebrum distill ${file}",
      "problemMatcher": []
    }
  ]
}
```

Atalho: `Cmd+Shift+P` → "Run Task" → "Cerebrum: Distill"

### 3. Alias para Shell

Adicione ao `~/.zshrc` ou `~/.bashrc`:

```bash
alias cd='cerebrum distill'
alias ci='cerebrum distill 00-Inbox/ --auto'
alias ch='cerebrum curate'  # quando implementado
```

Agora você pode:
```bash
cd paper.pdf        # distill paper.pdf
ci                  # distill inbox completo
```

---

## Troubleshooting

### Problema: "Ollama not found"

```bash
# Verificar se Ollama está rodando
ollama list

# Se não, iniciar:
ollama serve &
```

### Problema: "Model not found"

```bash
# Baixar modelo
ollama pull llama3.2
```

### Problema: "No notes created"

**Causa comum:** LLM retornou formato inválido

**Solução:**
1. Verifique se Ollama está rodando
2. Teste o modelo diretamente: `ollama run llama3.2 "teste"`
3. Tente modelo diferente: edite config.yaml

### Problema: Respostas em inglês

Edite `.cerebrum/config.yaml`:

```yaml
llm:
  temperature: 0.5  # Aumentar um pouco
```

E os prompts em `cerebrum/agents/distiller.py` já pedem pt-BR.

---

## Desenvolvimento Futuro

**Próximas semanas:**
- [ ] Linker agent (sugestão de conexões)
- [ ] Curator agent (health checks)
- [ ] Embeddings locais (busca semântica)
- [ ] Synthesizer (insights emergentes)

**Quer contribuir?**

1. Fork o repo
2. Implemente um agente
3. Teste no seu vault
4. Compartilhe!

---

## Suporte

**Problemas?**
- Abra issue no GitHub
- Ou edite o código diretamente (é seu!)

**Quer mostrar seu uso?**
- Compartilhe prints do seu vault
- Conte como está usando

---

## Filosofia

Este é **seu** sistema de conhecimento.

- ✅ Roda localmente
- ✅ Código simples e hackeável
- ✅ Sem vendor lock-in
- ✅ Privacidade total
- ✅ Evolui com você

**Comece simples. Itere. Cresça.**

---

**Agora vá destilar conhecimento! 🧠**
