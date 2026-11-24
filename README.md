# 🤖 Local Project Debugging Agent

> A fully **offline** AI-powered debugging assistant — no API keys, no internet, no cost.  
> Works on **Windows, macOS and Linux**.

Point it at any project folder, ask a question in plain English, and it gives you the root cause, the exact file, and a code fix — all powered by a local LLM running on your own machine.

---

## 📸 How It Looks

```
╭──────────────────────────────────────────────────────────╮
│              Local Project Debugging Agent               │
│  No API tokens. Runs fully offline on Windows,           │
│  macOS and Linux.                                        │
╰──────────────────────────────────────────────────────────╯

Enter your project path (or press Enter for current dir): /home/user/myproject

Scanning project: /home/user/myproject
Found 42 files

Your query: why is my login view returning 403?

Thinking...

╭──────────────────────── Agent Response ─────────────────────────╮
│                                                                  │
│  Root Cause: CSRF token missing in your AJAX POST request        │
│  File: templates/login.html, views.py line 34                    │
│  Fix: Add {% csrf_token %} inside your <form> tag                │
│                                                                  │
╰──────────────────────────────────────────────────────────────────╯
```

---

## ✨ Features

- 🔍 **Smart project scanner** — reads `.py`, `.html`, `.js`, `.css`, `.json`, `.sql` and more
- 🧠 **Query-aware context** — ranks files by relevance to your question automatically
- ⚡ **Priority files first** — always reads `models.py`, `views.py`, `settings.py`, `urls.py` first
- 🌿 **Git-aware** — includes uncommitted changes as part of the context
- 🎨 **Rich terminal UI** — colored panels and markdown rendering in the terminal
- 🔒 **100% offline** — uses [Ollama](https://ollama.com) + `qwen2.5-coder:7b` running locally
- 💸 **Zero cost** — no OpenAI, no Anthropic, no subscriptions
- 🖥️ **Cross-platform** — works on Windows, macOS and Linux

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Core language |
| [Ollama](https://ollama.com) | Local LLM runtime |
| `qwen2.5-coder:7b` | AI model specialized for code |
| [Rich](https://github.com/Textualize/rich) | Terminal UI with colors and panels |

---

## 🚀 Quick Start

### Step 1 — Install Ollama

| OS | Instructions |
|----|-------------|
| **Windows** | Download from [ollama.com/download/windows](https://ollama.com/download/windows) and run the installer |
| **macOS** | Download from [ollama.com/download/mac](https://ollama.com/download/mac) or run `brew install ollama` |
| **Linux** | Run `curl -fsSL https://ollama.com/install.sh \| sh` |

### Step 2 — Run Setup

**macOS / Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```bat
setup.bat
```

This will:
- Pull the `qwen2.5-coder:7b` model (~4GB, one-time download)
- Install Python dependencies (`ollama`, `rich`)

### Step 3 — Run the Agent

```bash
python3 agent.py        # macOS / Linux
python agent.py         # Windows
```

---

## 💬 Usage

```
Enter your project path (or press Enter for current dir): /home/user/myproject

Your query: why is my celery task not running?
Your query: explain what the InvestorProfile model does
Your query: find where the 500 error is coming from
Your query: how does the login flow work?
Your query: exit
```

Type `exit` or `quit` to stop.

---

## 📁 Project Structure

```
agent/
├── agent.py        # Main agent — scans project, builds context, queries LLM
├── setup.sh        # One-time setup for macOS / Linux
├── setup.bat       # One-time setup for Windows
├── requirements.txt
└── README.md
```

---

## ⚙️ How It Works

```
Your Query
    │
    ▼
Scan Project Files
(skips venv, node_modules, migrations, __pycache__ etc.)
    │
    ▼
Rank Files by Relevance to Your Query
(priority: settings.py, models.py, views.py, urls.py)
    │
    ▼
Build Context (max 60,000 characters)
    │
    ▼
Send to Local LLM (qwen2.5-coder:7b via Ollama)
    │
    ▼
Get Answer with:
  - Root cause
  - Exact file + code area
  - Step-by-step fix
  - Code snippet
```

---

## 🔧 Configuration

Edit these constants at the top of `agent.py` to customize behaviour:

| Constant | Default | Description |
|----------|---------|-------------|
| `MODEL` | `qwen2.5-coder:7b` | Ollama model to use |
| `MAX_FILE_SIZE_KB` | `50` | Skip files larger than this size |
| `SUPPORTED_EXTENSIONS` | `.py .html .js .css ...` | File types to include in scan |
| `SKIP_DIRS` | `venv, node_modules, migrations ...` | Directories to skip |
| `PRIORITY_FILES` | `models.py, views.py, settings.py ...` | Always read these files first |

You can swap the model to any Ollama-supported model:

```python
MODEL = "llama3.2"          # Faster, lighter
MODEL = "qwen2.5-coder:7b"  # Better for code (default)
MODEL = "codellama"         # Alternative code model
```

---

## 📦 Requirements

- Python 3.8+
- [Ollama](https://ollama.com) installed and running
- ~4GB free disk space for the model
- ~4GB RAM minimum (8GB recommended)

```bash
pip install ollama rich
```

---

## 🖥️ Platform Support

| Platform | Supported | Setup |
|----------|-----------|-------|
| Windows 10/11 | ✅ | `setup.bat` |
| macOS (Intel & Apple Silicon) | ✅ | `setup.sh` |
| Ubuntu / Debian Linux | ✅ | `setup.sh` |
| Other Linux distros | ✅ | `setup.sh` |

---

## 👨‍💻 Author

**Dungroth Srinivas**
- 📧 dungrothsreenivas143@gmail.com
- 📍 Hyderabad, India
- 🔗 [GitHub](https://github.com/srinivasdungroth)

---

## 📄 License

MIT License — free to use, modify and distribute.
