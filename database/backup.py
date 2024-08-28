import shutil
import os
import datetime

def backup_database(db_path, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = os.path.join(backup_dir, f"backup_{timestamp}.db")

    shutil.copyfile(db_path, backup_path)
    print(f"Database backed up to {backup_path}")
    return backup_path

def restore_database(backup_path, db_path):
    if os.path.exists(backup_path):
        shutil.copyfile(backup_path, db_path)
        print(f"Database restored from {backup_path}")
    else:
        print(f"Backup file {backup_path} not found.")
