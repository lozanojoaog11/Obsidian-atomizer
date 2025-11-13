# 🧠 Cerebrum - Personal Knowledge Refinement

Your local, private, AI-powered second brain.

## Quick Start

### 1. Install

```bash
# From this directory
pip install -e .

# With local LLM support (recommended)
pip install -e ".[local]"

# OR with cloud LLM support
pip install -e ".[cloud]"

# OR everything
pip install -e ".[full]"
```

### 2. Setup Ollama (for local LLM)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull model
ollama pull llama3.2:latest
```

### 3. Initialize in your vault

```bash
cd ~/your-obsidian-vault
cerebrum init
```

### 4. Start using!

```bash
# Process a file
cerebrum distill 00-Inbox/paper.pdf

# Process entire inbox
cerebrum distill 00-Inbox/ --auto
```

## Commands

### `cerebrum distill`
Transform raw text into atomic notes.

```bash
# Single file
cerebrum distill paper.pdf

# Directory
cerebrum distill inbox/ --auto

# With specific template
cerebrum distill article.md --template academic
```

### `cerebrum link` (Coming soon)
Suggest semantic connections.

### `cerebrum curate` (Coming soon)
Maintain vault health.

### `cerebrum synthesize` (Coming soon)
Generate emergent insights.

## Configuration

Edit `.cerebrum/config.yaml`:

```yaml
llm:
  provider: ollama  # or 'gemini'
  model: llama3.2:latest
  temperature: 0.3

vault:
  inbox: 00-Inbox
  permanent: 03-Permanent
  mocs: 04-MOCs

taxonomy:
  tags: [note, concept]
  domains: [knowledge, research]
```

## Architecture

```
cerebrum/
├── agents/          # Distiller, Linker, Curator, Synthesizer
├── intelligence/    # LLM service, embeddings
├── vault/           # File operations, parsing
└── utils/           # Config, templates
```

## Roadmap

- [x] Distiller agent (basic)
- [ ] Local embeddings
- [ ] Linker agent
- [ ] Curator agent
- [ ] Synthesizer agent
- [ ] VS Code integration
- [ ] Web interface (optional)

## Privacy

Everything runs locally:
- LLM: Ollama (local)
- Embeddings: Cached locally
- Data: Never leaves your machine

## License

MIT (or whatever you prefer - it's your tool!)
