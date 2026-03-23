#!/bin/bash

LOG_FILE="/var/www/tokenguard/backups/logs/backup_$(date +%Y%m%d).log"

/var/www/tokenguard/scripts/backup.sh all >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    echo "Ошибка при создании бэкапа!" >> "$LOG_FILE"
fi

find /var/www/tokenguard/backups/logs -name "backup_*.log" -mtime +30 -delete