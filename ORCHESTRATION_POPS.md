# 🎼 Cerebrum Orchestration - POPs Técnicos Detalhados

> **"De caos a conhecimento: workflows programáticos com validação em cada etapa"**

---

## 🏗️ ARQUITETURA DE ORQUESTRAÇÃO

### Princípios de Design

1. **Pipeline Clear**: Output de agente N = Input de agente N+1
2. **Validação Entre Etapas**: Checklists programáticos impedem propagação de erros
3. **Idempotência**: Rodar 2x = mesmo resultado
4. **Observabilidade**: Logs e métricas em cada etapa
5. **Fault Tolerance**: Falha em agente não quebra pipeline inteiro

---

## 📐 SCHEMA DE DADOS (Entre Agentes)

### Message Format (JSON)

```json
{
  "workflow_id": "uuid-v4",
  "step": 3,
  "agent": "Destilador",
  "timestamp": "2025-01-15T14:30:22Z",
  "status": "completed",  // pending, running, completed, failed
  "input": {
    // Input específico do agente
  },
  "output": {
    // Output específico do agente
  },
  "validation": {
    "passed": true,
    "checks": {
      "check_name": {
        "passed": true,
        "message": "...",
        "value": "..."
      }
    }
  },
  "metadata": {
    "duration_ms": 1234,
    "tokens_used": 5600,
    "cost_usd": 0.023
  }
}
```

---

## 🤖 POPs DETALHADOS POR AGENTE

### Agente 1: EXTRATOR

**Input:**
```json
{
  "file_path": "/path/to/file.pdf",
  "file_type": "pdf",  // auto-detected or specified
  "options": {
    "ocr": true,
    "extract_images": false,
    "language": "pt-BR"
  }
}
```

**Process:**
```python
class ExtratorAgent:
    def process(self, input_msg: Dict) -> Dict:
        file_path = Path(input_msg['file_path'])
        file_type = self._detect_type(file_path)

        # 1. Extração
        if file_type == 'pdf':
            raw_text, metadata = self._extract_pdf(file_path)
        elif file_type == 'markdown':
            raw_text, metadata = self._extract_markdown(file_path)
        elif file_type == 'epub':
            raw_text, metadata = self._extract_epub(file_path)

        # 2. Estrutura
        structure = self._analyze_structure(raw_text)

        # 3. Metadata enrichment
        metadata = self._enrich_metadata(metadata, raw_text)

        # 4. Normalização
        normalized_text = self._normalize(raw_text)

        output = {
            "raw_text": normalized_text,
            "metadata": metadata,
            "structure": structure,
            "stats": {
                "word_count": len(normalized_text.split()),
                "char_count": len(normalized_text),
                "sections": len(structure['sections'])
            }
        }

        # 5. Validação
        validation = self._validate_extraction(output)

        return {
            "output": output,
            "validation": validation
        }

    def _validate_extraction(self, output: Dict) -> Dict:
        checks = {}

        # Check 1: Texto não vazio
        checks['text_not_empty'] = {
            'passed': len(output['raw_text']) > 100,
            'message': 'Texto deve ter >100 caracteres',
            'value': len(output['raw_text'])
        }

        # Check 2: Metadata básico presente
        required_fields = ['title', 'source_type']
        checks['metadata_complete'] = {
            'passed': all(f in output['metadata'] for f in required_fields),
            'message': f'Metadata deve conter: {required_fields}',
            'value': list(output['metadata'].keys())
        }

        # Check 3: Encoding OK
        try:
            output['raw_text'].encode('utf-8')
            checks['encoding_valid'] = {
                'passed': True,
                'message': 'UTF-8 encoding válido'
            }
        except UnicodeEncodeError:
            checks['encoding_valid'] = {
                'passed': False,
                'message': 'Erro de encoding'
            }

        all_passed = all(c['passed'] for c in checks.values())

        return {
            'passed': all_passed,
            'checks': checks
        }
```

**Output:**
```json
{
  "raw_text": "...",
  "metadata": {
    "title": "Neuroplasticity and Learning",
    "authors": ["Silva, M.", "Costa, P."],
    "year": 2024,
    "source_type": "academic_paper",
    "doi": "10.1038/nn.2024.123",
    "pages": 24,
    "language": "en"
  },
  "structure": {
    "sections": [
      {"title": "Introduction", "start": 0, "end": 1200},
      {"title": "Methods", "start": 1200, "end": 3400}
    ],
    "headings": [...],
    "citations": [...]
  },
  "stats": {
    "word_count": 8420,
    "char_count": 52341,
    "sections": 5
  }
}
```

**Validation Checklist:**
```yaml
extrator_validation:
  - name: text_not_empty
    check: len(raw_text) > 100
    critical: true

  - name: metadata_complete
    check: all(['title', 'source_type'] in metadata)
    critical: true

  - name: encoding_valid
    check: raw_text.encode('utf-8') succeeds
    critical: true

  - name: structure_identified
    check: len(structure.sections) > 0
    critical: false

  - name: word_count_reasonable
    check: 500 < word_count < 100000
    critical: false
```

---

### Agente 2: CLASSIFICADOR

**Input:**
```json
{
  "raw_text": "...",
  "metadata": {...},
  "structure": {...}
}
```

**Process:**
```python
class ClassificadorAgent:
    def process(self, input_msg: Dict) -> Dict:
        metadata = input_msg['metadata']
        raw_text = input_msg['raw_text']
        structure = input_msg['structure']

        # 1. Detectar tipo de conteúdo
        content_type = self._classify_content_type(metadata, structure)

        # 2. Decidir frameworks
        framework_plan = self._decide_frameworks(content_type, metadata)

        # 3. Selecionar templates
        templates = self._select_templates(content_type, framework_plan)

        # 4. Definir taxonomia
        taxonomy = self._infer_taxonomy(raw_text, metadata)

        # 5. Definir destino PARA
        para_path = self._determine_para_path(content_type, taxonomy)

        output = {
            "content_type": content_type,
            "framework_plan": framework_plan,
            "templates": templates,
            "taxonomy": taxonomy,
            "para_path": para_path
        }

        validation = self._validate_classification(output)

        return {
            "output": output,
            "validation": validation
        }

    def _classify_content_type(self, metadata: Dict, structure: Dict) -> str:
        """Classifica tipo de conteúdo"""

        # Heurísticas
        if metadata.get('source_type') == 'academic_paper':
            if 'methods' in [s['title'].lower() for s in structure['sections']]:
                return 'academic_paper'

        if metadata.get('source_type') == 'book':
            return 'book_chapter'

        if len(raw_text.split()) < 500:
            return 'fleeting_idea'

        # LLM classification (fallback)
        return self._llm_classify(metadata, structure)

    def _decide_frameworks(self, content_type: str, metadata: Dict) -> Dict:
        """Decide qual combinação de frameworks aplicar"""

        framework_map = {
            'academic_paper': {
                'basb': {
                    'para_category': 'Resources',
                    'progressive_summarization': True,
                    'intermediate_packets': True
                },
                'lyt': {
                    'create_moc': True,
                    'moc_type': 'discipline',
                    'update_home': False
                },
                'zettelkasten': {
                    'note_types': ['literature', 'permanent'],
                    'min_permanent_notes': 5,
                    'linking_strategy': 'aggressive'
                }
            },
            'book_chapter': {
                'basb': {
                    'para_category': 'Resources',
                    'progressive_summarization': True,
                    'intermediate_packets': False
                },
                'lyt': {
                    'create_moc': True,
                    'moc_type': 'book',
                    'update_home': False
                },
                'zettelkasten': {
                    'note_types': ['literature', 'permanent'],
                    'min_permanent_notes': 3,
                    'linking_strategy': 'moderate'
                }
            },
            'fleeting_idea': {
                'basb': {
                    'para_category': 'Inbox',
                    'progressive_summarization': False,
                    'intermediate_packets': False
                },
                'lyt': {
                    'create_moc': False,
                    'update_home': False
                },
                'zettelkasten': {
                    'note_types': ['fleeting'],
                    'min_permanent_notes': 0,
                    'linking_strategy': 'minimal'
                }
            }
        }

        return framework_map.get(content_type, framework_map['fleeting_idea'])

    def _select_templates(self, content_type: str, framework_plan: Dict) -> List[str]:
        """Seleciona templates apropriados"""

        template_map = {
            'academic_paper': ['academic-literature', 'concept-academic'],
            'book_chapter': ['book-note', 'concept'],
            'fleeting_idea': ['fleeting'],
            'project': ['project-basb'],
            'moc': ['moc-lyt']
        }

        return template_map.get(content_type, ['default'])

    def _infer_taxonomy(self, raw_text: str, metadata: Dict) -> Dict:
        """Infere taxonomia usando LLM + heurísticas"""

        # Heurísticas simples
        domain_keywords = {
            'neuroscience': ['brain', 'neuron', 'synapse', 'cortex'],
            'philosophy': ['epistemology', 'metaphysics', 'ontology'],
            'systems': ['complex', 'emergence', 'feedback loop']
        }

        text_lower = raw_text.lower()
        detected_domains = []

        for domain, keywords in domain_keywords.items():
            if any(kw in text_lower for kw in keywords):
                detected_domains.append(domain)

        # LLM refinement
        llm_taxonomy = self._llm_infer_taxonomy(raw_text[:3000])

        return {
            'domains': detected_domains or [llm_taxonomy['domain']],
            'subdomain': llm_taxonomy.get('subdomain'),
            'tags': self._generate_hierarchical_tags(llm_taxonomy)
        }

    def _generate_hierarchical_tags(self, llm_taxonomy: Dict) -> List[str]:
        """Gera tags hierárquicas"""
        tags = []

        domain = llm_taxonomy.get('domain')
        subdomain = llm_taxonomy.get('subdomain')

        if domain:
            if subdomain:
                tags.append(f"{domain}/{subdomain}")
            else:
                tags.append(domain)

        # Add type tags
        content_type = llm_taxonomy.get('type')
        if content_type:
            tags.append(f"type/{content_type}")

        return tags

    def _validate_classification(self, output: Dict) -> Dict:
        checks = {}

        # Check 1: Content type identificado
        checks['content_type_identified'] = {
            'passed': output['content_type'] in [
                'academic_paper', 'book_chapter', 'fleeting_idea', 'project', 'moc'
            ],
            'message': 'Content type deve ser válido',
            'value': output['content_type']
        }

        # Check 2: Framework plan completo
        required_frameworks = ['basb', 'lyt', 'zettelkasten']
        checks['framework_plan_complete'] = {
            'passed': all(f in output['framework_plan'] for f in required_frameworks),
            'message': f'Framework plan deve ter: {required_frameworks}',
            'value': list(output['framework_plan'].keys())
        }

        # Check 3: Taxonomia definida
        checks['taxonomy_defined'] = {
            'passed': 'domains' in output['taxonomy'] and len(output['taxonomy']['domains']) > 0,
            'message': 'Pelo menos 1 domínio deve ser identificado',
            'value': output['taxonomy'].get('domains', [])
        }

        # Check 4: Templates selecionados
        checks['templates_selected'] = {
            'passed': len(output['templates']) > 0,
            'message': 'Pelo menos 1 template deve ser selecionado',
            'value': output['templates']
        }

        all_passed = all(c['passed'] for c in checks.values())

        return {
            'passed': all_passed,
            'checks': checks
        }
```

**Output:**
```json
{
  "content_type": "academic_paper",
  "framework_plan": {
    "basb": {
      "para_category": "Resources",
      "progressive_summarization": true,
      "intermediate_packets": true
    },
    "lyt": {
      "create_moc": true,
      "moc_type": "discipline",
      "update_home": false
    },
    "zettelkasten": {
      "note_types": ["literature", "permanent"],
      "min_permanent_notes": 5,
      "linking_strategy": "aggressive"
    }
  },
  "templates": ["academic-literature", "concept-academic"],
  "taxonomy": {
    "domains": ["neuroscience"],
    "subdomain": "cellular",
    "tags": [
      "neuro/cellular",
      "concept/mechanism",
      "evidence/empirical"
    ]
  },
  "para_path": "3-Resources/41-Neuroscience"
}
```

---

### Agente 3: DESTILADOR

**Input:**
```json
{
  "raw_text": "...",
  "metadata": {...},
  "framework_plan": {...},
  "taxonomy": {...}
}
```

**Process:**
```python
class DestiladorAgent:
    def process(self, input_msg: Dict) -> Dict:
        raw_text = input_msg['raw_text']
        metadata = input_msg['metadata']
        framework_plan = input_msg['framework_plan']
        taxonomy = input_msg['taxonomy']

        # 1. Identificar conceitos atômicos (LLM)
        concepts = self._identify_atomic_concepts(
            raw_text,
            min_concepts=framework_plan['zettelkasten']['min_permanent_notes'],
            max_concepts=15
        )

        # 2. Criar nota de literatura (se aplicável)
        notes = []
        if 'literature' in framework_plan['zettelkasten']['note_types']:
            lit_note = self._create_literature_note(raw_text, metadata, taxonomy)
            notes.append(lit_note)

        # 3. Criar notas permanentes para cada conceito
        if 'permanent' in framework_plan['zettelkasten']['note_types']:
            for concept in concepts:
                perm_note = self._create_permanent_note(
                    concept,
                    raw_text,
                    metadata,
                    taxonomy
                )
                notes.append(perm_note)

        output = {
            "notes": notes,
            "stats": {
                "total_notes": len(notes),
                "literature_notes": sum(1 for n in notes if n['type'] == 'literature'),
                "permanent_notes": sum(1 for n in notes if n['type'] == 'permanent')
            }
        }

        validation = self._validate_distillation(output, framework_plan)

        return {
            "output": output,
            "validation": validation
        }

    def _identify_atomic_concepts(
        self,
        raw_text: str,
        min_concepts: int,
        max_concepts: int
    ) -> List[Dict]:
        """LLM identifica conceitos atômicos"""

        prompt = f"""Analise o texto a seguir e identifique {min_concepts}-{max_concepts} conceitos atômicos.

Para cada conceito, forneça:
1. **title**: Título claro (2-5 palavras)
2. **definition**: Definição em 1-2 frases
3. **context**: Por que é importante (2-3 frases)
4. **relations**: Relações com outros conceitos identificados

Critérios:
- Cada conceito deve ser ATÔMICO (1 ideia completa)
- Deve ser STANDALONE (entendível sozinho)
- Deve ser ÚTIL (aplicável ou fundamental)

Texto:
---
{raw_text[:8000]}
---

Responda em JSON:
{{
  "concepts": [
    {{
      "title": "...",
      "definition": "...",
      "context": "...",
      "relations": ["Conceito 1", "Conceito 2"]
    }}
  ]
}}
"""

        response = self.llm.generate(prompt, json_mode=True)
        data = json.loads(response)

        return data['concepts']

    def _create_permanent_note(
        self,
        concept: Dict,
        source_text: str,
        metadata: Dict,
        taxonomy: Dict
    ) -> Dict:
        """Cria nota permanente para um conceito"""

        # Gerar ID único (timestamp)
        note_id = datetime.now().strftime('%Y%m%d%H%M%S%f')

        # Slugify título
        slug = self._slugify(concept['title'])

        # Extrair contexto relevante do texto fonte
        relevant_context = self._extract_context(source_text, concept['title'])

        # Gerar conteúdo usando LLM
        content = self._generate_concept_content(
            concept,
            relevant_context,
            metadata
        )

        # Metadata completo
        note_metadata = {
            'id': note_id,
            'title': concept['title'],
            'type': 'permanent',
            'status': 'seedling',
            'domain': taxonomy['domains'][0] if taxonomy['domains'] else None,
            'subdomain': taxonomy.get('subdomain'),
            'tags': taxonomy['tags'],
            'basb': {
                'para': None,  # Será preenchido pelo Anatomista
                'progressive_summary': {'layer': 0, 'last_summarized': None},
                'intermediate_packet': False
            },
            'lyt': {
                'mocs': [],
                'fluid_framework': None
            },
            'zettelkasten': {
                'connections_count': 0,
                'centrality_score': 0.0,
                'cluster_id': None
            },
            'source': {
                'type': metadata.get('source_type'),
                'title': metadata.get('title'),
                'authors': metadata.get('authors', []),
                'year': metadata.get('year'),
                'doi': metadata.get('doi')
            },
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat(),
            'reviewed': 0,
            'last_reviewed': None,
            'next_review': (datetime.now() + timedelta(days=7)).isoformat(),
            'version': 1,
            'confidence': 0.75,
            'completeness': 0.6,
            'importance': 'medium'
        }

        return {
            'id': note_id,
            'slug': slug,
            'title': concept['title'],
            'type': 'permanent',
            'content': content,
            'metadata': note_metadata,
            'relations_planned': concept.get('relations', [])
        }

    def _generate_concept_content(
        self,
        concept: Dict,
        context: str,
        source_metadata: Dict
    ) -> str:
        """LLM gera conteúdo estruturado da nota"""

        prompt = f"""Crie uma nota atômica sobre: {concept['title']}

Definição: {concept['definition']}
Contexto: {concept.get('context', '')}

Texto fonte (para referência):
{context[:3000]}

Estrutura da nota:
1. Definição atômica (1-2 frases)
2. Essência do conceito (2-3 parágrafos)
3. Detalhamento (componentes, mecanismos)
4. Aplicações práticas
5. Evidências (se houver no texto)

Requisitos:
- Português (pt-BR)
- Markdown limpo
- Use callouts (> [!abstract], > [!tip], etc.)
- Standalone (não assume conhecimento prévio)

Não inclua frontmatter (será adicionado automaticamente).
"""

        content = self.llm.generate(prompt, temperature=0.4)

        # Ensure título está presente
        if not content.startswith('#'):
            content = f"# {concept['title']}\n\n{content}"

        return content

    def _validate_distillation(self, output: Dict, framework_plan: Dict) -> Dict:
        checks = {}

        notes = output['notes']

        # Check 1: Mínimo de notas criadas
        min_required = framework_plan['zettelkasten']['min_permanent_notes']
        checks['min_notes_created'] = {
            'passed': len(notes) >= min_required,
            'message': f'Mínimo {min_required} notas permanentes',
            'value': len(notes)
        }

        # Check 2: Todas notas têm título único
        titles = [n['title'] for n in notes]
        checks['unique_titles'] = {
            'passed': len(titles) == len(set(titles)),
            'message': 'Títulos devem ser únicos',
            'value': len(set(titles))
        }

        # Check 3: Todas notas têm conteúdo
        checks['all_have_content'] = {
            'passed': all(len(n['content']) > 100 for n in notes),
            'message': 'Todas notas devem ter >100 caracteres',
            'value': min(len(n['content']) for n in notes)
        }

        # Check 4: Metadata completo
        required_fields = ['id', 'title', 'type', 'domain', 'tags']
        checks['metadata_complete'] = {
            'passed': all(
                all(f in n['metadata'] for f in required_fields)
                for n in notes
            ),
            'message': f'Metadata deve conter: {required_fields}'
        }

        all_passed = all(c['passed'] for c in checks.values())

        return {
            'passed': all_passed,
            'checks': checks
        }
```

**Output:**
```json
{
  "notes": [
    {
      "id": "20250115143022001",
      "slug": "potenciacao-de-longo-prazo-ltp",
      "title": "Potenciação de Longo Prazo (LTP)",
      "type": "permanent",
      "content": "# Potenciação de Longo Prazo (LTP)\n\n> [!abstract] Definição...",
      "metadata": {...},
      "relations_planned": ["Consolidação de Memória", "Receptores NMDA"]
    },
    ...
  ],
  "stats": {
    "total_notes": 13,
    "literature_notes": 1,
    "permanent_notes": 12
  }
}
```

---

## 🔄 WORKFLOW COMPLETO (Orquestração)

### Athena Orchestrator

```python
class AthenaOrchestrator:
    """
    Orquestrador principal que coordena todos os agentes
    """

    def __init__(self):
        self.agents = {
            'extrator': ExtratorAgent(),
            'classificador': ClassificadorAgent(),
            'destilador': DestiladorAgent(),
            'anatomista': AnatomistAgent(),
            'conector': ConectorAgent(),
            'curador': CuradorAgent(),
            'sintetizador': SintetizadorAgent()
        }

    def process_file(self, file_path: str) -> Dict:
        """
        Processa um arquivo através do pipeline completo
        """
        workflow_id = str(uuid4())

        self.log(f"🎼 Iniciando workflow {workflow_id}")
        self.log(f"📄 Arquivo: {file_path}")

        # Pipeline
        pipeline = [
            ('extrator', {}),
            ('classificador', {}),
            ('destilador', {}),
            ('anatomista', {}),
            ('conector', {}),
            ('curador', {}),
            ('sintetizador', {})
        ]

        # Estado do workflow
        state = {
            'workflow_id': workflow_id,
            'file_path': file_path,
            'current_step': 0,
            'data': {},
            'reports': []
        }

        # Executar pipeline
        for step_num, (agent_name, agent_config) in enumerate(pipeline, 1):
            state['current_step'] = step_num

            self.log(f"\n{'='*60}")
            self.log(f"STEP {step_num}/{ len(pipeline)}: {agent_name.upper()}")
            self.log(f"{'='*60}")

            try:
                # Executar agente
                result = self._execute_agent(
                    agent_name,
                    state['data'],
                    agent_config
                )

                # Validar output
                if not result['validation']['passed']:
                    self.log(f"❌ Validação falhou em {agent_name}")
                    self._print_validation_errors(result['validation'])

                    # Decisão: continuar ou abortar?
                    if self._has_critical_failures(result['validation']):
                        raise WorkflowException(f"Falha crítica em {agent_name}")

                # Atualizar estado
                state['data'].update(result['output'])
                state['reports'].append({
                    'step': step_num,
                    'agent': agent_name,
                    'status': 'completed',
                    'validation': result['validation'],
                    'metadata': result.get('metadata', {})
                })

                self.log(f"✅ {agent_name} completado")

            except Exception as e:
                self.log(f"❌ Erro em {agent_name}: {str(e)}")
                state['reports'].append({
                    'step': step_num,
                    'agent': agent_name,
                    'status': 'failed',
                    'error': str(e)
                })
                raise

        # Gerar relatório final
        final_report = self._generate_final_report(state)

        return {
            'workflow_id': workflow_id,
            'status': 'completed',
            'output': state['data'],
            'report': final_report
        }

    def _execute_agent(
        self,
        agent_name: str,
        current_data: Dict,
        config: Dict
    ) -> Dict:
        """Executa um agente específico"""

        agent = self.agents[agent_name]

        # Preparar input baseado no agente
        input_data = self._prepare_agent_input(agent_name, current_data)

        # Timestamp
        start_time = time.time()

        # Executar
        result = agent.process(input_data)

        # Metadata
        elapsed = time.time() - start_time
        result['metadata'] = {
            'duration_ms': int(elapsed * 1000),
            'timestamp': datetime.now().isoformat()
        }

        return result

    def _prepare_agent_input(self, agent_name: str, data: Dict) -> Dict:
        """Prepara input específico para cada agente"""

        input_map = {
            'extrator': lambda d: {
                'file_path': d.get('file_path')
            },
            'classificador': lambda d: {
                'raw_text': d['raw_text'],
                'metadata': d['metadata'],
                'structure': d['structure']
            },
            'destilador': lambda d: {
                'raw_text': d['raw_text'],
                'metadata': d['metadata'],
                'framework_plan': d['framework_plan'],
                'taxonomy': d['taxonomy']
            },
            'anatomista': lambda d: {
                'notes': d['notes'],
                'templates': d['templates'],
                'para_path': d['para_path']
            },
            'conector': lambda d: {
                'notes': d['structured_notes'],
                'vault_graph': self._load_vault_graph()
            },
            'curador': lambda d: {
                'new_notes': d['linked_notes'],
                'vault_path': self.config['vault_path']
            },
            'sintetizador': lambda d: {
                'vault_graph': self._load_vault_graph(),
                'new_notes': d['linked_notes']
            }
        }

        return input_map[agent_name](data)

    def _has_critical_failures(self, validation: Dict) -> bool:
        """Verifica se há falhas críticas"""
        for check_name, check_result in validation['checks'].items():
            if not check_result['passed'] and check_result.get('critical', False):
                return True
        return False

    def _generate_final_report(self, state: Dict) -> str:
        """Gera relatório markdown final"""

        # Template do relatório
        template = """
# ✅ Processamento Concluído

## 📄 Input
- **Arquivo:** {file_name}
- **Workflow ID:** {workflow_id}

## 🤖 Execução

{execution_steps}

## 📝 Output

### Notas Criadas ({total_notes})

{notes_list}

### MOCs Sugeridos ({total_mocs})

{mocs_list}

### Insights Emergentes ({total_insights})

{insights_list}

## 🔗 Grafo Atualizado

```
Antes:  {before_notes} notas, {before_links} links
Depois: {after_notes} notas, {after_links} links
Δ: +{delta_notes} notas, +{delta_links} links
```

## 📊 Qualidade

{quality_table}

## ⏱️ Performance

- **Total:** {total_time}
- **Mais lento:** {slowest_agent} ({slowest_time})
- **Mais rápido:** {fastest_agent} ({fastest_time})

## 🎯 Próximos Passos

{next_steps}

---

**Tudo salvo em:** `{para_path}`
**Abrir vault:** `cerebrum open`
        """

        # Preencher template
        ...

        return report_md
```

---

## 📋 CHECKLISTS PROGRAMÁTICOS

### Validation Schemas (JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "definitions": {
    "Note": {
      "type": "object",
      "required": ["id", "title", "type", "content", "metadata"],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[0-9]{17,}$"
        },
        "title": {
          "type": "string",
          "minLength": 3,
          "maxLength": 200
        },
        "type": {
          "enum": ["fleeting", "literature", "permanent", "moc", "project"]
        },
        "content": {
          "type": "string",
          "minLength": 100
        },
        "metadata": {
          "$ref": "#/definitions/Metadata"
        }
      }
    },
    "Metadata": {
      "type": "object",
      "required": ["domain", "tags", "created"],
      "properties": {
        "domain": {"type": "string"},
        "tags": {
          "type": "array",
          "items": {"type": "string"},
          "minItems": 1
        }
      }
    }
  }
}
```

---

## 🚦 SISTEMA DE LOGS E OBSERVABILIDADE

### Log Format

```json
{
  "timestamp": "2025-01-15T14:30:22.123Z",
  "workflow_id": "uuid",
  "step": 3,
  "agent": "Destilador",
  "level": "INFO",  // DEBUG, INFO, WARNING, ERROR, CRITICAL
  "message": "Identificados 12 conceitos atômicos",
  "data": {
    "concepts_count": 12,
    "llm_tokens": 5600
  }
}
```

### Metrics Tracking

```python
class MetricsCollector:
    def __init__(self):
        self.metrics = defaultdict(list)

    def record_agent_execution(self, agent_name: str, duration_ms: int):
        self.metrics[f"{agent_name}_duration"].append(duration_ms)

    def record_llm_call(self, tokens: int, cost_usd: float):
        self.metrics['llm_tokens'].append(tokens)
        self.metrics['llm_cost'].append(cost_usd)

    def record_notes_created(self, count: int):
        self.metrics['notes_created'].append(count)

    def get_summary(self) -> Dict:
        return {
            'total_workflows': len(self.metrics['workflow_id']),
            'avg_duration_ms': statistics.mean(self.metrics['total_duration']),
            'total_llm_cost': sum(self.metrics['llm_cost']),
            'total_notes_created': sum(self.metrics['notes_created'])
        }
```

---

## 🎯 PRÓXIMOS PASSOS

Esta documentação fornece os POPs técnicos. Próximos documentos a criar:

1. **IMPLEMENTATION_PHASES.md** - Como implementar progressivamente
2. **AGENT_PROMPTS.md** - Prompts otimizados para cada agente
3. **TESTING_STRATEGY.md** - Testes automatizados de cada agente

**Quer que eu crie qual primeiro?**
