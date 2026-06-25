# Tervault

#### Description:
Tervault is a high-performance, dark-theme optimized Command-Line Interface (CLI) tool designed for Linux power users and developers to securely store, organize, and intelligently retrieve terminal commands. Developed as a final project for Harvard's CS50x, Tervault eliminates the friction of forgetting complex shell syntax by creating an isolated local vault that integrates with the Google Gemini API (`gemini-2.5-flash`) for AI-driven semantic searching.

Rather than relying on strict keyword matching, Tervault leverages artificial intelligence to understand the developer's underlying intent. Users can query their database using natural language (e.g., "how to update packages in Arch Linux"), and the application will map the semantic meaning against their locally saved command library to surface the exact record instantly.

---

## Visual Design & User Experience (UX)

Tervault features a fully responsive and stylized console interface built on top of the `rich` Python library. Key design elements include:
- **Centered Layout Alignment**: Main menu elements and panels are dynamically aligned and boxed to maintain a clean workspace layout.
- **Color-Coded Feedback Loops**: Immediate semantic color formatting (green for successful database writes, yellow for empty states, and crisp red for input errors or exception catches).
- **Graceful Terminal Clearing**: Utilizing native `os.system("clear")` transitions to maintain a single-page app experience inside the shell.

---

## Technical Features & Architecture

### 1. Isolated State Configuration
The tool strictly decoupling configuration architecture from the runtime repository. All configuration states, including user preferences and encrypted Gemini API credentials, are automatically hosted within a dedicated hidden environment folder in the user's home directory (`~/.tervault/config.json`).

### 2. Dual-Engine Retrieval System
Tervault provides two methods for command lookup:
- **Standard Table Indexing**: Instantly lists every saved command, formatted into a stylized, clean `rich.table.Table` with automatic indexing.
- **AI Semantic Search**: Extracts all local entries, formats them into structured context blocks, and passes them to the Gemini API using highly strict system boundaries (`prompts.py`) to prevent model hallucination and ensure only the raw matched command is returned.

### 3. Advanced Backup & Merger Core
The persistence architecture supports modular backups inside `~/.tervault/backups/`. The backup core provides two distinct recovery strategies:
- **Direct Restore**: Complete replacement of the current file with an older snapshot via `shutil`.
- **Incremental Merging**: Uses advanced SQLite capabilities by executing `ATTACH DATABASE` to bind an external backup session, running a programmatic `INSERT OR REPLACE` loop to combine distinct databases without losing unique primary records.

---

## File Structure & Module Breakdown

- **`main.py`**: The central execution entry point. Houses the main control loop, manages terminal clearing states, and coordinates the primary UI panel views.
- **`commands.py`**: Acts as the intermediate controller layer that handles validation checking and converts user interactions into backend transaction calls.
- **`database.py`**: Manages the local SQLite database creation (`commands.db`), schema instantiations (`CREATE TABLE IF NOT EXISTS`), insertion transactions, and deletions safely inside `~/.tervault/`.
- **`config.py`**: Direct interface for setup file initialization, parsing, and storing API keys using JSON data structures.
- **`gemini_api.py`**: Wrapper built around the official modern `google-genai` SDK. Sets up the client runtime, compiles database entries, and securely processes structured responses from `gemini-2.5-flash`.
- **`prompts.py`**: Houses the strict, isolated system instructions ensuring the AI responds exclusively with raw terminal syntax without verbose commentary.
- **`backup.py`**: Controls the snapshotting pipeline, managing automatic date-string generation, file copies, and advanced SQL database merging routines.
- **`.gitignore`**: Correctly configured to keep untracked build assets and compiled Python bytecode arrays (`__pycache__/`, `*.pyc`) out of the remote repository.

---

## Installation & System Requirements

### Prerequisites
Ensure you have Python 3.10+ installed on your environment.

### Installation Steps

1. Clone this repository locally and navigate to the root directory:
```bash
   git clone [https://github.com/Ayman-pixels-33/tervault.git](https://github.com/Ayman-pixels-33/tervault.git)
   cd tervault

```

2. Set up and activate a Virtual Environment (Recommended for PEP 668 environments):
```bash
python -m venv .venv
source .venv/bin/activate

```


*(Note: If you use the Fish shell, use `source .venv/bin/activate.fish` instead).*
3. Install the necessary libraries from the requirements file:
```bash
pip install -r requirements.txt

```


4. Run the application:
```bash
python main.py

```
