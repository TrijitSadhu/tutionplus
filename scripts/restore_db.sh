#!/bin/bash
# ─── Restore PostgreSQL from backup ──────────────────────────────────────────
# Usage: ./restore_db.sh /home/tutionplus/db_backups/tutionplus_2026-08-11_02-00.dump
# WARNING: This will WIPE the current database and restore from the backup file.

set -e

BACKUP_FILE="$1"
DB_NAME="${DB_NAME:-tutionplus}"
DB_USER="${DB_USER:-postgres}"

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

echo "[$(date)] Copying backup into container..."
docker cp "$BACKUP_FILE" tutionplus-db-1:/tmp/restore.dump

echo "[$(date)] Restoring database..."
docker exec tutionplus-db-1 pg_restore \
  -U "$DB_USER" \
  -d "$DB_NAME" \
  --clean --if-exists \
  -F c \
  /tmp/restore.dump

docker exec tutionplus-db-1 rm -f /tmp/restore.dump

echo "[$(date)] Restore complete from: $BACKUP_FILE"
