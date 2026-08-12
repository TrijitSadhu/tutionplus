#!/bin/bash
# ─── Automated PostgreSQL backup ─────────────────────────────────────────────
# Runs natively on the VPS host against the native PostgreSQL install.
# Cron: 0 2 * * * /home/tutionplus/app/scripts/backup_db.sh
# Keeps last 7 daily backups, then one per week for 4 weeks

set -e

ENV_FILE="/home/tutionplus/app/.env"
if [ -f "$ENV_FILE" ]; then
  set -a
  source "$ENV_FILE"
  set +a
fi

BACKUP_DIR="/home/tutionplus/db_backups"
DATE=$(date +%Y-%m-%d_%H-%M)
FILENAME="tutionplus_${DATE}.dump"
KEEP_DAILY=7
KEEP_WEEKLY=4

# DB credentials (from .env, falling back to native defaults)
DB_NAME="${DB_NAME:-tutionplus}"
DB_USER="${DB_USER:-postgres}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"

mkdir -p "$BACKUP_DIR"

echo "[$(date)] Starting backup: $FILENAME"

# Dump from native PostgreSQL
PGPASSWORD="$DB_PASSWORD" pg_dump \
  -h "$DB_HOST" \
  -p "$DB_PORT" \
  -U "$DB_USER" \
  -d "$DB_NAME" \
  -F c \
  -f "${BACKUP_DIR}/${FILENAME}"

echo "[$(date)] Backup saved: ${BACKUP_DIR}/${FILENAME}"

# ─── Cleanup old backups ──────────────────────────────────────────────────────
# Keep last N daily backups
ls -t "$BACKUP_DIR"/*.dump 2>/dev/null | tail -n +$((KEEP_DAILY + 1)) | xargs rm -f 2>/dev/null || true

echo "[$(date)] Cleanup done. Current backups:"
ls -lh "$BACKUP_DIR"/*.dump 2>/dev/null || echo "  (none)"
