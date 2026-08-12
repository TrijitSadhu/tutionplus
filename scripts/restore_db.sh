#!/bin/bash
# ─── Restore PostgreSQL from backup ──────────────────────────────────────────
# Runs natively on the VPS host against the native PostgreSQL install.
# Usage: ./restore_db.sh /home/tutionplus/db_backups/tutionplus_2026-08-11_02-00.dump
# WARNING: This will WIPE the current database and restore from the backup file.

set -e

ENV_FILE="/home/tutionplus/app/.env"
if [ -f "$ENV_FILE" ]; then
  set -a
  source "$ENV_FILE"
  set +a
fi

BACKUP_FILE="$1"
DB_NAME="${DB_NAME:-tutionplus}"
DB_USER="${DB_USER:-postgres}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"

if [ -z "$BACKUP_FILE" ]; then
  echo "Usage: $0 <path_to_backup.dump>"
  echo ""
  echo "Available backups:"
  ls -lh /home/tutionplus/db_backups/*.dump 2>/dev/null || echo "  (none found)"
  exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
  echo "ERROR: File not found: $BACKUP_FILE"
  exit 1
fi

echo "WARNING: This will REPLACE the current database with: $BACKUP_FILE"
read -p "Are you sure? (yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
  echo "Aborted."
  exit 0
fi

echo "[$(date)] Restoring database..."
PGPASSWORD="$DB_PASSWORD" pg_restore \
  -h "$DB_HOST" \
  -p "$DB_PORT" \
  -U "$DB_USER" \
  -d "$DB_NAME" \
  --clean --if-exists \
  -F c \
  "$BACKUP_FILE"

echo "[$(date)] Restore complete from: $BACKUP_FILE"
