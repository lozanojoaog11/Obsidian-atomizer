# 🎨 Cerebrum Web UI - Design Document

**Version:** 0.5.0 - Web Edition
**Design Philosophy:** Apple minimalism meets Obsidian elegance
**Status:** In Development

---

## 🎯 Vision

Create a beautiful, intuitive web interface that makes knowledge refinement feel magical—like the best of Apple and Obsidian combined.

**Key Principles:**
- **"It just works, beautifully"** - Zero learning curve
- **Minimalist** - Clean, focused, no clutter
- **Delightful** - Smooth animations, thoughtful interactions
- **Fast** - Instant feedback, optimistic updates
- **Elegant** - Typography, spacing, colors perfected

---

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- **React 18** - Component-based UI
- **Vite** - Lightning-fast dev server
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **React Query** - Server state management
- **Zustand** - Client state management

**Backend:**
- **FastAPI** - Modern Python API framework
- **WebSockets** - Real-time processing updates
- **Uvicorn** - ASGI server
- **Existing Cerebrum pipeline** - Zero changes needed

**Typography:**
- **Montserrat** - Headings (geometric, modern)
- **Poppins** - Body text (friendly, readable)
- **JetBrains Mono** - Code/metadata (monospace)

---

## 🎨 Design System

### Color Palette (Apple-inspired + Obsidian dark mode)

```css
/* Primary */
--primary-900: #1a1a1a;      /* Deep black (bg) */
--primary-800: #2a2a2a;      /* Card bg */
--primary-700: #3a3a3a;      /* Hover bg */
--primary-600: #4a4a4a;      /* Border */
--primary-500: #6a6a6a;      /* Muted text */
--primary-400: #8a8a8a;      /* Secondary text */
--primary-300: #aaaaaa;      /* Tertiary text */
--primary-200: #d1d1d1;      /* Primary text */
--primary-100: #f5f5f5;      /* Bright white */

/* Accent */
--accent-purple: #9b87f5;    /* Primary actions (Obsidian purple) */
--accent-blue: #5e8cff;      /* Links */
--accent-green: #4ade80;     /* Success */
--accent-red: #f87171;       /* Error */
--accent-yellow: #fbbf24;    /* Warning */
--accent-orange: #fb923c;    /* Processing */

/* Semantic */
--success: var(--accent-green);
--error: var(--accent-red);
--warning: var(--accent-yellow);
--info: var(--accent-blue);
--processing: var(--accent-orange);
```

### Typography Scale

```css
/* Montserrat - Headings */
--font-display: 'Montserrat', -apple-system, sans-serif;

/* Poppins - Body */
--font-body: 'Poppins', -apple-system, sans-serif;

/* JetBrains Mono - Code */
--font-mono: 'JetBrains Mono', 'SF Mono', monospace;

/* Scale (1.25 ratio) */
--text-xs: 0.75rem;      /* 12px */
--text-sm: 0.875rem;     /* 14px */
--text-base: 1rem;       /* 16px */
--text-lg: 1.125rem;     /* 18px */
--text-xl: 1.25rem;      /* 20px */
--text-2xl: 1.5rem;      /* 24px */
--text-3xl: 1.875rem;    /* 30px */
--text-4xl: 2.25rem;     /* 36px */
--text-5xl: 3rem;        /* 48px */
```

### Spacing System (8px grid)

```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-24: 6rem;     /* 96px */
```

### Border Radius (Apple-style)

```css
--radius-sm: 6px;     /* Buttons, inputs */
--radius-md: 12px;    /* Cards */
--radius-lg: 16px;    /* Modals */
--radius-xl: 24px;    /* Hero sections */
--radius-full: 9999px; /* Pills */
```

### Shadows (Subtle depth)

```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
--shadow-glow: 0 0 20px rgb(155 135 245 / 0.3); /* Purple glow */
```

---

## 📱 UI Components

### 1. App Shell

**Layout:**
```
┌─────────────────────────────────────────────┐
│  [Logo] Cerebrum          [Status] [Avatar] │ ← Header (64px)
├─────────────────────────────────────────────┤
│                                             │
│                                             │
│              Main Content                   │ ← Content Area
│                                             │
│                                             │
└─────────────────────────────────────────────┘
```

**Header:**
- Logo + wordmark (left)
- Processing status indicator (center)
- User avatar + settings (right)
- Frosted glass effect (backdrop-blur)
- Sticky on scroll

### 2. Home View (Upload Interface)

**Design:**
```
┌─────────────────────────────────────────────┐
│                                             │
│          🧠                                 │
│       Cerebrum                              │
│   It just works, beautifully                │
│                                             │
│   ┌───────────────────────────────┐        │
│   │                                │        │
│   │   📄  Drop PDF here            │        │
│   │   or click to browse           │        │ ← Drop zone
│   │                                │        │
│   └───────────────────────────────┘        │
│                                             │
│   Recent Processing:                        │
│   • paper.pdf  →  13 notes, 2 MOCs          │ ← History
│   • book.pdf   →  28 notes, 4 MOCs          │
│                                             │
└─────────────────────────────────────────────┘
```

**Features:**
- Large drop zone (dashed border, hover effect)
- Drag & drop with visual feedback
- File type validation (PDF only for now)
- Recent processing history
- Empty state with gentle CTA

### 3. Processing View

**Design:**
```
┌─────────────────────────────────────────────┐
│                                             │
│   Processing paper.pdf...                   │
│                                             │
│   ┌───────────────────────────────┐        │
│   │ ████████████░░░░░░░░░░░  65%  │        │ ← Progress bar
│   └───────────────────────────────┘        │
│                                             │
│   Stage 3 of 6: Destilling into atomic notes│
│                                             │
│   ✓ Extraction complete (2.3s)              │
│   ✓ Classification complete (1.1s)          │
│   ⚡ Destilling... (8 notes created)        │ ← Live updates
│   ⏳ Connection pending                     │
│   ⏳ MOC creation pending                   │
│   ⏳ Save pending                           │
│                                             │
└─────────────────────────────────────────────┘
```

**Features:**
- Real-time progress bar
- Stage indicators (current highlighted)
- Live stats (notes created, time elapsed)
- Smooth transitions between stages
- Pulsing animation on active stage

### 4. Results View

**Design:**
```
┌─────────────────────────────────────────────┐
│   ✓ Done · paper.pdf                        │
│                                             │
│   ┌─────────────────────────────────────┐  │
│   │ 13 atomic notes                     │  │
│   │ 48 connections                      │  │ ← Stats cards
│   │ 2 MOCs                             │  │
│   │ 87s                                │  │
│   └─────────────────────────────────────┘  │
│                                             │
│   📝 Permanent Notes                        │
│   ┌─────────────────────────────────────┐  │
│   │ • Neuroplasticity                   │  │
│   │ • Long-Term Potentiation            │  │ ← Note list
│   │ • Synaptic Plasticity               │  │   (clickable)
│   │ • Hebbian Learning                  │  │
│   │   ... 9 more                        │  │
│   └─────────────────────────────────────┘  │
│                                             │
│   🗺️  MOCs Created                         │
│   ┌─────────────────────────────────────┐  │
│   │ ✓ Cognitive Neuroscience (8 notes)  │  │ ← MOC list
│   │ ↻ Machine Learning (12 notes)       │  │
│   └─────────────────────────────────────┘  │
│                                             │
│   [Open in Obsidian]  [Process Another]    │ ← Actions
│                                             │
└─────────────────────────────────────────────┘
```

**Features:**
- Stats cards with icons
- Expandable note lists
- Click note → preview modal
- CTA buttons (primary + secondary)

### 5. Vault Browser

**Design (Split view like Obsidian):**
```
┌─────────────────────────────────────────────┐
│ 📁 Vault Browser                            │
├───────────┬─────────────────────────────────┤
│           │                                 │
│ 📂 MOCs   │ # 🗺️ Cognitive Neuroscience    │
│   • Cog.. │                                 │
│   • ML    │ > Domain: neuroscience          │ ← Note preview
│           │ > Status: 🌿 Budding (12 notes)  │   (markdown
│ 📂 Perm   │                                 │    rendered)
│   • Neur..│ ## 🎯 What Is This Map About?  │
│   • LTP   │                                 │
│           │ This map organizes...           │
│ 📂 Res    │                                 │
│   • paper │                                 │
│           │                                 │
└───────────┴─────────────────────────────────┘
  Sidebar      Content (markdown rendered)
  (200px)
```

**Features:**
- Tree view navigation
- File icons by type
- Search filter
- Markdown rendering
- Graph view button (future)

### 6. Settings Panel

**Design (Modal):**
```
┌─────────────────────────────────────────────┐
│ ⚙️  Settings                        [×]      │
├─────────────────────────────────────────────┤
│                                             │
│ Vault Location                              │
│ ┌─────────────────────────────────────┐    │
│ │ /Users/user/vault                   │    │
│ └─────────────────────────────────────┘    │
│ [Choose Folder]                             │
│                                             │
│ AI Provider                                 │
│ ○ Ollama (llama3.2)  ● Gemini              │
│                                             │
│ Processing Options                          │
│ ☑ Auto-create MOCs                         │
│ ☑ Generate connections                     │
│ ☐ Verbose output                           │
│                                             │
│         [Cancel]  [Save Changes]            │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🎭 Interactions & Animations

### Micro-interactions

**File Drop:**
```
1. Hover → Border pulse (purple glow)
2. Drop → Ripple effect from drop point
3. Accept → Smooth scale in animation
```

**Processing:**
```
1. Start → Fade in progress view
2. Stage change → Slide transition
3. Complete → Confetti burst 🎉
```

**Button Hover:**
```
1. Hover → Scale 1.02, brightness increase
2. Click → Scale 0.98, haptic feedback
3. Loading → Spinner replaces text
```

### Transitions

**Page transitions:**
```css
/* Fade + slide */
.page-enter {
  opacity: 0;
  transform: translateY(10px);
}

.page-enter-active {
  opacity: 1;
  transform: translateY(0);
  transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

**Card animations:**
```css
/* Stagger children */
.card-list > * {
  animation: fadeInUp 400ms ease-out;
  animation-fill-mode: backwards;
}

.card-list > *:nth-child(1) { animation-delay: 0ms; }
.card-list > *:nth-child(2) { animation-delay: 100ms; }
.card-list > *:nth-child(3) { animation-delay: 200ms; }
```

---

## 🔌 Backend API Design

### FastAPI Endpoints

**Core Processing:**
```python
POST /api/process
- Body: { file: File, options: ProcessingOptions }
- Response: { job_id: str }
- WebSocket: /ws/process/{job_id} (real-time updates)

GET /api/jobs/{job_id}
- Response: ProcessingResult

GET /api/jobs
- Response: List[ProcessingResult] (history)
```

**Vault Management:**
```python
GET /api/vault/notes
- Query: folder, type, search
- Response: List[NoteMetadata]

GET /api/vault/notes/{note_id}
- Response: Note (full content + metadata)

GET /api/vault/mocs
- Response: List[MOC]

GET /api/vault/stats
- Response: VaultStats (note count, MOC count, etc.)
```

**Settings:**
```python
GET /api/settings
- Response: Settings

PUT /api/settings
- Body: Settings
- Response: Settings
```

### WebSocket Protocol

**Processing updates:**
```json
{
  "type": "stage_start",
  "stage": "destillation",
  "stage_number": 3,
  "total_stages": 6,
  "message": "Destilling into atomic notes..."
}

{
  "type": "progress",
  "stage": "destillation",
  "progress": 0.65,
  "stats": {
    "notes_created": 8,
    "time_elapsed": 12.5
  }
}

{
  "type": "stage_complete",
  "stage": "destillation",
  "result": {
    "notes_created": 13,
    "duration": 15.2
  }
}

{
  "type": "complete",
  "result": ProcessingResult
}

{
  "type": "error",
  "error": "Failed to extract text from PDF"
}
```

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
│   │   │   │   ├── vault.py     # Vault endpoints
│   │   │   │   └── settings.py  # Settings endpoints
│   │   │   └── websocket.py     # WebSocket handler
│   │   ├── models/
│   │   │   ├── request.py       # Request models
│   │   │   └── response.py      # Response models
│   │   └── services/
│   │       └── processor.py     # Cerebrum integration
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/              # Base components
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   └── ...
│   │   │   ├── features/        # Feature components
│   │   │   │   ├── Upload/
│   │   │   │   ├── Processing/
│   │   │   │   ├── Results/
│   │   │   │   └── Vault/
│   │   │   └── layout/          # Layout components
│   │   │       ├── Header.tsx
│   │   │       └── Shell.tsx
│   │   ├── hooks/
│   │   │   ├── useProcessing.ts
│   │   │   └── useVault.ts
│   │   ├── lib/
│   │   │   ├── api.ts           # API client
│   │   │   └── websocket.ts     # WebSocket client
│   │   ├── store/
│   │   │   └── index.ts         # Zustand store
│   │   ├── styles/
│   │   │   └── globals.css      # Global styles
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
└── README.md
```

---

## 🚀 Development Phases

### Phase 1: Foundation (Week 1)
- ✅ Setup FastAPI backend
- ✅ Create basic API endpoints
- ✅ Setup React + Vite + TypeScript
- ✅ Install Tailwind + Framer Motion
- ✅ Implement design system (tokens, base components)

### Phase 2: Core Features (Week 2)
- ✅ Upload interface
- ✅ Processing view with WebSocket
- ✅ Results view
- ✅ Basic vault browser

### Phase 3: Polish (Week 3)
- ✅ Animations and transitions
- ✅ Settings panel
- ✅ Error handling
- ✅ Responsive design

### Phase 4: Advanced (Week 4)
- ⏳ Graph view
- ⏳ Advanced search
- ⏳ Batch processing
- ⏳ Export functionality

---

## 🎨 Visual References

**Inspiration:**
1. **Apple.com** - Minimalism, typography, spacing
2. **Obsidian** - Dark mode, purple accents, graph view
3. **Linear.app** - Smooth animations, keyboard shortcuts
4. **Raycast** - Clean UI, fast interactions
5. **Arc Browser** - Elegant sidebar, command palette

**Design Principles:**
- **Generous white space** (or dark space in dark mode)
- **Bold typography hierarchy**
- **Subtle shadows and glows**
- **Smooth, fast animations** (60fps)
- **Keyboard-first** (shortcuts for everything)

---

## 🔧 Implementation Notes

### Performance
- Code splitting by route
- Lazy load heavy components
- Virtualize long lists (react-window)
- Debounce search inputs
- Optimistic UI updates

### Accessibility
- Semantic HTML
- ARIA labels
- Keyboard navigation
- Focus management
- Screen reader support

### Mobile
- Responsive breakpoints (640, 768, 1024, 1280)
- Touch-friendly targets (44px minimum)
- Swipe gestures
- Bottom sheet for mobile actions

---

## 📊 Success Metrics

**User Experience:**
- First paint < 1s
- Time to interactive < 2s
- Upload to results < 90s
- Zero learning curve

**Visual Quality:**
- 60fps animations
- Smooth scrolling
- Crisp typography
- Consistent spacing

---

**Next Steps:** Begin Phase 1 implementation with FastAPI backend setup.
