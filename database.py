import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".tervault" / "commands.db"

def init_db():
    """Create table if not exists"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS commands (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        command TEXT NOT NULL UNIQUE,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def add_command(command, description):
    """Add command to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO commands (command, description) VALUES (?, ?)",
            (command, description)
        )
        conn.commit()
        print(f"✓ Added: {command}")
        return True
    except sqlite3.IntegrityError:
        print(f"✗ Command already exists")
        return False
    finally:
        conn.close()

def delete_command(command_id):
    """حذف أمر من database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM commands WHERE id = ?", (command_id,))
        conn.commit()
        print(f"✓ Deleted: {command_id}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    finally:
        conn.close()

def get_all_commands():
    """Get all commands from database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, command, description FROM commands")
    commands = cursor.fetchall()
    conn.close()

    return commands

#if __name__ == "__main__":
#   init_db()
#   print("Database ready!")
