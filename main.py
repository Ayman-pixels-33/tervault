from commands import add, search, list_all, delete, export, import_backup
from config import get_api_key, save_api_key
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.table import Table
from database import init_db
import os

def main():
    init_db()
    if not get_api_key():
        api_key = input("Enter Gemini API key: ")
        save_api_key(api_key)

    while True:
        os.system("clear")
        console = Console()

        menu_text = """[cyan]1. Add command
2. Search
3. List all
4. Delete
5. Export/backup
6. Exit[/cyan]"""

        panel = Panel(menu_text, title="Menu", border_style="white")
        console.print(Align.center(panel))
        choice = input("\nChoose: ").strip()

        if choice == "1":
            os.system("clear")
            console.print("[bold cyan]Add Command[/bold cyan]")
            cmd = input("Command: ").strip()
            desc = input("Description: ").strip()

            if cmd and desc:
                result = add(cmd, desc)
                if result:
                    console.print("[green]✓ Added[/green]")
                else:
                    console.print("[red]✗ Already exists[/red]")
            else:
                console.print("[red]✗ Missing fields[/red]")
            input("Press Enter to continue...")

        elif choice == "2":
            os.system("clear")
            console.print("[bold cyan]Search[/bold cyan]")
            query = input("Search: ").strip()

            if query:
                result = search(query)
                console.print(f"[green]Result: {result}[/green]")
            else:
                console.print("[red]✗ Empty query[/red]")
            input("Press Enter to continue...")

        elif choice == "3":
            os.system("clear")
            console.print("[bold cyan]All Commands[/bold cyan]")
            cmds = list_all()

            if cmds:
                table = Table(title="Commands")
                table.add_column("ID", style="yellow")
                table.add_column("Command", style="cyan")
                table.add_column("Description", style="green")

                for cmd in cmds:
                    table.add_row(str(cmd[0]), cmd[1], cmd[2])
                console.print(table)
            else:
                console.print("[yellow]No commands found[/yellow]")
            input("Press Enter to continue...")

        elif choice == "4":
            os.system("clear")
            console.print("[bold cyan]Delete Command[/bold cyan]")
            cmds = list_all()

            if cmds:
                table = Table(title="Select ID to Delete")
                table.add_column("ID", style="yellow")
                table.add_column("Command", style="cyan")

                for cmd in cmds:
                    table.add_row(str(cmd[0]), cmd[1])
                console.print(table)
                cmd_id = input("Enter ID to delete: ").strip()

                if not cmd_id or not cmd_id.isdigit():
                    console.print("[red]✗ Invalid ID. Please enter a valid number.[/red]")
                else:
                    result = delete(cmd_id)
                    if result:
                        console.print("[green]✓ Deleted successfully[/green]")
                    else:
                        console.print("[red]✗ Failed to delete (ID might not exist)[/red]")
            else:
                console.print("[yellow]No commands found to delete[/yellow]")
            input("Press Enter to continue...")

        elif choice == "5":
            os.system("clear")
            console.print("[bold cyan]Backup[/bold cyan]")
            backup_text = """[cyan]1. Export
2. Import
3. Back[/cyan]"""

            panel = Panel(backup_text, title="Backup Menu", border_style="white")
            console.print(Align.center(panel))
            sub_choice = input("\nChoose: ").strip()

            if sub_choice == "1":
                export()  # الدالة تتولى الطباعة الصحيحة داخلياً الآن بناءً على النتيجة الحقيقية
            elif sub_choice == "2":
                import_backup()
            input("Press Enter to continue...")

        elif choice == "6":
            console.print("[bold cyan]Goodbye![/bold cyan]")
            break
        else:
            console.print("[red]✗ Invalid choice[/red]")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")