# 🧠 Cerebrum Web - Beautiful Knowledge Refinement

**Version:** 0.5.0 - Web Edition
**Design:** Apple minimalism + Obsidian elegance
**Philosophy:** "It just works, beautifully" ✨

---

## 🚀 Quick Start

### 1. Install Dependencies

**Backend:**
```bash
cd cerebrum-web/backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd cerebrum-web/frontend
npm install
```

### 2. Run Development Servers

**Terminal 1 - Backend:**
```bash
cd cerebrum-web/backend
python -m app.main
```
Backend runs on: `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
cd cerebrum-web/frontend
npm run dev
```
Frontend runs on: `http://localhost:5173`

### 3. Open Browser

Navigate to: **http://localhost:5173**

---

## 🎨 Features

✨ **Drag & Drop Upload** - Drop PDF, get atomic notes
⚡ **Real-time Processing** - WebSocket updates
🗺️ **Auto MOCs** - Maps of Content created automatically
🔗 **Semantic Links** - 4-8 connections per note
💜 **Beautiful UI** - Apple/Obsidian inspired design
📱 **Responsive** - Works on all screen sizes

---

## 🏗️ Architecture

### Tech Stack

**Backend:**
- FastAPI - Modern Python API
- WebSocket - Real-time updates
- Cerebrum Pipeline - Existing orchestrator

**Frontend:**
- React 18 + TypeScript
- Vite - Lightning-fast dev
- Tailwind CSS - Utility-first styling
- Framer Motion - Smooth animations
- Zustand - State management

**Design:**
- Fonts: Montserrat (headings) + Poppins (body)
- Colors: Dark mode with purple accents
- Style: Minimalist, clean, elegant

---

## 📁 Project Structure

```
cerebrum-web/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── process.py   # Processing endpoints
│   │   │   │   ├── vault.py     # Vault browser
│   │   │   │   └── settings.py  # Settings
│   │   │   └── websocket.py     # Real-time updates
│   │   ├── models/
│   │   │   ├── request.py       # Request schemas
│   │   │   └── response.py      # Response schemas
│   │   └── services/
│   │       └── processor.py     # Cerebrum integration
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── App.tsx              # Main app component
    │   ├── main.tsx             # Entry point
    │   ├── lib/
    │   │   ├── api.ts           # API client
    │   │   └── websocket.ts     # WebSocket client
    │   ├── store/
    │   │   └── index.ts         # Zustand store
    │   └── styles/
    │       └── globals.css      # Global styles + design system
    ├── index.html
    ├── package.json
    ├── vite.config.ts
    ├── tailwind.config.js
    └── tsconfig.json
```

---

## 🎯 How It Works

### Upload Flow

```
1. User drops PDF
2. Frontend uploads to /api/process
3. Backend returns job_id
4. Frontend connects WebSocket (/ws/process/{job_id})
5. Backend processes file through Cerebrum pipeline
6. WebSocket sends real-time updates
7. Frontend shows progress
8. On completion, displays results
```

### Processing Pipeline

```
PDF → Extractor → Classificador → Destilador → Conector → MOC Agent → Save
        ↓             ↓              ↓            ↓           ↓
    Raw text    Taxonomy    Atomic notes   Links      MOCs    Vault
```

---

## 🎨 Design System

### Colors

```css
/* Primary (Obsidian dark) */
--primary-900: #1a1a1a  /* Background */
--primary-800: #2a2a2a  /* Cards */
--primary-700: #3a3a3a  /* Hover */
--primary-200: #d1d1d1  /* Text */

/* Accent */
--accent-purple: #9b87f5  /* Primary actions */
--accent-green: #4ade80   /* Success */
--accent-red: #f87171     /* Error */
```

### Typography

```css
/* Headings */
font-family: 'Montserrat', sans-serif;

/* Body */
font-family: 'Poppins', sans-serif;

/* Code */
font-family: 'JetBrains Mono', monospace;
```

---

## 🔌 API Endpoints

### Processing

- `POST /api/process` - Upload and process file
- `GET /api/jobs/{job_id}` - Get job status
- `GET /api/jobs` - List all jobs
- `WS /ws/process/{job_id}` - Real-time updates

### Vault

- `GET /api/vault/stats` - Vault statistics
- `GET /api/vault/notes` - List notes
- `GET /api/vault/notes/{id}` - Get note content
- `GET /api/vault/mocs` - List MOCs

### Settings

- `GET /api/settings` - Get settings
- `PUT /api/settings` - Update settings

---

## 🛠️ Development

### Run Tests

```bash
# Backend
cd cerebrum-web/backend
pytest

# Frontend
cd cerebrum-web/frontend
npm test
```

### Build for Production

```bash
# Frontend
cd cerebrum-web/frontend
npm run build

# Serve with backend
cd cerebrum-web/backend
python -m app.main
```

---

## 🎯 Next Steps

**v0.5.1 - Enhancements:**
- [ ] Vault browser with file tree
- [ ] Note preview modal
- [ ] Graph view visualization
- [ ] Batch processing
- [ ] Settings panel
- [ ] Dark/light theme toggle

**v0.6 - Advanced:**
- [ ] Real-time collaboration
- [ ] Mobile app (React Native)
- [ ] Desktop app (Electron)
- [ ] Cloud sync

---

## 🏆 Philosophy

> "Simplicidade é a sofisticação máxima"
> — Leonardo da Vinci

**Cerebrum Web:**
- Sophisticated underneath (6-agent pipeline, semantic AI, vector embeddings)
- Simple on surface (drag, drop, done)
- Beautiful always (Apple design, smooth animations, perfect typography)

**It just works, beautifully.** ✨

---

## 📚 Documentation

- **WEB_UI_DESIGN.md** - Complete design document
- **SYSTEM_STATUS.md** - v0.4 system status
- **V0.4_MAPS_EDITION.md** - MOC features
- **API Docs** - http://localhost:8000/api/docs (when running)

---

## 🎉 Credits

**Frameworks:**
- LYT (Linking Your Thinking) - Nick Milo
- BASB (Building a Second Brain) - Tiago Forte
- Zettelkasten - Niklas Luhmann

**Design Inspiration:**
- Apple.com - Minimalism
- Obsidian - Dark mode, purple accents
- Linear.app - Smooth animations
- Arc Browser - Elegant UI

---

**Happy knowledge refining!** 🧠✨
