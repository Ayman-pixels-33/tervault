from database import add_command as db_add
from gemini_api import search_command as gemini_search
from database import delete_command as db_delete
from backup import list_backups, import_backup as db_import
from backup import export_backup
from database import get_all_commands

def add(command, description):
    return db_add(command, description)

def search(query):
    all_commands = get_all_commands()
    return gemini_search(query, all_commands)

def delete(command_id):
    return db_delete(command_id)

def list_all():
    return get_all_commands()

def export():
    """تستدعي التصدير الجديد وتمرر حالته"""
    return export_backup()

def import_backup():
    backups = list_backups()
    if not backups:
        print("No backups available")
        return
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup}")

    choice = input("Choose backup: ")
    try:
        backup_name = backups[int(choice) - 1]
        print("1. Add to current")
        print("2. Replace current")
        merge_choice = input("Choose: ")

        merge = (merge_choice == "1")
        db_import(backup_name, merge=merge)
    except Exception as e:
        print(f"✗ Error: {e}")