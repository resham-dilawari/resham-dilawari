# 🚀 Deployment Guide - Ensuring Data Persistence

## 📋 Overview

This guide ensures your RAG database never gets lost during deployment or updates.

---

## 💾 Data Persistence Strategy

### What Needs to Persist:
1. **ChromaDB** (`./chroma_db/`) - Vector embeddings and documents
2. **Simple RAG DB** (`./simple_rag_db/`) - JSON knowledge base
3. **User analyses** - Automatically stored by RAG agent

### What Doesn't Persist (and shouldn't):
- `.env` file (contains secrets)
- `__pycache__/` (Python cache)
- `venv/` (virtual environment)

---

## 🔧 Local Development (Your PC)

### Current Setup:
✅ Data stored in: `C:\AI Portfolio Advisor\chroma_db\`  
✅ Persists across app restarts  
✅ Protected by `.gitignore`

### Backup Before Major Changes:
```bash
# Create backup
python scripts\backup_rag.py backup

# List all backups
python scripts\backup_rag.py list

# Restore if needed
python scripts\backup_rag.py restore rag_backup_20261212_120000
```

### Automatic Backup:
```bash
# Creates backup only if no backup in last 7 days
python scripts\backup_rag.py auto
```

---

## ☁️ Cloud Deployment Options

### Option 1: Render (Recommended for MVP)

**Persistent Disk Setup:**

1. Create a Render account at https://render.com

2. Create `render.yaml` in project root:
```yaml
services:
  - type: web
    name: ai-portfolio-advisor
    env: python
    region: oregon
    plan: starter  # $7/month includes 512MB RAM
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app_unified.py --server.headless=true --server.port=$PORT --server.address=0.0.0.0
    
    # PERSISTENT DISK - THIS IS CRITICAL!
    disk:
      name: rag-database
      mountPath: /opt/render/project/src/chroma_db
      sizeGB: 1  # 1GB is enough for MVP
    
    envVars:
      - key: GEMINI_API_KEY
        sync: false  # You'll add this in Render dashboard
      - key: PYTHON_VERSION
        value: 3.11.0
```

3. Deploy:
   - Push code to GitHub
   - Connect Render to your repo
   - Add `GEMINI_API_KEY` in Render dashboard
   - Deploy!

**Result:** Database persists across deployments! ✅

---

### Option 2: Railway

**Persistent Volume Setup:**

1. Create `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run app_unified.py --server.headless=true --server.port=$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

2. In Railway Dashboard:
   - Create a new service from GitHub
   - Go to "Volumes" tab
   - Add volume: `/app/chroma_db` → This persists your data!
   - Add environment variable: `GEMINI_API_KEY`

**Result:** Database persists! ✅

---

### Option 3: Fly.io

**Persistent Storage:**

1. Create `fly.toml`:
```toml
app = "ai-portfolio-advisor"
primary_region = "sjc"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8501"

[[services]]
  internal_port = 8501
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

# PERSISTENT VOLUME - CRITICAL!
[[mounts]]
  source = "rag_database"
  destination = "/app/chroma_db"
```

2. Deploy:
```bash
fly launch
fly volumes create rag_database --size 1  # 1GB volume
fly secrets set GEMINI_API_KEY=your_key_here
fly deploy
```

**Result:** Database persists! ✅

---

### Option 4: AWS EC2 / DigitalOcean Droplet (Full Control)

**EBS Volume / Block Storage:**

1. Create instance with attached storage
2. Mount volume to `/data/chroma_db`
3. Update code to use mounted path:

```python
# In agents/rag_agent.py
persist_dir = os.environ.get('RAG_DB_PATH', './chroma_db')
self.rag_system = RAGSystem(persist_directory=persist_dir)
```

4. Set environment variable:
```bash
export RAG_DB_PATH=/data/chroma_db
```

**Backup Strategy:**
- Automated EBS snapshots daily
- Or use the backup script: `python scripts/backup_rag.py auto`

**Result:** Full control, persistent storage! ✅

---

## 📦 Backup Strategy (All Deployments)

### Automated Backups:

**Option A: Scheduled Backups (Recommended)**

Add to your deployment platform:

**Render:**
```yaml
# Add to render.yaml
cronjobs:
  - name: daily-rag-backup
    schedule: "0 2 * * *"  # 2 AM daily
    command: python scripts/backup_rag.py auto
```

**Cron (Linux servers):**
```bash
# Edit crontab
crontab -e

# Add this line
0 2 * * * cd /path/to/project && python scripts/backup_rag.py auto
```

**Option B: Manual Backups**

Before major updates:
```bash
python scripts/backup_rag.py backup pre_deployment_$(date +%Y%m%d)
```

---

## 🔄 Migration Between Environments

### From Local to Cloud:

1. **Create backup locally:**
```bash
python scripts\backup_rag.py backup production_migration
```

2. **Transfer backup to cloud:**
```bash
# Upload to cloud server
scp backups/production_migration.zip user@your-server:/app/backups/

# Or commit to private repo (if data not sensitive)
git add backups/production_migration.zip
git commit -m "Production database migration"
git push
```

3. **Restore on cloud:**
```bash
# SSH into server
ssh user@your-server
cd /app
python scripts/backup_rag.py restore production_migration
```

### From Cloud to Local:

1. **Download backup from cloud**
2. **Restore locally:**
```bash
python scripts\backup_rag.py restore downloaded_backup
```

---

## 🛡️ Data Safety Checklist

### Before Deployment:
- [ ] Create backup: `python scripts/backup_rag.py backup`
- [ ] Verify `.gitignore` excludes `chroma_db/`
- [ ] Configure persistent volume in deployment platform
- [ ] Test restore process locally

### After Deployment:
- [ ] Verify database directory exists on server
- [ ] Run one analysis to populate database
- [ ] Create backup from production
- [ ] Set up automated backups

### Regular Maintenance:
- [ ] Weekly backup review
- [ ] Monthly cleanup of old backups (keep last 3-6 months)
- [ ] Test restore process quarterly

---

## 🚨 Disaster Recovery

### If Data is Lost:

1. **Stop the application immediately**

2. **Restore from most recent backup:**
```bash
python scripts/backup_rag.py list
python scripts/backup_rag.py restore <most_recent_backup>
```

3. **Verify restoration:**
```bash
# Check if databases exist
ls -la chroma_db/
ls -la simple_rag_db/
```

4. **Restart application**

5. **Create new backup:**
```bash
python scripts/backup_rag.py backup post_recovery_$(date +%Y%m%d)
```

---

## 📊 Storage Requirements

### Initial Setup:
- **Simple RAG DB:** ~50 KB
- **ChromaDB (empty):** ~10 MB
- **Embedding Model:** ~90 MB (cached in user directory)

### After 100 Analyses:
- ~50-100 MB

### After 1,000 Analyses:
- ~200-500 MB

### After 10,000 Analyses:
- ~1-2 GB

**Recommendation:** Start with 1 GB persistent volume, scale as needed.

---

## ✅ Quick Reference

### Backup Commands:
```bash
# Create backup
python scripts/backup_rag.py backup

# List backups
python scripts/backup_rag.py list

# Restore backup
python scripts/backup_rag.py restore <name>

# Auto backup (if needed)
python scripts/backup_rag.py auto
```

### Backup Location:
- Local: `C:\AI Portfolio Advisor\backups\`
- Cloud: `/app/backups/` (or your project path)

### Files that Persist:
- `chroma_db/` - Vector database ✅
- `simple_rag_db/` - JSON database ✅
- `backups/` - Backup archives ✅

### Files that Don't (and shouldn't):
- `.env` - Secrets (use platform env vars)
- `__pycache__/` - Python cache
- `venv/` - Virtual environment

---

## 🎯 Recommended Setup

**For Portfolio/Demo:**
- Use Render with 1GB persistent disk ($7/month)
- Weekly manual backups
- Keep last 4 backups

**For Production:**
- Use AWS/GCP with auto-scaling storage
- Daily automated backups
- 30-day retention policy
- Cross-region backup replication

---

## 💡 Pro Tips

1. **Always backup before:**
   - Major code changes
   - Deployment updates
   - Database migrations

2. **Test restore process:**
   - Do it at least once before you need it
   - Verify data integrity after restore

3. **Monitor storage:**
   - Set up alerts when >80% full
   - Clean up old data periodically

4. **Version your backups:**
   - Include date in backup name
   - Keep metadata about what changed

---

## 🆘 Support

If data persistence issues occur:
1. Check deployment logs
2. Verify persistent volume is mounted
3. Check disk space: `df -h`
4. Restore from backup
5. Create GitHub issue with logs

---

**Your data is now protected! 🛡️**
