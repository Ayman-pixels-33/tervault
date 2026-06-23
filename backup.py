import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

BACKUP_DIR = Path.home() / ".tervault" / "backups"
DB_PATH = Path("commands.db")  # تحويله إلى Path أيضاً لتوحيد الأسلوب
TABLE_NAME = "commands"

def export_backup():
    if not DB_PATH.exists():
        print(f"✗ Error: Source database '{DB_PATH}' does not exist.")
        return False

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    date_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = f"backup_{date_string}.db"
    backup_path = BACKUP_DIR / backup_name

    try:
        shutil.copy(DB_PATH, backup_path)
        print(f"✓ Backup saved: {backup_name}")
        return True
    except Exception as e:
        print(f"✗ Error during backup: {e}")
        return False


def list_backups():
    if not BACKUP_DIR.exists():
        print("No backups folder")
        return []

    # إرجاع أسماء الملفات مرتبة من الأحدث للأقدم
    backups = sorted(BACKUP_DIR.glob("*.db"), key=lambda x: x.stat().st_mtime, reverse=True)
    return [b.name for b in backups]


def import_backup(backup_name, merge=False):  # جعلت القيمة الافتراضية False للاستبدال المباشر كأمان
    backup_path = BACKUP_DIR / backup_name

    if not backup_path.exists():
        print(f"✗ Backup not found: {backup_name}")
        return False

    try:
        if merge:
            print(f"Merging data from {backup_name} into current database...")

            # الاتصال بقاعدة البيانات الحالية
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # ربط القاعدة الاحتياطية بالجلسة الحالية باسم مستعار (backup_db)
            cursor.execute(f"ATTACH DATABASE '{backup_path}' AS backup_db")

            # دمج البيانات: إدخال السجلات غير الموجودة وتجاهل المتكرر بناءً على الـ Primary Key
            cursor.execute(
                f"INSERT OR REPLACE INTO {TABLE_NAME} SELECT * FROM backup_db.{TABLE_NAME}"
            )

            # حفظ التغييرات وفصل القاعدة الاحتياطية
            conn.commit()
            cursor.execute("DETACH DATABASE backup_db")
            conn.close()

            print(f"✓ Merge completed successfully!")
            return True
        else:
            shutil.copy(backup_path, DB_PATH)
            print(f"✓ Database replaced with {backup_name}")
            return True
    except Exception as e:
        print(f"✗ Error during import: {e}")
        return False


#if __name__ == "__main__":
#    export_backup()
#    print("Available backups:", list_backups())
