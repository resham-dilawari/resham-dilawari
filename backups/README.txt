RAG DATABASE BACKUPS
====================

This folder contains backups of your RAG knowledge base.

IMPORTANT:
- These backups are NOT in version control (.gitignore)
- Always backup before major changes
- Keep at least 2-3 recent backups
- Test restore process periodically

QUICK COMMANDS:
---------------
# Create backup
python scripts\backup_rag.py backup

# List all backups  
python scripts\backup_rag.py list

# Restore from backup
python scripts\backup_rag.py restore <backup_name>

BACKUP CONTENTS:
----------------
- chroma_db/ (Vector database with embeddings)
- simple_rag_db/ (JSON knowledge base)
- backup_metadata.json (Backup info)

RETENTION POLICY:
-----------------
Recommended: Keep last 3-6 months of backups
Delete old backups manually or set up automated cleanup

For more info, see: DEPLOYMENT_GUIDE.md
