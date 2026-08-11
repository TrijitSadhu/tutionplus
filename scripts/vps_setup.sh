#!/bin/bash
# ─── First-time VPS setup script ─────────────────────────────────────────────
# Run this ONCE on a fresh Interserver VPS (Ubuntu 22.04)
# Usage: bash vps_setup.sh

set -e

echo "==> Updating system..."
apt-get update && apt-get upgrade -y

echo "==> Installing Docker..."
curl -fsSL https://get.docker.com | sh
usermod -aG docker $USER

echo "==> Installing Docker Compose plugin..."
apt-get install -y docker-compose-plugin

echo "==> Creating app directories..."
mkdir -p /home/tutionplus/app
mkdir -p /home/tutionplus/db_backups
mkdir -p /home/tutionplus/scripts

echo "==> Cloning repo..."
# Replace with your actual GitHub repo URL
git clone https://github.com/YOUR_USERNAME/tutionplus.git /home/tutionplus/app

echo "==> Setting up .env..."
cp /home/tutionplus/app/.env.example /home/tutionplus/app/.env
echo ""
echo ">>> EDIT /home/tutionplus/app/.env with your production values! <<<"
echo ""

echo "==> Copying scripts..."
cp /home/tutionplus/app/scripts/backup_db.sh /home/tutionplus/scripts/
cp /home/tutionplus/app/scripts/restore_db.sh /home/tutionplus/scripts/
chmod +x /home/tutionplus/scripts/*.sh

echo "==> Setting up daily backup cron (2am every night)..."
(crontab -l 2>/dev/null; echo "0 2 * * * /home/tutionplus/scripts/backup_db.sh >> /home/tutionplus/db_backups/backup.log 2>&1") | crontab -

echo "==> Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit /home/tutionplus/app/.env with production secrets"
echo "  2. cd /home/tutionplus/app"
echo "  3. docker compose -f docker-compose.prod.yml up --build -d"
