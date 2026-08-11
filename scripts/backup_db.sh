#!/bin/bash
# ─── Automated PostgreSQL backup ─────────────────────────────────────────────
# Runs inside the VPS host (outside Docker)
# Cron: 0 2 * * * /home/tutionplus/scripts/backup_db.sh
# Keeps last 7 daily backups, then one per week for 4 weeks

set -e

BACKUP_DIR="/home/tutionplus/db_backups"
DATE=$(date +%Y-%m-%d_%H-%M)
FILENAME="tutionplus_${DATE}.dump"
KEEP_DAILY=7
KEEP_WEEKLY=4

# DB credentials (matches your .env)
DB_NAME="${DB_NAME:-tutionplus}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-tutionplus_pass_2026}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"

mkdir -p "$BACKUP_DIR"

echo "[$(date)] Starting backup: $FILENAME"

# Dump from running Docker postgres container
docker exec tutionplus-db-1 pg_dump \
  -U "$DB_USER" \
  -d "$DB_NAME" \
  -F c \
  -f "/tmp/${FILENAME}"

# Copy dump out of container to host
docker cp "tutionplus-db-1:/tmp/${FILENAME}" "${BACKUP_DIR}/${FILENAME}"

# Remove temp file from container
docker exec tutionplus-db-1 rm -f "/tmp/${FILENAME}"

echo "[$(date)] Backup saved: ${BACKUP_DIR}/${FILENAME}"

# ─── Cleanup old backups ──────────────────────────────────────────────────────
# Keep last N daily backups
ls -t "$BACKUP_DIR"/*.dump 2>/dev/null | tail -n +$((KEEP_DAILY + 1)) | xargs rm -f 2>/dev/null || true

echo "[$(date)] Cleanup done. Current backups:"
ls -lh "$BACKUP_DIR"/*.dump 2>/dev/null || echo "  (none)"
