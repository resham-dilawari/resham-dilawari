"""
RAG Database Backup and Restore Utility
Ensures your RAG knowledge base is never lost
"""
import os
import shutil
import json
from datetime import datetime
import zipfile

class RAGBackupManager:
    """Manage backups of RAG database."""
    
    def __init__(self):
        self.backup_dir = "./backups"
        self.db_dirs = ["chroma_db", "simple_rag_db"]
        
        # Create backup directory if it doesn't exist
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self, backup_name=None):
        """Create a backup of all RAG databases."""
        if backup_name is None:
            backup_name = f"rag_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_path = os.path.join(self.backup_dir, f"{backup_name}.zip")
        
        print(f"🔄 Creating backup: {backup_name}")
        print("=" * 60)
        
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            total_files = 0
            
            for db_dir in self.db_dirs:
                if os.path.exists(db_dir):
                    print(f"📦 Backing up {db_dir}...")
                    
                    # Walk through directory and add all files
                    for root, dirs, files in os.walk(db_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, ".")
                            zipf.write(file_path, arcname)
                            total_files += 1
                else:
                    print(f"⚠️  {db_dir} not found, skipping...")
            
            # Add metadata
            metadata = {
                "backup_name": backup_name,
                "created": datetime.now().isoformat(),
                "databases": [db for db in self.db_dirs if os.path.exists(db)],
                "total_files": total_files,
                "version": "1.0"
            }
            
            zipf.writestr("backup_metadata.json", json.dumps(metadata, indent=2))
        
        backup_size = os.path.getsize(backup_path) / (1024 * 1024)  # MB
        
        print(f"✅ Backup created successfully!")
        print(f"📍 Location: {os.path.abspath(backup_path)}")
        print(f"📊 Total files: {total_files}")
        print(f"💾 Size: {backup_size:.2f} MB")
        print("=" * 60)
        
        return backup_path
    
    def restore_backup(self, backup_name):
        """Restore from a backup."""
        backup_path = os.path.join(self.backup_dir, f"{backup_name}.zip")
        
        if not os.path.exists(backup_path):
            # Try with extension if not provided
            if not backup_name.endswith('.zip'):
                backup_path = os.path.join(self.backup_dir, f"{backup_name}.zip")
            
            if not os.path.exists(backup_path):
                print(f"❌ Backup not found: {backup_path}")
                return False
        
        print(f"🔄 Restoring from backup: {backup_name}")
        print("=" * 60)
        
        # Read metadata
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            if 'backup_metadata.json' in zipf.namelist():
                metadata_content = zipf.read('backup_metadata.json')
                metadata = json.loads(metadata_content)
                print(f"📅 Backup Date: {metadata['created']}")
                print(f"📊 Databases: {', '.join(metadata['databases'])}")
                print(f"📁 Total Files: {metadata['total_files']}")
            
            # Extract all files
            print(f"\n📦 Extracting files...")
            zipf.extractall(".")
            
        print(f"✅ Restore completed successfully!")
        print(f"📍 Databases restored to current directory")
        print("=" * 60)
        
        return True
    
    def list_backups(self):
        """List all available backups."""
        if not os.path.exists(self.backup_dir):
            print("📂 No backups directory found")
            return []
        
        backups = [f for f in os.listdir(self.backup_dir) if f.endswith('.zip')]
        
        if not backups:
            print("📂 No backups found")
            return []
        
        print("=" * 60)
        print("📦 AVAILABLE BACKUPS")
        print("=" * 60)
        
        backup_info = []
        
        for backup_file in sorted(backups, reverse=True):
            backup_path = os.path.join(self.backup_dir, backup_file)
            backup_size = os.path.getsize(backup_path) / (1024 * 1024)
            backup_date = datetime.fromtimestamp(os.path.getmtime(backup_path))
            
            # Try to read metadata
            try:
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    if 'backup_metadata.json' in zipf.namelist():
                        metadata_content = zipf.read('backup_metadata.json')
                        metadata = json.loads(metadata_content)
                        databases = metadata.get('databases', [])
                    else:
                        databases = ['Unknown']
            except:
                databases = ['Unknown']
            
            print(f"\n📦 {backup_file}")
            print(f"   Date: {backup_date.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Size: {backup_size:.2f} MB")
            print(f"   DBs:  {', '.join(databases)}")
            
            backup_info.append({
                'name': backup_file.replace('.zip', ''),
                'path': backup_path,
                'size_mb': backup_size,
                'date': backup_date,
                'databases': databases
            })
        
        print("=" * 60)
        return backup_info
    
    def auto_backup_if_needed(self):
        """Create automatic backup if databases exist and no recent backup."""
        # Check if any database exists
        has_data = any(os.path.exists(db) and os.listdir(db) for db in self.db_dirs if os.path.exists(db))
        
        if not has_data:
            print("ℹ️  No database data to backup yet")
            return None
        
        # Check for recent backups (within last 7 days)
        recent_backups = []
        if os.path.exists(self.backup_dir):
            for backup_file in os.listdir(self.backup_dir):
                if backup_file.endswith('.zip'):
                    backup_path = os.path.join(self.backup_dir, backup_file)
                    backup_date = datetime.fromtimestamp(os.path.getmtime(backup_path))
                    age_days = (datetime.now() - backup_date).days
                    if age_days < 7:
                        recent_backups.append(backup_file)
        
        if recent_backups:
            print(f"✅ Recent backup exists: {recent_backups[0]}")
            return None
        
        print("📅 No recent backup found, creating automatic backup...")
        return self.create_backup(f"auto_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")


def main():
    """Main CLI interface."""
    import sys
    
    manager = RAGBackupManager()
    
    if len(sys.argv) < 2:
        print("""
╔═══════════════════════════════════════════════════════════╗
║           RAG DATABASE BACKUP & RESTORE UTILITY           ║
╚═══════════════════════════════════════════════════════════╝

USAGE:
    python scripts/backup_rag.py <command> [options]

COMMANDS:
    backup [name]         Create a new backup
                         Optional: Specify custom backup name
    
    restore <name>       Restore from a backup
                         Required: Backup name (without .zip)
    
    list                 List all available backups
    
    auto                 Auto-backup if needed (no backup in last 7 days)

EXAMPLES:
    python scripts/backup_rag.py backup
    python scripts/backup_rag.py backup my_custom_backup
    python scripts/backup_rag.py restore rag_backup_20261212_120000
    python scripts/backup_rag.py list
    python scripts/backup_rag.py auto

BACKUP LOCATION:
    ./backups/

NOTE: Database directories are in .gitignore and won't be committed.
      Always backup before major changes!
""")
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    if command == "backup":
        backup_name = sys.argv[2] if len(sys.argv) > 2 else None
        manager.create_backup(backup_name)
    
    elif command == "restore":
        if len(sys.argv) < 3:
            print("❌ Error: Backup name required")
            print("Usage: python scripts/backup_rag.py restore <backup_name>")
            manager.list_backups()
            sys.exit(1)
        
        backup_name = sys.argv[2]
        manager.restore_backup(backup_name)
    
    elif command == "list":
        manager.list_backups()
    
    elif command == "auto":
        result = manager.auto_backup_if_needed()
        if result is None:
            print("✅ No backup needed at this time")
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run without arguments to see usage")
        sys.exit(1)


if __name__ == "__main__":
    main()
