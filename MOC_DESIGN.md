# MOC Auto-Creation Design - v0.4

**Goal:** Automatically create and maintain Maps of Content (MOCs) that organize atomic notes into meaningful clusters.

**Target:** LYT framework score 3/10 → 7/10

---

## 1. Current State Analysis

### What We Have
- ✅ Classificador suggests 2-4 MOC names per source (field: `lyt_mocs`)
- ✅ Vault structure has `04-MOCs/` folder
- ✅ Permanent notes have domain, subdomain, tags in frontmatter
- ✅ Semantic connections already created (4-8 links per note)

### What's Missing
- ❌ MOC notes are never created
- ❌ No clustering algorithm to group related notes
- ❌ No MOC updates when new notes are added

---

## 2. Design Philosophy

### Apple Principles
- **It just works:** MOCs created automatically, no user action required
- **Minimal:** Only create MOCs when there's value (≥5 notes in cluster)
- **Beautiful:** Clean, question-driven templates

### LYT Principles
- **Maps organize journeys:** MOCs are entry points to knowledge domains
- **Heterarchical:** Notes can belong to multiple MOCs
- **Emergent:** MOCs form naturally from note connections

### Epistemic Principles
- **Prompts > Instructions:** Questions guide thinking
- **Status progression:** MOCs mature as notes accumulate (Seedling → Evergreen)
- **Evidence-based:** Show note clusters explicitly

---

## 3. MOC Creation Algorithm

### Strategy: Hybrid (Suggested + Emergent)

#### Phase 1: Suggested MOCs (Immediate)
When processing a source:
1. Classificador suggests 2-4 MOC names
2. Check if MOC already exists in vault
3. If not exists: Create MOC with current permanent notes
4. If exists: Update MOC by adding new notes

**Clustering logic for suggested MOCs:**
- Include all permanent notes from current source that match:
  - Same domain OR
  - ≥2 shared tags OR
  - Mentioned in connections

#### Phase 2: Emergent MOCs (Future - v1.0)
Periodically scan vault:
1. Detect clusters using embeddings (ChromaDB)
2. Find dense connection graphs (≥5 notes, ≥10 links)
3. Suggest new MOCs based on patterns

**For v0.4: Focus on Phase 1 only**

---

## 4. MOC Agent Responsibilities

### Inputs
- List of permanent notes (from current processing)
- Classification result (with suggested MOC names)
- Existing vault state (to detect existing MOCs)

### Outputs
- List of MOC notes (created or updated)
- Stats: MOCs created, MOCs updated, notes added to MOCs

### Core Methods

```python
class MOCAgent:
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.mocs_path = vault_path / '04-MOCs'

    def create_or_update_mocs(
        self,
        permanent_notes: List[Note],
        classification: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Main method: create/update MOCs for permanent notes."""

        suggested_mocs = classification.get('lyt_mocs', [])

        mocs_created = []
        mocs_updated = []

        for moc_name in suggested_mocs:
            # Get relevant notes for this MOC
            relevant_notes = self._cluster_notes_for_moc(
                moc_name, permanent_notes, classification
            )

            if len(relevant_notes) < 3:
                # Skip MOCs with too few notes
                continue

            # Check if MOC exists
            existing_moc = self._find_existing_moc(moc_name)

            if existing_moc:
                # Update existing MOC
                updated_moc = self._update_moc(
                    existing_moc, relevant_notes
                )
                mocs_updated.append(updated_moc)
            else:
                # Create new MOC
                new_moc = self._create_moc(
                    moc_name, relevant_notes, classification
                )
                mocs_created.append(new_moc)

        return {
            'mocs_created': mocs_created,
            'mocs_updated': mocs_updated,
            'stats': {
                'mocs_created_count': len(mocs_created),
                'mocs_updated_count': len(mocs_updated)
            }
        }

    def _cluster_notes_for_moc(
        self,
        moc_name: str,
        notes: List[Note],
        classification: Dict[str, Any]
    ) -> List[Note]:
        """Determine which notes belong to this MOC."""

        # For v0.4: Simple heuristic
        # All notes from same source belong to same MOC
        # (because they share domain/subdomain)

        return notes

    def _find_existing_moc(self, moc_name: str) -> Optional[Note]:
        """Find existing MOC by name."""

        moc_id = self._slugify(moc_name)
        moc_file = self.mocs_path / f"{moc_id}.md"

        if moc_file.exists():
            return self._load_moc(moc_file)

        return None

    def _create_moc(
        self,
        moc_name: str,
        notes: List[Note],
        classification: Dict[str, Any]
    ) -> Note:
        """Create new MOC note."""

        moc_id = self._slugify(moc_name)

        # Create MOC metadata
        metadata = NoteMetadata(
            id=moc_id,
            title=moc_name,
            type='moc',
            status='seedling',
            domain=classification.get('domain'),
            subdomain=classification.get('subdomain'),
            tags=['lyt/moc', f"domain/{classification.get('domain')}"],
            moc_note_count=len(notes),
            created=datetime.now().isoformat()
        )

        # Render MOC body
        body = self._render_moc_template(
            moc_name, notes, classification
        )

        return Note(metadata=metadata, content=body)

    def _update_moc(
        self,
        existing_moc: Note,
        new_notes: List[Note]
    ) -> Note:
        """Update existing MOC with new notes."""

        # Parse existing note links from MOC
        existing_links = self._extract_note_links(existing_moc.content)

        # Add new notes (avoid duplicates)
        new_note_titles = [n.metadata.title for n in new_notes]
        combined_titles = list(set(existing_links + new_note_titles))

        # Update note count in metadata
        existing_moc.metadata.moc_note_count = len(combined_titles)

        # Update status based on note count
        if len(combined_titles) >= 15:
            existing_moc.metadata.status = 'evergreen'
        elif len(combined_titles) >= 8:
            existing_moc.metadata.status = 'budding'

        # Re-render MOC with updated note list
        # (preserves manual edits in other sections)
        existing_moc.content = self._update_moc_note_list(
            existing_moc.content, combined_titles
        )

        return existing_moc

    def _render_moc_template(
        self,
        moc_name: str,
        notes: List[Note],
        classification: Dict[str, Any]
    ) -> str:
        """Render MOC template (Apple + Epistemic style)."""

        # See section 5 below
```

---

## 5. MOC Template Design

### Structure

```markdown
# 🗺️ {MOC Name}

> [!abstract] Map of Content
> **Domain:** {domain} / {subdomain}
> **Status:** 🌱 Seedling ({note_count} notes)
> **Purpose:** Navigate and synthesize knowledge in this area

---

## 🎯 What Is This Map About?

> [!question] Core Questions
> - What is the central theme connecting these notes?
> - Why did these ideas cluster together?
> - What journey does this map enable?

{Auto-generated description based on domain/subdomain}

---

## 🗺️ The Landscape

> [!tip] Navigate this knowledge domain
> Below are atomic notes organized by theme

### Core Concepts
{List of permanent notes - automatically maintained}

- [[Note 1]]
- [[Note 2]]
- [[Note 3]]
...

### Related Maps
> [!info] Connected MOCs

- [[Related MOC 1]]
- [[Related MOC 2]]

---

## 💡 Why Does This Matter?

> [!question] Significance
> - What problems does this knowledge solve?
> - What projects could benefit from this?
> - What becomes possible with this understanding?

**Your answer:**
-

---

## 🔬 Synthesis & Insights

> [!tip] Emergent patterns across these notes
> As you review notes in this map, capture emerging insights:

**Patterns I've noticed:**
-

**Connections to other maps:**
-

**Surprising insights:**
-

---

## 📋 Curated Paths

> [!example] Suggested reading sequences
> Different paths through this knowledge for different goals

**For beginners:**
1. Start: [[]]
2. Then: [[]]
3. Finally: [[]]

**For deep dive:**
-

**For practical application:**
-

---

## ❓ Open Questions

> [!question] To explore further
> - [ ] What's missing from this map?
> - [ ] What contradictions exist between notes?
> - [ ] What experiments could test these ideas?

**Personal questions:**
-

---

## 🔄 Evolution

> [!info] Map Status
> **Current:** {status_emoji} {status}
>
> **Progress toward Evergreen:**
> - [x] ≥5 notes mapped (Currently: {count})
> - [ ] ≥3 curated paths created
> - [ ] ≥2 synthesis insights captured
> - [ ] Used in at least 1 project

**Update History:**
- {date}: Created with {count} notes
- {date}: Added {n} new notes
- {date}: Reached Budding status

---

## 💭 Personal Notes

> [!tip] Your unique perspective on this domain

**Why I care about this:**


**How I've used this map:**


**Projects that drew from this:**


---

**Meta:** This MOC is auto-maintained by Cerebrum
```

---

## 6. Integration with Orchestrator

### New Pipeline Stage

```
Stages (v0.3):
1. Extractor → 2. Classificador → 3. Destilador → 4. Conector → 5. Save

Stages (v0.4):
1. Extractor → 2. Classificador → 3. Destilador → 4. Conector → 5. MOC → 6. Save
```

### Orchestrator Changes

```python
# In orchestrator.py process() method

# After Stage 4 (Connection), before Stage 5 (Save):

# Stage 5: MOC Creation/Update
if self.verbose:
    print("🗺️  Stage 5: Creating/updating MOCs...")

moc_result = self._run_moc_creation(
    destillation['permanent_notes'],
    classification
)
result.stages['moc'] = moc_result
result.mocs_created = moc_result['stats']['mocs_created_count']
result.mocs_updated = moc_result['stats']['mocs_updated_count']

# Stage 6: Save to vault (now includes MOCs)
if self.verbose:
    print("💾 Stage 6: Saving to vault...")

save_result = self.destilador.save_notes(
    result.literature_note,
    result.permanent_notes
)

# Save MOCs
for moc in moc_result['mocs_created'] + moc_result['mocs_updated']:
    self._save_moc(moc)
```

---

## 7. File Naming Convention

### MOC Files

```
04-MOCs/
├── neuroscience.md           # Domain-level MOC
├── cognitive-neuroscience.md # Subdomain MOC
├── machine-learning.md
└── distributed-systems.md
```

**Naming logic:**
- Slugify MOC name (lowercase, hyphens)
- No timestamps (MOCs are persistent entities)
- Stored in `04-MOCs/` folder

---

## 8. Update Strategy

### When to Update MOCs

**Option 1: Every processing run (v0.4)**
- After processing each source, check if any suggested MOC exists
- If exists, add new permanent notes to MOC
- Simple, reliable, works immediately

**Option 2: Batch update (v1.0)**
- User runs `cerebrum curate --update-mocs`
- Scans entire vault, rebuilds all MOC note lists
- Useful for vault maintenance

**For v0.4: Implement Option 1**

### Update Algorithm

```python
def _update_moc_note_list(existing_content: str, note_titles: List[str]) -> str:
    """Update the note list in MOC while preserving manual edits."""

    # 1. Parse existing content
    # 2. Find "### Core Concepts" section
    # 3. Replace note list between "### Core Concepts" and next "###"
    # 4. Keep all other sections intact (user's manual edits)
    # 5. Update metadata (note count, status, update date)

    # Use regex to find and replace
    pattern = r'(### Core Concepts.*?\n)(.*?)(\n###|$)'

    new_note_list = '\n'.join(f"- [[{title}]]" for title in sorted(note_titles))

    updated = re.sub(
        pattern,
        r'\1' + new_note_list + r'\3',
        existing_content,
        flags=re.DOTALL
    )

    return updated
```

---

## 9. Validation

### MOC Quality Checks

```python
def validate_moc(moc: Note) -> Dict[str, Any]:
    """Validate MOC quality."""

    checks = {
        'has_title': moc.metadata.title is not None,
        'has_domain': moc.metadata.domain is not None,
        'min_notes': moc.metadata.moc_note_count >= 3,
        'has_status': moc.metadata.status in ['seedling', 'budding', 'evergreen'],
        'in_correct_folder': moc in '04-MOCs/'
    }

    return {
        'passed': all(checks.values()),
        'checks': checks
    }
```

---

## 10. User Experience

### Before (v0.3)
```bash
$ cerebrum process paper.pdf

✓ Done · paper.pdf

13 atomic notes  ·  48 connections  ·  87s
```

### After (v0.4)
```bash
$ cerebrum process paper.pdf

✓ Done · paper.pdf

13 atomic notes  ·  48 connections  ·  2 MOCs  ·  87s
```

**Verbose mode:**
```bash
$ cerebrum process paper.pdf --verbose

🧠 Cerebrum · It just works, beautifully

🔌 Initializing AI...
✓ Using ollama (llama3.2)

📄 Stage 1: Extracting...
🏷️  Stage 2: Classifying...
⚗️  Stage 3: Destilling into atomic notes...
🔗 Stage 4: Creating semantic connections...
🗺️  Stage 5: Creating/updating MOCs...
   ✓ Created: Cognitive Neuroscience (8 notes)
   ✓ Updated: Machine Learning (3 notes added)
💾 Stage 6: Saving to vault...

✓ Done · paper.pdf

13 atomic notes  ·  48 connections  ·  2 MOCs  ·  87s

Concepts extracted:
  · Neuroplasticity
  · Long-Term Potentiation
  · Synaptic Plasticity
  · Hebbian Learning
  ...
```

---

## 11. Implementation Plan

### Step 1: Create MOC Agent (2h)
- [x] Design algorithm
- [ ] Implement `MOCAgent` class
- [ ] Implement `_render_moc_template()`
- [ ] Implement `_create_moc()`
- [ ] Implement `_update_moc()`

### Step 2: Integrate with Orchestrator (1h)
- [ ] Add MOC stage to pipeline
- [ ] Update ProcessingResult to include MOC stats
- [ ] Add MOC saving logic

### Step 3: Update CLI Output (30m)
- [ ] Add MOC count to minimal output
- [ ] Add MOC details to verbose output

### Step 4: Test (1h)
- [ ] Test with single PDF
- [ ] Test MOC creation
- [ ] Test MOC update (process second PDF in same domain)
- [ ] Validate MOC template rendering

### Step 5: Document (30m)
- [ ] Update SYSTEM_STATUS.md
- [ ] Create MOC_IMPLEMENTATION.md
- [ ] Update README with MOC features

**Total: ~5 hours**

---

## 12. Success Metrics

### Before (v0.3)
- LYT score: 3/10 (MOCs suggested but not created)
- Manual work: User must create MOCs manually
- Vault navigation: Difficult to find related notes

### After (v0.4)
- LYT score: 7/10 (MOCs auto-created and maintained)
- Manual work: Zero (MOCs created automatically)
- Vault navigation: Easy (MOCs provide entry points)

### Target Improvements
- +0.5 overall system score (8.5 → 9.0)
- User delight: "Wow, it created maps for me!"
- Knowledge organization: Domain-based navigation enabled

---

## 13. Future Enhancements (v1.0)

### Emergent MOC Detection
- Scan vault for dense connection clusters
- Suggest new MOCs based on actual usage patterns
- Machine learning clustering (HDBSCAN on embeddings)

### Smart MOC Organization
- Hierarchical MOCs (domain → subdomain → topic)
- MOC of MOCs (Home note that indexes all MOCs)
- Cross-domain MOCs (interdisciplinary maps)

### Interactive Curation
- `cerebrum curate --mocs` command
- Show MOC health (orphan notes, suggested additions)
- Merge/split MOC suggestions

---

**Status:** Design complete ✅
**Next:** Implement MOC Agent
