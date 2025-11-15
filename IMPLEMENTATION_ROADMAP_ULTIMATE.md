# 🗺️ Roadmap de Implementação - Cerebrum Ultimate

> **"De MVP funcional a refinaria suprema em 6 meses"**

---

## 🎯 VISÃO GERAL

**Meta:** Implementar progressivamente o sistema multi-agente completo, validando cada fase antes de avançar.

**Filosofia:** Start simple, validate, iterate, expand

---

## 📅 CRONOGRAMA MACRO (6 Meses)

```
Mês 1: MVP Funcional (Destilador + Classificador)
Mês 2: Linking Inteligente (Conector)
Mês 3: Curadoria Automática (Curador)
Mês 4: Orquestração Completa (Athena)
Mês 5: Insights Emergentes (Sintetizador)
Mês 6: Polish + Otimização
```

---

## 🏗️ FASE 1: MVP FUNCIONAL (Semanas 1-4)

### Objetivo
Sistema básico que pega PDF/texto e gera notas atômicas estruturadas.

### Agentes a Implementar
- ✅ **Extrator** (básico - PDF + Markdown)
- ✅ **Classificador** (heurístico simples)
- ✅ **Destilador** (LLM local)

### Features
- [x] CLI funcional (`cerebrum process file.pdf`)
- [x] Extração de PDF
- [x] Classificação de conteúdo (academic_paper vs fleeting)
- [x] Geração de notas atômicas (5-12 por documento)
- [x] Frontmatter básico (id, title, type, domain, tags)
- [x] Salvar em estrutura PARA

### Deliverables

**Semana 1-2: Extrator + Classificador**

```bash
# Dia 1-3: Extrator
- Implementar ExtratorAgent
- Parser PDF (pypdf)
- Parser Markdown (python-frontmatter)
- Metadata extraction
- Testes: 5 PDFs acadêmicos

# Dia 4-7: Classificador
- Implementar ClassificadorAgent
- Heurísticas de classificação
- Framework plan básico (BASB + Zettelkasten)
- Taxonomia por keywords
- Testes: 10 documentos variados
```

**Semana 3-4: Destilador**

```bash
# Dia 8-14: Destilador
- Implementar DestiladorAgent
- LLM prompt para conceitos atômicos
- Template concept-basic
- Geração de frontmatter
- Slugification
- Save to vault
- Testes: Processar 20 papers

# Dia 14: Validação Phase 1
- [ ] Processar 1 paper acadêmico em <3 min
- [ ] Gerar 5-10 notas atômicas
- [ ] Frontmatter completo e válido
- [ ] Salvo na estrutura PARA correta
- [ ] Usar em seu próprio vault por 1 semana
```

### Código Essencial

```python
# cerebrum/agents/phase1_mvp.py

class Phase1Pipeline:
    """MVP: Extrator → Classificador → Destilador"""

    def __init__(self):
        self.extrator = ExtratorAgent()
        self.classificador = ClassificadorAgent()
        self.destilador = DestiladorAgent()

    def process(self, file_path: str) -> Dict:
        # Step 1: Extract
        extracted = self.extrator.process({'file_path': file_path})
        if not extracted['validation']['passed']:
            raise Exception("Extração falhou")

        # Step 2: Classify
        classified = self.classificador.process(extracted['output'])
        if not classified['validation']['passed']:
            raise Exception("Classificação falhou")

        # Step 3: Distill
        distilled = self.destilador.process({
            **extracted['output'],
            **classified['output']
        })
        if not distilled['validation']['passed']:
            raise Exception("Destilação falhou")

        # Save notes
        notes_saved = []
        for note in distilled['output']['notes']:
            filepath = self._save_note(note)
            notes_saved.append(filepath)

        return {
            'notes_created': len(notes_saved),
            'paths': notes_saved
        }
```

### Success Criteria - Phase 1

- ✅ 20 papers processados com sucesso
- ✅ Tempo médio < 3 min/paper
- ✅ 0 erros de frontmatter
- ✅ Notas fazem sentido standalone
- ✅ Você usa o sistema diariamente

---

## 🔗 FASE 2: LINKING INTELIGENTE (Semanas 5-8)

### Objetivo
Notas não ficam órfãs - sistema cria conexões semânticas automáticas.

### Agente a Implementar
- ✅ **Conector** (embeddings + LLM)

### Features
- [ ] Gerar embeddings de cada nota (ChromaDB)
- [ ] Busca por similaridade semântica
- [ ] LLM para validar conexões
- [ ] Tipos de links (supports, extends, etc.)
- [ ] Backlinks automáticos
- [ ] Detecção de clusters → sugestão de MOCs

### Deliverables

**Semana 5-6: Embeddings & Search**

```bash
# Setup
pip install chromadb sentence-transformers

# Implementação
- ChromaDB setup
- Embedding generation (all-MiniLM-L6-v2)
- Similarity search (threshold 0.75)
- Cache de embeddings
- Testes: 100 notas, buscar similares
```

**Semana 7-8: Link Creation & Validation**

```bash
# Implementação
- LLM prompt para validar links
- Tipos de relacionamento
- Bidirectional linking
- Update frontmatter (links_out, links_in)
- Graph analysis básico (NetworkX)
- Cluster detection (Louvain)
- Testes: 50 notas novas, linkar ao vault existente
```

### Código Essencial

```python
# cerebrum/agents/conector.py

class ConectorAgent:
    def __init__(self):
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection("notes")
        self.llm = LLMService()

    def process(self, input_msg: Dict) -> Dict:
        new_notes = input_msg['notes']
        vault_path = input_msg['vault_path']

        # Load existing vault
        existing_notes = self._load_vault_notes(vault_path)

        results = []

        for new_note in new_notes:
            # Generate embedding
            embedding = self._generate_embedding(new_note['content'])

            # Search similar
            similar = self.collection.query(
                query_embeddings=[embedding],
                n_results=15,
                where={"type": "permanent"}
            )

            # LLM validation
            validated_links = []
            for candidate in similar['documents'][0]:
                should_link = self._llm_validate_link(new_note, candidate)

                if should_link['link']:
                    validated_links.append({
                        'target': candidate['slug'],
                        'type': should_link['type'],
                        'confidence': should_link['confidence']
                    })

            # Update note
            new_note['metadata']['links_out'] = validated_links

            # Update backlinks in targets
            for link in validated_links:
                self._add_backlink(link['target'], new_note['slug'])

            results.append(new_note)

        # Detect clusters
        clusters = self._detect_clusters(results + existing_notes)

        return {
            'output': {
                'linked_notes': results,
                'clusters': clusters
            },
            'validation': self._validate_linking(results)
        }
```

### Success Criteria - Phase 2

- ✅ 0% notas órfãs
- ✅ Média 4-6 links/nota
- ✅ Links fazem sentido contextualmente
- ✅ 2-3 clusters detectados → MOCs sugeridos
- ✅ Tempo de linking < 30s/nota

---

## 🧹 FASE 3: CURADORIA AUTOMÁTICA (Semanas 9-12)

### Objetivo
Sistema mantém saúde do vault automaticamente.

### Agente a Implementar
- ✅ **Curador**

### Features
- [ ] Health checks diários/semanais/mensais
- [ ] Detecção de órfãos e duplicatas
- [ ] Spaced repetition scheduling
- [ ] Status evolution (seedling → evergreen)
- [ ] Progressive Summarization tracking
- [ ] Dashboard de métricas

### Deliverables

**Semana 9-10: Health Checks**

```python
# cerebrum/agents/curador.py

class CuradorAgent:
    def daily_check(self):
        """Execução diária (5 min)"""
        # Scan notas criadas hoje
        # Validar frontmatter
        # Verificar orphans imediatos
        # Agendar próximas revisões
        pass

    def weekly_check(self):
        """Execução semanal (20 min)"""
        # Gerar health report
        # Detectar duplicatas
        # Evoluir status de notas
        # Sugerir MOCs para clusters
        pass

    def monthly_check(self):
        """Execução mensal (60 min)"""
        # Dashboard completo
        # Análise de tendências
        # Limpeza de archives
        # Otimização de taxonomia
        pass
```

**Semana 11-12: Automation & Dashboard**

```bash
# Implementação
- Cron-like scheduler (APScheduler)
- Automated reviews reminder
- Dashboard generation (Markdown)
- Dataview queries integration
- Backup automation
- Testes: rodar em vault de 500+ notas
```

### Success Criteria - Phase 3

- ✅ Health check roda automaticamente
- ✅ Dashboard atualiza semanalmente
- ✅ Spaced repetition funciona
- ✅ Orphans < 3% sempre
- ✅ Status evolui automaticamente

---

## 🎼 FASE 4: ORQUESTRAÇÃO COMPLETA (Semanas 13-16)

### Objetivo
Athena orquestra todos os agentes em workflows robustos.

### Componente a Implementar
- ✅ **Athena Orchestrator**
- ✅ **Anatomista** (templates avançados)

### Features
- [ ] Pipeline declarativo (YAML workflows)
- [ ] Validação entre etapas
- [ ] Rollback em caso de falha
- [ ] Logs estruturados
- [ ] Métricas de performance
- [ ] Templates dinâmicos avançados

### Deliverables

**Semana 13-14: Orchestrator Core**

```yaml
# workflows/process_paper.yaml

name: process_academic_paper
description: Processa paper acadêmico completo

steps:
  - agent: Extrator
    input: {file_path: $INPUT}
    validation:
      - text_length > 1000
      - metadata.title exists

  - agent: Classificador
    input: {raw_text: $PREV.raw_text, metadata: $PREV.metadata}
    validation:
      - basb_path defined

  - agent: Destilador
    input: {raw_text: $STEP1.raw_text, framework_plan: $PREV.framework_plan}
    validation:
      - min_notes >= 5

  - agent: Anatomista
    input: {notes: $PREV.notes, templates: $STEP2.templates}

  - agent: Conector
    input: {notes: $PREV.structured_notes}

  - agent: Curador
    input: {new_notes: $PREV.linked_notes}

output: final_report.md
```

```python
class AthenaOrchestrator:
    def load_workflow(self, yaml_path: str):
        """Carrega workflow de arquivo YAML"""
        pass

    def execute_workflow(self, workflow: Dict, input_data: Dict):
        """Executa workflow com validação em cada etapa"""
        pass
```

**Semana 15-16: Anatomista & Templates**

```bash
# Implementação
- Template engine avançado
- Templates por tipo de conteúdo
- Callouts dinâmicos
- Mermaid diagrams auto-generation
- Dataview queries embedding
- Testes: 10 tipos diferentes de notas
```

### Success Criteria - Phase 4

- ✅ Pipeline completo end-to-end funciona
- ✅ Validação detecta e reporta erros
- ✅ Logs permitem debug
- ✅ Templates cobrem 80% dos casos
- ✅ Tempo total < 5 min para paper completo

---

## 🔮 FASE 5: INSIGHTS EMERGENTES (Semanas 17-20)

### Objetivo
Sistema detecta padrões e gera conhecimento novo.

### Agente a Implementar
- ✅ **Sintetizador**

### Features
- [ ] Community detection (graph clustering)
- [ ] Cross-domain pattern matching
- [ ] Analogical reasoning (estruturas similares)
- [ ] Insight generation (notas síntese)
- [ ] Auto-create MOCs para clusters
- [ ] Trend analysis

### Deliverables

**Semana 17-18: Graph Analysis**

```python
# cerebrum/agents/sintetizador.py

class SintetizadorAgent:
    def detect_communities(self, graph: nx.Graph):
        """Louvain algorithm para clustering"""
        communities = community_louvain.best_partition(graph)
        return communities

    def cross_domain_patterns(self, domains: List[str]):
        """Encontra padrões estruturais em domínios diferentes"""
        patterns = []

        for domain_a in domains:
            for domain_b in domains:
                if domain_a != domain_b:
                    similarity = self._structural_similarity(domain_a, domain_b)

                    if similarity > 0.75:
                        pattern = self._extract_pattern(domain_a, domain_b)
                        patterns.append(pattern)

        return patterns
```

**Semana 19-20: Insight Generation**

```bash
# Implementação
- LLM prompts para insights
- Nota synthesis template
- Auto-linking de insights a notas fonte
- Weekly insights report
- Testes: 1000+ notas vault, gerar insights
```

### Success Criteria - Phase 5

- ✅ 1-3 insights emergentes/semana
- ✅ Insights são realmente não-óbvios
- ✅ Patterns cross-domain detectados
- ✅ MOCs automáticos criados
- ✅ Você teve pelo menos 1 "aha moment"

---

## 💎 FASE 6: POLISH & OTIMIZAÇÃO (Semanas 21-24)

### Objetivo
Sistema production-ready, otimizado, documentado.

### Features
- [ ] Performance optimization (cache, batch processing)
- [ ] Error handling robusto
- [ ] Retry logic com exponential backoff
- [ ] Configuração flexível (YAML)
- [ ] Documentação completa
- [ ] Tests automatizados (pytest)
- [ ] CI/CD básico

### Deliverables

**Semana 21: Performance**

```bash
- Implementar cache de embeddings (Redis ou SQLite)
- Batch processing (processar 10+ arquivos de uma vez)
- Lazy loading de grafo
- Otimizar prompts LLM (reduzir tokens)
- Benchmark: processar 100 papers em <30 min
```

**Semana 22: Robustez**

```bash
- Error handling em cada agente
- Retry logic para LLM calls
- Validation schemas (JSON Schema)
- Fallbacks quando LLM falha
- Graceful degradation
```

**Semana 23: Testes**

```bash
# tests/test_agents.py

def test_extrator_pdf():
    agent = ExtratorAgent()
    result = agent.process({'file_path': 'test.pdf'})
    assert result['validation']['passed']
    assert len(result['output']['raw_text']) > 100

def test_destilador_creates_notes():
    agent = DestiladorAgent()
    result = agent.process({...})
    assert len(result['output']['notes']) >= 5

# Coverage goal: >80%
```

**Semana 24: Documentação & Exemplos**

```bash
- README.md completo
- QUICKSTART.md atualizado
- Exemplos de uso
- Video tutorial (opcional)
- Deploy guide
```

### Success Criteria - Phase 6

- ✅ 100 papers processados sem erros
- ✅ Test coverage > 80%
- ✅ Performance benchmarks atingidos
- ✅ Documentação completa
- ✅ 3+ pessoas testaram e aprovaram

---

## 📊 MÉTRICAS DE PROGRESSO

### Por Fase

| Fase | Notas Criadas | Links Criados | Insights | Vault Health |
|------|---------------|---------------|----------|--------------|
| 1 | 100-200 | 0 | 0 | N/A |
| 2 | 300-500 | 800-1500 | 0 | 70% |
| 3 | 500-800 | 1500-3000 | 0 | 85% |
| 4 | 800-1200 | 3000-5000 | 0 | 90% |
| 5 | 1200-2000 | 5000-8000 | 5-10 | 92% |
| 6 | 2000+ | 8000+ | 10+ | 95% |

### KPIs Finais (Mês 6)

**Performance:**
- ⚡ Processar paper em <3 min
- ⚡ Linking em <30s/nota
- ⚡ Health check em <5 min
- ⚡ 100 papers batch em <30 min

**Qualidade:**
- 📊 Orphan rate < 2%
- 📊 Avg links: 4-6/nota
- 📊 Evergreen ratio: 15-20%
- 📊 User satisfaction: 8+/10

**Escalabilidade:**
- 📈 Vault de 2000+ notas
- 📈 8000+ links
- 📈 50+ MOCs
- 📈 Sem degradação de performance

---

## 🛠️ TECH STACK FINAL

### Backend
```python
# Core
python = "^3.11"
fastapi = "^0.104.0"
pydantic = "^2.5.0"

# LLM & Embeddings
ollama = "^0.1.6"
sentence-transformers = "^2.2.2"
chromadb = "^0.4.18"

# Graph & Analysis
networkx = "^3.2"
python-louvain = "^0.16"

# Utilities
python-frontmatter = "^1.0.0"
pypdf = "^3.17.0"
pyyaml = "^6.0.1"
click = "^8.1.7"
rich = "^13.7.0"
apscheduler = "^3.10.4"

# Testing
pytest = "^7.4.3"
pytest-cov = "^4.1.0"
```

### Frontend (Opcional - Fase Extra)
```typescript
// Se quiser interface web
react = "^19.1.1"
vite = "^6.2.0"
reactflow = "^11.10.0"  // Graph viz
```

---

## 🎯 MILESTONES PRINCIPAIS

### Mês 1 ✅
**MVP Funcional**
- Processar 20 papers
- Gerar 200+ notas atômicas
- Usar no dia-a-dia

### Mês 2 ✅
**Linking Inteligente**
- 0 órfãs
- 800+ links criados
- Primeiros MOCs sugeridos

### Mês 3 ✅
**Curadoria Automática**
- Health checks rodando
- Dashboard atualizado
- Spaced repetition ativo

### Mês 4 ✅
**Orquestração Completa**
- Pipeline end-to-end
- Templates avançados
- <5 min processamento

### Mês 5 ✅
**Insights Emergentes**
- Primeiros insights cross-domain
- MOCs automáticos
- Sistema "pensa" junto

### Mês 6 ✅
**Production Ready**
- Vault de 2000+ notas
- Performance otimizado
- Documentado e testado

---

## 🚦 DECISÕES CRÍTICAS

### Decisão 1: Local vs Cloud LLM
**Opção A:** Local (Ollama)
- ✅ Privacidade total
- ✅ Custo zero
- ❌ Qualidade inferior
- ❌ Requer GPU

**Opção B:** Cloud (Gemini)
- ✅ Melhor qualidade
- ✅ Mais rápido
- ❌ Custo por uso
- ❌ Privacidade

**Recomendação:** Hybrid
- Local para tarefas simples (classificação, linking)
- Cloud para tarefas complexas (geração de conteúdo)

### Decisão 2: Vector DB
**Opção A:** ChromaDB (local)
- ✅ Simples setup
- ✅ Local-first
- ❌ Escalabilidade limitada

**Opção B:** Pinecone (cloud)
- ✅ Escalável
- ✅ Managed
- ❌ Custo
- ❌ Dependência externa

**Recomendação:** ChromaDB para MVP, avaliar Pinecone se >10k notas

### Decisão 3: Interface
**Opção A:** CLI puro
- ✅ Rápido
- ✅ Scriptável
- ❌ Learning curve

**Opção B:** Web UI
- ✅ User-friendly
- ✅ Graph viz
- ❌ Complexidade

**Opção C:** Obsidian Plugin
- ✅ Integração nativa
- ✅ Usa UI existente
- ❌ Limitações da API

**Recomendação:** CLI + Web UI opcional (Fase 7)

---

## 📅 PRÓXIMOS 7 DIAS (Começar AGORA)

### Dia 1 (Hoje)
```bash
# Setup
- [ ] Criar branch feature/cerebrum-ultimate
- [ ] Setup ambiente virtual
- [ ] Instalar dependências base
- [ ] Escrever primeiro teste

# Implementar
- [ ] ExtratorAgent skeleton
- [ ] Parser PDF básico
- [ ] Teste com 1 PDF
```

### Dia 2
```bash
- [ ] Completar ExtratorAgent
- [ ] Metadata extraction
- [ ] Structure analysis
- [ ] Testes: 5 PDFs
```

### Dia 3
```bash
- [ ] ClassificadorAgent skeleton
- [ ] Content type detection
- [ ] Framework plan básico
- [ ] Testes: 10 documentos
```

### Dia 4-5
```bash
- [ ] DestiladorAgent skeleton
- [ ] LLM integration (Ollama)
- [ ] Concept identification
- [ ] Note generation
- [ ] Testes: 3 papers
```

### Dia 6-7
```bash
- [ ] Integração Extrator → Classificador → Destilador
- [ ] CLI command: cerebrum process
- [ ] End-to-end test: processar 1 paper completo
- [ ] Validar output no Obsidian
- [ ] Ajustes baseados em feedback
```

---

## 🎓 LIÇÕES APRENDIDAS (Antecipadas)

### Armadilhas a Evitar

1. **Over-engineering inicial**
   - Não implemente todos agentes de uma vez
   - Valide cada fase antes de avançar

2. **Perfeccionismo de prompts**
   - Prompts LLM nunca serão perfeitos
   - Itere baseado em uso real

3. **Subestimar validação**
   - Validação entre agentes é CRÍTICA
   - Invista tempo nisso

4. **Ignorar performance cedo**
   - Cache embeddings desde o início
   - Batch processing > loop individual

5. **Documentação depois**
   - Documente enquanto implementa
   - Futuro você agradece

---

## ✅ CHECKLIST DE SUCESSO

### Fase 1 Completa Quando:
- [ ] 20 papers processados
- [ ] 200+ notas criadas
- [ ] Você usa diariamente
- [ ] Amigo testou e funcionou

### Fase 2 Completa Quando:
- [ ] Linking automático funciona
- [ ] 0 órfãs
- [ ] Conexões fazem sentido
- [ ] MOC sugerido e criado

### Sistema Completo Quando:
- [ ] Vault de 2000+ notas
- [ ] Performance benchmarks OK
- [ ] Testes passam
- [ ] Documentação completa
- [ ] 3+ pessoas usando com sucesso
- [ ] Você não imagina vida sem

---

**Começar agora:** Abra terminal e rode primeiro comando! 🚀
