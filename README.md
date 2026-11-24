# 🤖 Local Project Debugging Agent

> A fully **offline** AI-powered debugging assistant that runs on your Mac — no API keys, no internet, no cost.

It scans your entire project, understands the code, and answers any question about it using a local LLM (via [Ollama](https://ollama.com)).

---

## 📸 How It Looks

```
╭─────────────────────────────────────────────────────╮
│         Local Project Debugging Agent               │
│   No API tokens. Runs fully on your Mac.            │
╰─────────────────────────────────────────────────────╯

Enter your project path (or press Enter for current dir): /Users/you/myproject

Scanning project: /Users/you/myproject
Found 42 files

Your query: why is my login view returning 403?

Thinking...

╭─────────────────── Agent Response ──────────────────╮
│                                                     │
│  Root Cause: CSRF token missing in your AJAX call   │
│  File: templates/login.html, views.py line 34       │
│  Fix: Add {% csrf_token %} inside your <form> tag   │
│                                                     │
╰─────────────────────────────────────────────────────╯
```

---

## ✨ Features

- 🔍 **Smart project scanner** — reads `.py`, `.html`, `.js`, `.css`, `.json`, `.sql` and more
- 🧠 **Query-aware context** — ranks files by relevance to your question
- ⚡ **Priority files first** — always reads `models.py`, `views.py`, `settings.py`, `urls.py` first
- 🌿 **Git-aware** — shows uncommitted changes as part of context
- 🎨 **Rich terminal UI** — colored output with panels and markdown rendering
- 🔒 **100% offline** — uses [Ollama](https://ollama.com) + `qwen2.5-coder:7b` locally
- 💸 **Zero cost** — no OpenAI, no Anthropic, no API bills

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Core language |
| [Ollama](https://ollama.com) | Local LLM runtime |
| `qwen2.5-coder:7b` | AI model (code-specialized) |
| [Rich](https://github.com/Textualize/rich) | Beautiful terminal output |

---

## 🚀 Quick Start

### Step 1 — Run Setup (one time only)

```bash
cd agent
chmod +x setup.sh
./setup.sh
```

This will:
- Install Ollama if not already installed
- Start the Ollama server
- Pull the `llama3.2` model (~2GB, one-time download)

### Step 2 — Install Python dependencies

```bash
pip install ollama rich
```

### Step 3 — Run the agent

```bash
python3 agent.py
```

---

## 💬 Usage

```
Enter your project path (or press Enter for current dir): /Users/you/myproject

Your query: why is my celery task not running?
Your query: explain what the InvestorProfile model does
Your query: find where the 500 error is coming from
Your query: how does the login flow work?
Your query: exit
```

Type **exit** or **quit** to stop.

---

## 📁 Project Structure

```
agent/
├── agent.py       # Main agent — scans project, builds context, queries LLM
└── setup.sh       # One-time setup script for Ollama + model
```

---

## ⚙️ How It Works

```
Your Query
    │
    ▼
Scan Project Files
(skips venv, node_modules, migrations etc.)
    │
    ▼
Rank Files by Relevance to Query
(priority: settings.py, models.py, views.py, urls.py)
    │
    ▼
Build Context (max 60,000 chars)
    │
    ▼
Send to Local LLM (qwen2.5-coder:7b via Ollama)
    │
    ▼
Get Answer with:
  - Root cause
  - File + line reference
  - Step-by-step fix
  - Code snippet
```

---

## 🔧 Configuration

You can edit these constants at the top of `agent.py`:

| Constant | Default | Description |
|----------|---------|-------------|
| `MODEL` | `qwen2.5-coder:7b` | Ollama model to use |
| `MAX_FILE_SIZE_KB` | `50` | Skip files larger than this |
| `SUPPORTED_EXTENSIONS` | `.py .html .js ...` | File types to scan |
| `SKIP_DIRS` | `venv, node_modules ...` | Directories to ignore |
| `PRIORITY_FILES` | `models.py, views.py ...` | Always read these first |

---

## 📦 Requirements

- macOS (Apple Silicon or Intel)
- Python 3.8+
- [Ollama](https://ollama.com) installed
- ~4GB RAM free for the model

```bash
pip install ollama rich
```

---

## 👨‍💻 Author

**Dungroth Srinivas**
- 📧 dungrothsreenivas143@gmail.com
- 📍 Hyderabad, India
- 🔗 [GitHub](https://github.com/srinivasdungroth)

---

## 📄 License

MIT License — free to use, modify and distribute.
