# 📚 Templates Aprimorados - Cerebrum v0.2

Baseado em princípios epistêmicos state-of-the-art.

## Meta-Princípios Aplicados

1. **Frontmatter Primeiro, Sempre** ✅
2. **Prompts > Instruções** 🆕
3. **Linking É Obrigatório** ✅
4. **Estrutura Reflete Processamento** 🆕
5. **Progressive Summarization** ✅

---

## Template: Literature Note (Aprimorado)

```markdown
---
# === IDENTITY ===
id: {{id}}
title: {{title}}
type: literature
status: seedling

# === CONTEXT ===
source:
  type: {{source_type}}
  title: {{source_title}}
  authors: {{source_authors}}
  year: {{year}}
  url: {{url}}
created: {{created}}

# === TAXONOMY ===
domain: {{domain}}
subdomain: {{subdomain}}
tags: {{tags}}

# === BASB ===
basb:
  para_category: Resources
  para_path: {{basb_para_path}}
  progressive_summary:
    layer: 0
    last_summarized: null
  intermediate_packet: false

# === LYT ===
lyt:
  mocs: {{lyt_mocs}}
  context: "Source material for concept extraction"

# === ZETTELKASTEN ===
zettelkasten:
  note_type: literature
  connections_count: 0

# === MANAGEMENT ===
reviewed: 0
next_review: {{next_review}}
---

# 📚 {{title}}

> [!info] Bibliographic Information
> **Authors:** {{authors_str}}
> **Type:** {{source_type}}
> **Year:** {{year}}
> **Status:** 🌱 Seedling (captured, not yet processed)

---

## 📋 Layer 0: Raw Capture

> [!question] Initial Questions
> - What is the main thesis or argument?
> - What evidence or examples support it?
> - How does this connect to my existing knowledge?

{{preview}}

---

## 💎 Permanent Notes Extracted

> [!tip] These atomic concepts were distilled from this source
> Each represents a single, reusable idea

{{permanent_notes_links}}

---

## 🔄 Layer 1: Bold Key Passages (Todo)

> [!note] Progressive Summarization - Layer 1
> When you first USE information from this source:
> - Bold the 10-20% most important passages
> - Focus on surprising insights or actionable advice

**Instructions:**
- Read through Raw Content below
- Bold (`**text**`) the most valuable 10-20%
- This becomes your "second read" layer

---

## ✨ Layer 2: Highlight Insights (Todo)

> [!note] Progressive Summarization - Layer 2
> When this becomes CRITICAL to a project:
> - Highlight 10-20% of bolded text
> - Use `==highlighted==` or color callouts
> - These are the absolute essentials

---

## 📝 Layer 3: Executive Summary (Todo)

> [!note] Progressive Summarization - Layer 3
> When you need to EXPLAIN this to others:
> - Write a 3-5 sentence summary
> - Include key takeaways only
> - Link to most important permanent notes

---

## 🔗 Connections

> [!tip] How this relates to other knowledge
> Links will evolve as you process and review

### Related Sources
- [[]] ← Similar topic
- [[]] ← Contrasting view
- [[]] ← Builds upon

### Spawned Concepts
{{permanent_notes_links}}

### Relevant MOCs
{{mocs_links}}

---

## 📝 Raw Content

{{raw_text}}

---

## ❓ Processing Questions

> [!question] To deepen understanding
> - [ ] What assumptions does the author make?
> - [ ] What are potential weaknesses in the argument?
> - [ ] How could I apply this practically?
> - [ ] What questions does this raise?
> - [ ] Who should read this?

---

## 🔄 Review Log

**Next Review:** {{next_review_date}}

> [!info] Spaced Repetition
> - First review: 7 days (check permanent notes quality)
> - Second review: 30 days (Layer 1 - bold key passages)
> - Third review: 90 days (Layer 2 - highlight if critical)
> - Archive after 6 months if not actively used

**Review History:**
- [ ] {{date_plus_7}}: Check permanent notes, add bold (Layer 1)
- [ ] {{date_plus_30}}: Highlight critical passages (Layer 2)
- [ ] {{date_plus_90}}: Create executive summary if needed (Layer 3)

---

**Meta:** This note follows BASB + LYT + Zettelkasten principles
**Template Version:** 0.2.0 (Epistemic-Enhanced)
```

---

## Template: Permanent Note (Aprimorado)

```markdown
---
# === IDENTITY ===
id: {{id}}
title: {{title}}
aliases: []
type: permanent
status: seedling

# === CONTEXT ===
created: {{created}}
source:
  literature_note: "[[{{literature_note_title}}]]"
  original_source: {{source_title}}
  authors: {{source_authors}}

# === TAXONOMY ===
domain: {{domain}}
subdomain: {{subdomain}}
tags: {{tags}}

# === BASB ===
basb:
  para_category: Resources
  para_path: {{basb_para_path}}
  progressive_summary:
    layer: 0
  intermediate_packet: false

# === LYT ===
lyt:
  mocs: {{lyt_mocs}}
  fluid_frameworks: []
  context: null

# === ZETTELKASTEN ===
zettelkasten:
  permanent_note_type: {{concept_type}}
  connections_count: {{connections_count}}
  connections_quality: {{connections_quality}}
  centrality_score: 0.0
  status_progression:
    - seedling: {{created}}
    - budding: null
    - evergreen: null

# === QUALITY ===
confidence: 0.75
completeness: 0.60
importance: medium
evidence_strength: medium

# === MANAGEMENT ===
reviewed: 0
last_reviewed: null
next_review: {{next_review}}
version: 1
---

# {{title}}

> [!abstract] Atomic Definition
> **{{definition}}**
>
> *This is a permanent note - a single, reusable concept*
> **Type:** {{concept_type}} | **Status:** 🌱 Seedling | **Confidence:** 75%

---

## 🎯 Essência do Conceito

> [!question] Core Questions
> - What is this, fundamentally?
> - Why does it matter?
> - When does it apply?

{{explanation}}

---

## 💡 Por Que Importa?

> [!question] Significance
> - Why should I care about this?
> - What problems does it solve?
> - What becomes possible?

{{why_matters}}

---

## 🔬 Aplicações

> [!example] Practical Use Cases
> Where and how to apply this concept

{{applications_list}}

> [!question] My Applications
> - [ ] Where can I use this in my current projects?
> - [ ] What experiments could test this?
> - [ ] Who else should know about this?

---

## 🌐 Conexões

> [!tip] How this connects to the knowledge graph
> These connections were created by semantic analysis

{{connections_by_type}}

> [!question] Additional Connections
> - What prerequisites should someone understand first?
> - What concepts does this enable?
> - What contradicts or limits this?

**Add manually:**
- [[]] ← Prerequisite
- [[]] → Enables
- [[]] ⚔️ Contrasts

---

## 🧪 Evidence & Examples

> [!note] What supports this concept?
> Add evidence as you encounter it

- From source: {{source_examples}}
- Real-world observations:
  -
- Counterexamples:
  -

---

## 📚 Source Trail

> [!info] Where this came from
> Maintains intellectual lineage

**Primary Source:** [[{{literature_note_title}}]]
**Original Author(s):** {{source_authors}}
**Related Sources:**
- [[]] ← Corroborates
- [[]] ← Alternative view

---

## ❓ Open Questions

> [!question] To explore further
> Questions drive deeper understanding

- [ ] How does this connect to {{related_concept}}?
- [ ] What are the edge cases or limitations?
- [ ] Are there practical experiments to validate?
- [ ] How has my understanding evolved?

**My Questions:**
-
-

---

## 🔄 Evolution Log

> [!info] How this note matures over time
> Track progression from seedling → evergreen

**Status Progression:**
- 🌱 Seedling ({{created}}): Initial capture
- 🌿 Budding (target: +30 days): Multiple connections, refined explanation
- 🌳 Evergreen (target: +90 days): Battle-tested, highly connected, cited in outputs

**Growth Criteria:**
- [ ] ≥5 quality connections
- [ ] Used in at least 1 project/output
- [ ] Reviewed and refined 3+ times
- [ ] Cited by other permanent notes

**Review History:**
- {{created}}: Created from literature note
- Next: {{next_review}}

---

## 💭 Personal Insights

> [!tip] Your unique perspective
> Add your thoughts, experiences, connections

**My Take:**


**How I've Used This:**


**Surprising Connections:**


---

**Meta Information:**
- **Confidence:** 75% (initial capture)
- **Completeness:** 60% (needs refinement)
- **Next Review:** {{next_review_date}}
- **Template Version:** 0.2.0 (Epistemic-Enhanced)
```

---

## Novos Templates: Tipos Especializados

### Template: Concept Note (Pure Concept, sem source)

```markdown
---
id: {{id}}
title: {{title}}
type: permanent
subtype: pure-concept
status: seedling
domain: {{domain}}
tags: {{tags}}
created: {{created}}
confidence: 0.50  # Lower for emergent concepts
---

# {{title}}

> [!abstract] Emergent Concept
> **Definition:** {{one_liner}}
>
> This concept emerged from connecting multiple sources/experiences
> **Status:** 🌱 Seedling | **Confidence:** 50%

## 🧩 What Is This?

> [!question] Defining the concept
> - What makes this distinct from related ideas?
> - What are its essential properties?


## 🌊 How Did This Emerge?

> [!info] Genesis of the idea
> Track intellectual synthesis

**Sources that contributed:**
- [[source-1]]
- [[source-2]]
- [[experience-1]]

**The synthesis:**
[Explain how connecting these led to this new concept]

## 🔗 Connections

### Prerequisites
- [[]] ← Built on

### Related
- [[]] ↔ Similar to
- [[]] ⚔️ Contrasts with

### Applications
- [[]] → Enables

## ❓ Open Questions

- [ ] Is this really distinct, or a special case of X?
- [ ] What evidence would validate/invalidate this?
- [ ] Who else has thought about this?

---

**Next Steps:**
- [ ] Research existing literature
- [ ] Test applications
- [ ] Refine definition
```

### Template: Person Note

```markdown
---
id: {{id}}
title: {{name}}
type: person
role: [author|mentor|colleague|contact]
domain: {{domain}}
tags: [people, {{domain}}]
created: {{created}}
---

# 👤 {{name}}

> [!info] At a Glance
> **Role:** {{role}}
> **Domain:** {{domain}}
> **Connection:** {{how_i_know_them}}

## 🎯 Why This Person Matters

**Key Contributions:**
-

**Relevant to my work because:**
-

## 📚 Their Work

**Key Ideas/Concepts:**
- [[concept-1]] ← From {{source}}
- [[concept-2]] ← From {{source}}

**Notable Works:**
- [[literature-note-1]]
- [[literature-note-2]]

## 🔗 Connections

**Related People:**
- [[person-1]] ← Colleague/collaborator
- [[person-2]] ← Similar domain

**Influenced By:**
- [[person-3]]

**Influences:**
- [[person-4]]

## 💭 Personal Notes

**What I learned from them:**


**Questions to explore:**
- [ ]
- [ ]

**Contact Information:**
- Email:
- Website:
- Social:

---

**Review:** Every 6 months
```

### Template: Project Note

```markdown
---
id: {{id}}
title: {{project_name}}
type: project
status: [planning|active|paused|completed|archived]
basb:
  para_category: Projects
priority: [low|medium|high]
start_date: {{date}}
due_date: {{due}}
tags: [projects, {{area}}]
---

# 🎯 {{project_name}}

> [!success] Project Goal
> {{one_sentence_goal}}
>
> **Status:** {{status}} | **Priority:** {{priority}}
> **Timeline:** {{start}} → {{due}}

## 📋 Overview

**What success looks like:**
-

**Why this matters:**
-

**Scope:**
- In scope:
- Out of scope:

## 🗺️ Relevant Knowledge

> [!tip] Concepts and sources informing this project

**Key Concepts:**
- [[concept-1]] → Applied in {{where}}
- [[concept-2]] → Informs {{decision}}

**Sources:**
- [[literature-1]]
- [[literature-2]]

## ✅ Tasks

- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## 🔄 Progress Log

**{{date}}:**
-

## 🧠 Insights & Learnings

> [!note] What I'm discovering
> These may become permanent notes

-

## 📦 Outputs

**Artifacts created:**
-

**Permanent notes spawned:**
- [[new-concept-1]]
- [[new-concept-2]]

---

**Review:** Weekly while active
```

---

## Key Improvements Applied

### 1. **Prompts em vez de Instruções** 🆕
**Antes:** "## Learnings"
**Depois:** "> [!question] What did I learn? Why does it matter?"

### 2. **Callouts para Meta-info** 🆕
Uso de `> [!question]`, `> [!tip]`, `> [!info]` para highlight

### 3. **Progressive Processing Explícito** 🆕
Layers 0-3 com instruções claras de quando aplicar

### 4. **Status Progression Tracking** 🆕
Seedling → Budding → Evergreen com critérios objetivos

### 5. **Review System Integrado** 🆕
Spaced repetition com datas e checkboxes

### 6. **Linking Taxonomy** 🆕
← Prerequisite, ↔ Related, → Enables, ⚔️ Contrasts

### 7. **Confidence & Completeness** ✅
Já tínhamos, agora mais explícito

---

## Próximos Passos

Quer que eu:

1. **Implemente estes templates no código?**
   - Atualizar `destilador.py` com templates aprimorados
   - Adicionar novos tipos (person, project, pure-concept)

2. **Crie sistema de templates modulares?**
   - Template engine com componentes reutilizáveis
   - Users podem customizar facilmente

3. **Adicione review automation?**
   - Spaced repetition automático
   - Status progression baseado em critérios

4. **Implemente MOC auto-creation?**
   - Detectar clusters
   - Gerar MOCs automaticamente

Qual direção você quer tomar?
