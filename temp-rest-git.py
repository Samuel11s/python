from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse
import difflib


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path.cwd().resolve()

# Si True, le script affiche ce qu'il ferait sans modifier Git.
DRY_RUN = False

# Fichiers/dossiers qu'on ne veut jamais mettre dans l'historique.
IGNORED_NAMES = {
    ".git",
    "temp-rest-git.py",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".env",
    ".idea",
    ".vscode",
}

# Extensions intéressantes pour ton projet Python.
ALLOWED_EXTENSIONS = {
    ".py",
    ".pyw",
    ".pyi",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
}


@dataclass
class HistoryEntry:
    file_path: Path
    history_file: Path
    timestamp: int
    entry_id: str


# ============================================================
# UTILITAIRES GIT
# ============================================================

def run_git(*args, check=True):
    result = subprocess.run(
        ["git", *args],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
    )

    if check and result.returncode != 0:
        print("\n❌ Erreur Git:")
        print(result.stderr.strip())
        sys.exit(result.returncode)

    return result.stdout.strip()


def git_exists():
    try:
        subprocess.run(
            ["git", "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except FileNotFoundError:
        return False


# ============================================================
# LOCAL HISTORY DE VS CODE
# ============================================================

def find_vscode_history():
    """
    Trouve les emplacements habituels du Local History de VS Code.
    """

    system = platform.system()

    candidates = []

    if system == "Windows":
        appdata = os.environ.get("APPDATA")

        if appdata:
            candidates.extend([
                Path(appdata) / "Code" / "User" / "History",
                Path(appdata) / "Code - Insiders" / "User" / "History",
            ])

    elif system == "Darwin":
        home = Path.home()

        candidates.extend([
            home / "Library" / "Application Support" / "Code" / "User" / "History",
            home / "Library" / "Application Support" / "Code - Insiders" / "User" / "History",
        ])

    elif system == "Linux":
        home = Path.home()

        candidates.extend([
            home / ".config" / "Code" / "User" / "History",
            home / ".config" / "Code - Insiders" / "User" / "History",
        ])

    existing = [
        path for path in candidates
        if path.exists() and path.is_dir()
    ]

    return existing


def file_uri_to_path(uri):
    """
    Transforme un file:// URI de VS Code en chemin local.
    """

    parsed = urlparse(uri)

    if parsed.scheme != "file":
        return None

    path = unquote(parsed.path)

    # Windows: /C:/Users/... -> C:/Users/...
    if platform.system() == "Windows":
        if path.startswith("/") and len(path) > 2 and path[2] == ":":
            path = path[1:]

    return Path(path)


def path_belongs_to_project(path):
    """
    Vérifie qu'un fichier appartient réellement au dossier courant.
    """

    try:
        path.resolve().relative_to(PROJECT_ROOT)
        return True
    except ValueError:
        return False


def is_interesting_file(path):
    if not path:
        return False

    if not path_belongs_to_project(path):
        return False

    if any(part in IGNORED_NAMES for part in path.parts):
        return False

    # Pour ton projet Python, on se concentre sur les fichiers intéressants.
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        return False

    return True


# ============================================================
# LECTURE DE L'HISTORIQUE
# ============================================================

def scan_history():
    histories = find_vscode_history()

    if not histories:
        print("❌ Impossible de trouver le Local History de VS Code.")
        print()
        print("Vérifie que tu utilises bien VS Code Desktop et que")
        print("le Local History est activé.")
        sys.exit(1)

    print("📚 Historique(s) VS Code trouvé(s):")

    for history in histories:
        print(f"   {history}")

    entries = []

    for history_root in histories:

        for folder in history_root.iterdir():

            if not folder.is_dir():
                continue

            metadata_file = folder / "entries.json"

            if not metadata_file.exists():
                continue

            try:
                data = json.loads(
                    metadata_file.read_text(
                        encoding="utf-8"
                    )
                )
            except Exception:
                continue

            resource = data.get("resource")

            if not resource:
                continue

            original_file = file_uri_to_path(resource)

            if not original_file:
                continue

            original_file = original_file.resolve()

            if not is_interesting_file(original_file):
                continue

            for entry in data.get("entries", []):

                entry_id = entry.get("id")
                timestamp = entry.get("timestamp")

                if not entry_id or not timestamp:
                    continue

                history_file = folder / entry_id

                if not history_file.exists():
                    continue

                entries.append(
                    HistoryEntry(
                        file_path=original_file,
                        history_file=history_file,
                        timestamp=int(timestamp),
                        entry_id=entry_id,
                    )
                )

    # Chronologie globale.
    entries.sort(key=lambda e: e.timestamp)

    return entries


# ============================================================
# CONTENU DES SNAPSHOTS
# ============================================================

def read_snapshot(entry):
    try:
        return entry.history_file.read_text(
            encoding="utf-8",
            errors="replace",
        )
    except Exception:
        return None


def snapshot_hash(content):
    import hashlib

    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


# ============================================================
# ANALYSE DES MODIFICATIONS
# ============================================================

def analyze_python_change(old, new):
    """
    Génère une description simple de la modification.
    """

    if old is None:
        return "feat: add initial Python implementation"

    old_lines = old.splitlines()
    new_lines = new.splitlines()

    if old == new:
        return None

    added = max(0, len(new_lines) - len(old_lines))
    removed = max(0, len(old_lines) - len(new_lines))

    old_lower = old.lower()
    new_lower = new.lower()

    # Ajout de fonctions/classes.
    old_defs = (
        old.count("def ")
        + old.count("class ")
    )

    new_defs = (
        new.count("def ")
        + new.count("class ")
    )

    if new_defs > old_defs:
        if "class " in new_lower and "class " not in old_lower:
            return "feat: add class implementation"

        return "feat: add function"

    if new_defs < old_defs:
        return "refactor: simplify Python implementation"

    # Imports.
    if old_lower.count("import ") != new_lower.count("import "):
        return "refactor: update Python imports"

    # Input / output.
    if "input(" in new_lower and "input(" not in old_lower:
        return "feat: add user input handling"

    if "print(" in new_lower and "print(" not in old_lower:
        return "feat: add program output"

    # Conditions.
    if (
        ("if " in new_lower or "elif " in new_lower)
        and ("if " not in old_lower and "elif " not in old_lower)
    ):
        return "feat: add conditional logic"

    # Boucles.
    if (
        ("for " in new_lower or "while " in new_lower)
        and ("for " not in old_lower and "while " not in old_lower)
    ):
        return "feat: add loop logic"

    # Exceptions.
    if "try:" in new_lower and "try:" not in old_lower:
        return "feat: add error handling"

    # Commentaires / documentation.
    if new.count("#") > old.count("#"):
        return "docs: improve code comments"

    # Suppression importante.
    if removed > added * 2:
        return "refactor: remove obsolete code"

    # Petite correction probable.
    if added <= 5 and removed <= 5:
        return "fix: refine Python implementation"

    return "refactor: update Python implementation"


# ============================================================
# TEMPORAIRE POUR CONSTRUIRE UN ÉTAT
# ============================================================

def create_temp_snapshot(entries):
    """
    Construit un dossier temporaire représentant l'état historique.
    """

    temp = Path(
        tempfile.mkdtemp(
            prefix="vscode_git_history_"
        )
    )

    for entry in entries:

        content = read_snapshot(entry)

        if content is None:
            continue

        relative = entry.file_path.relative_to(
            PROJECT_ROOT
        )

        destination = temp / relative

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination.write_text(
            content,
            encoding="utf-8",
        )

    return temp


# ============================================================
# CONSTRUIRE LES ÉTATS CHRONOLOGIQUES
# ============================================================

def build_states(entries):
    """
    Regroupe les sauvegardes par timestamp.

    À chaque timestamp, on prend le dernier snapshot connu
    pour chaque fichier.
    """

    states = []

    current = {}

    last_timestamp = None

    for entry in entries:

        if entry.timestamp == last_timestamp:
            current[entry.file_path] = entry
            continue

        if current:
            states.append(
                (
                    last_timestamp,
                    current.copy()
                )
            )

        current = {
            entry.file_path: entry
        }

        last_timestamp = entry.timestamp

    if current:
        states.append(
            (
                last_timestamp,
                current.copy()
            )
        )

    return states


# ============================================================
# COMMITS
# ============================================================

def commit_state(timestamp, snapshot_dir, message):
    """
    Remplace temporairement les fichiers du projet par un état
    historique, commit, puis permet de passer au suivant.
    """

    backup_dir = Path(
        tempfile.mkdtemp(
            prefix="git_current_backup_"
        )
    )

    # Sauvegarde de l'état actuel.
    for path in PROJECT_ROOT.rglob("*"):

        if not path.is_file():
            continue

        if ".git" in path.parts:
            continue

        relative = path.relative_to(PROJECT_ROOT)

        destination = backup_dir / relative
        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:
            destination.write_bytes(
                path.read_bytes()
            )
        except Exception:
            pass

    # Supprime les fichiers suivis/non suivis du projet,
    # sauf le dossier .git.
    for path in list(PROJECT_ROOT.rglob("*")):

        if ".git" in path.parts:
            continue

        if path.is_file():
            try:
                path.unlink()
            except Exception:
                pass

    # Copie l'état historique.
    for path in snapshot_dir.rglob("*"):

        if not path.is_file():
            continue

        relative = path.relative_to(snapshot_dir)

        destination = PROJECT_ROOT / relative

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination.write_bytes(
            path.read_bytes()
        )

    run_git("add", "-A")

    # Vérifie s'il y a réellement quelque chose à committer.
    status = run_git(
        "status",
        "--porcelain",
    )

    if status:
        if DRY_RUN:
            print(
                f"[DRY RUN] {message}"
            )
        else:
            run_git(
                "commit",
                "-m",
                message,
                "--date",
                datetime.fromtimestamp(
                    timestamp / 1000
                ).isoformat(),
            )

    # Restaure l'état actuel original.
    for path in list(PROJECT_ROOT.rglob("*")):

        if ".git" in path.parts:
            continue

        if path.is_file():
            try:
                path.unlink()
            except Exception:
                pass

    for path in backup_dir.rglob("*"):

        if not path.is_file():
            continue

        relative = path.relative_to(backup_dir)

        destination = PROJECT_ROOT / relative

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination.write_bytes(
            path.read_bytes()
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("  VS CODE LOCAL HISTORY → GIT")
    print("=" * 60)

    print()
    print(f"📂 Projet : {PROJECT_ROOT}")

    if not git_exists():
        print("❌ Git n'est pas installé ou introuvable.")
        sys.exit(1)

    # Sécurité.
    if (PROJECT_ROOT / ".git").exists():
        print()
        print("⚠️ Un dépôt Git existe déjà ici.")
        print("Le script refuse de reconstruire l'historique")
        print("pour éviter d'écraser tes commits.")
        sys.exit(1)

    print()
    print("🔎 Scan du Local History de VS Code...")

    entries = scan_history()

    if not entries:
        print()
        print("❌ Aucun historique VS Code correspondant")
        print("   à ce dossier n'a été trouvé.")
        sys.exit(1)

    print()
    print(f"📌 {len(entries)} sauvegardes trouvées.")

    files = sorted(
        set(e.file_path for e in entries)
    )

    print()
    print("📄 Fichiers détectés:")

    for file in files:
        print(
            "   ",
            file.relative_to(PROJECT_ROOT)
        )

    states = build_states(entries)

    print()
    print(f"🕒 {len(states)} états historiques détectés.")

    print()
    print("⚠️ IMPORTANT")
    print("Le script va créer un nouveau dépôt Git et")
    print("reconstruire les commits à partir du Local History.")
    print()
    print("Ton état actuel sera sauvegardé puis restauré")
    print("à la fin.")
    print()

    confirmation = input(
        "Tape RECONSTRUIRE pour continuer : "
    )

    if confirmation != "RECONSTRUIRE":
        print("Annulé.")
        return

    # Initialisation Git.
    print()
    print("🔧 Initialisation de Git...")

    run_git("init")

    # Configuration initiale.
    print()
    print("📦 Construction de l'historique...")

    previous_contents = {}

    for index, (timestamp, state) in enumerate(states, 1):

        print(
            f"\n[{index}/{len(states)}] "
            f"{datetime.fromtimestamp(timestamp / 1000)}"
        )

        temp = create_temp_snapshot(
            list(state.values())
        )

        # Détermine les changements.
        messages = []

        for file_path, entry in state.items():

            new_content = read_snapshot(entry)

            if new_content is None:
                continue

            old_content = previous_contents.get(
                file_path
            )

            message = analyze_python_change(
                old_content,
                new_content,
            )

            if message:
                messages.append(
                    f"{message} "
                    f"({file_path.name})"
                )

            previous_contents[file_path] = new_content

        if messages:
            message = messages[0]

            if len(messages) > 1:
                message = (
                    f"{message} "
                    f"+ {len(messages) - 1} other change(s)"
                )

            commit_state(
                timestamp,
                temp,
                message,
            )

            print(f"   ✓ {message}")

    print()
    print("=" * 60)
    print("✅ Reconstruction terminée.")
    print("=" * 60)

    print()
    print("Historique Git créé :")

    print(
        run_git(
            "log",
            "--oneline",
            "--reverse",
        )
    )

    print()
    print("Ton état actuel a été restauré.")
    print()
    print("Tu peux maintenant utiliser :")
    print()
    print("    git log --oneline")
    print("    git status")
    print("    git diff")
    print()


if __name__ == "__main__":
    main()
