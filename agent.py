import os
import sys
import subprocess
import ollama
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

SUPPORTED_EXTENSIONS = {".py", ".html", ".js", ".css", ".txt", ".md", ".json", ".yaml", ".yml", ".env", ".cfg", ".ini", ".sql"}
SKIP_DIRS = {"__pycache__", ".git", "node_modules", "venv", ".venv", "env", "migrations", "staticfiles", "media", "static", "locale", ".pytest_cache", "drf-yasg", "temp", "swagger-ui-dist", "redoc", "site-packages", "lib", "bin", "include"}
MAX_FILE_SIZE_KB = 50

# These files are always read first with full content
PRIORITY_FILES = {"settings.py", "change.py", "models.py", "urls.py", "views.py", "serializers.py"}
MODEL = "qwen2.5-coder:7b"


def scan_project(project_path: str) -> dict:
    """Scan project and return file contents, priority files first."""
    priority = {}
    normal = {}
    for root, dirs, filenames in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in filenames:
            ext = os.path.splitext(fname)[1]
            if ext not in SUPPORTED_EXTENSIONS:
                continue
            fpath = os.path.join(root, fname)
            if os.path.getsize(fpath) > MAX_FILE_SIZE_KB * 1024:
                continue
            rel_path = os.path.relpath(fpath, project_path)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                if fname in PRIORITY_FILES:
                    priority[rel_path] = content
                else:
                    normal[rel_path] = content
            except Exception:
                pass
    return {**priority, **normal}


def build_context(files: dict, query: str, max_chars: int = 60000) -> str:
    """Build query-aware context — relevant files first."""
    query_lower = query.lower()
    query_words = set(query_lower.split())

    def relevance(item):
        path, content = item
        path_lower = path.lower()
        score = 0
        # priority filenames always rank high
        fname = os.path.basename(path_lower)
        if fname in {"settings.py", "change.py"}:
            score += 100
        if fname in {"models.py", "views.py", "serializers.py", "urls.py"}:
            score += 50
        # query word matches in path or content
        for word in query_words:
            if len(word) > 3:
                if word in path_lower:
                    score += 20
                if word in content.lower():
                    score += 10
        return score

    sorted_files = sorted(files.items(), key=relevance, reverse=True)
    lines = []
    total = 0
    for path, content in sorted_files:
        snippet = f"\n### FILE: {path}\n{content[:3000]}"
        if total + len(snippet) > max_chars:
            break
        lines.append(snippet)
        total += len(snippet)
    return "\n".join(lines)


def get_git_status(project_path: str) -> str:
    try:
        result = subprocess.run(["git", "status", "--short"], cwd=project_path, capture_output=True, text=True, timeout=5)
        return result.stdout.strip() or "No uncommitted changes"
    except Exception:
        return "Not a git repo or git not available"


def ask_agent(query: str, project_path: str):
    console.print(f"\n[bold cyan]Scanning project:[/bold cyan] {project_path}")
    files = scan_project(project_path)
    console.print(f"[green]Found {len(files)} files[/green]")

    project_context = build_context(files, query)
    git_status = get_git_status(project_path)

    system_prompt = """You are an expert Python/Django debugging assistant.
You are given a project's source code and a developer's query.
Your job is to:
1. Understand what the query is about
2. Find the relevant files and code sections
3. Explain clearly what is happening
4. Give specific, actionable next steps
5. Show code fixes if needed

Be concise, specific, and practical. Reference actual file names and line content from the project."""

    user_message = f"""PROJECT FILES:
{project_context}

GIT STATUS:
{git_status}

DEVELOPER QUERY:
{query}

Please analyze the project and answer the query with:
- What is happening (root cause)
- Where it is happening (file + area)
- What to do next (step-by-step)
- Code fix if applicable"""

    console.print("\n[bold yellow]Thinking...[/bold yellow]\n")

    response_text = ""
    with console.status("[bold green]Agent is analyzing your project...[/bold green]"):
        response = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            stream=False,
        )
        response_text = response["message"]["content"]

    console.print(Panel(Markdown(response_text), title="[bold green]Agent Response[/bold green]", border_style="green"))


def setup_check():
    """Check if ollama is running and model is available."""
    try:
        models = ollama.list()
        available = [m["model"] for m in models.get("models", [])]
        if not any(MODEL in m for m in available):
            console.print(f"[yellow]Model '{MODEL}' not found. Pulling now (first time only, ~2GB)...[/yellow]")
            subprocess.run(["ollama", "pull", MODEL], check=True)
    except Exception as e:
        console.print(f"[red]Ollama not running. Start it with: ollama serve[/red]")
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


def main():
    console.print(Panel("[bold]Local Project Debugging Agent[/bold]\nNo API tokens. Runs fully offline on Windows, macOS and Linux.", border_style="cyan"))

    project_path = input("\nEnter your project path (or press Enter for current dir): ").strip()
    if not project_path:
        project_path = os.getcwd()
    if not os.path.isdir(project_path):
        console.print(f"[red]Path not found: {project_path}[/red]")
        sys.exit(1)

    setup_check()

    console.print("\n[bold]Ask anything about your project.[/bold] Type 'exit' to quit.\n")
    while True:
        try:
            query = input("Your query: ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[cyan]Goodbye![/cyan]")
            break
        if query.lower() in ("exit", "quit", "q"):
            console.print("[cyan]Goodbye![/cyan]")
            break
        if not query:
            continue
        ask_agent(query, project_path)


if __name__ == "__main__":
    main()
