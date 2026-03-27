#!/bin/bash

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Конфигурация
PROJECT_ROOT="/var/www/tokenguard"
BACKUP_ROOT="/var/backups/tokenguard"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Типы бэкапов
BACKUP_TYPE=${1:-"all"}

# Google Drive конфигурация
GDRIVE_REMOTE="gdrive"
GDRIVE_PATH="tokenguard_backups"  # Используем существующую папку
ENABLE_GDRIVE=${ENABLE_GDRIVE:-true}

# Настройка логирования
LOG_DIR="$BACKUP_ROOT/logs"
LOG_FILE="$LOG_DIR/backup_${TIMESTAMP}.log"
ERROR_LOG="$LOG_DIR/backup_errors.log"

# Функция для логирования
log() {
    local message="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo -e "${BLUE}${message}${NC}" | tee -a "$LOG_FILE"
}

error() {
    local message="[ERROR] $1"
    echo -e "${RED}${message}${NC}" | tee -a "$LOG_FILE"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$ERROR_LOG"
    exit 1
}

success() {
    local message="[SUCCESS] $1"
    echo -e "${GREEN}${message}${NC}" | tee -a "$LOG_FILE"
}

warning() {
    local message="[WARNING] $1"
    echo -e "${YELLOW}${message}${NC}" | tee -a "$LOG_FILE"
}

# Отправка файла в Google Drive
upload_to_gdrive() {
    if [ "$ENABLE_GDRIVE" != "true" ]; then
        return 0
    fi
    
    local file_path="$1"
    local file_type="$2"
    
    if [ ! -f "$file_path" ]; then
        warning "Файл для загрузки не найден: $file_path"
        return 1
    fi
    
    local file_name=$(basename "$file_path")
    local file_size=$(du -h "$file_path" | cut -f1)
    
    log "Загрузка $file_type ($file_size) в Google Drive..."
    
    # Создаем директорию
    rclone mkdir "${GDRIVE_REMOTE}:${GDRIVE_PATH}/${file_type}" 2>/dev/null || true
    
    # Загружаем с прогрессом
    if rclone copy "$file_path" "${GDRIVE_REMOTE}:${GDRIVE_PATH}/${file_type}/" \
        --progress \
        --stats 1s 2>&1 | tee -a "$LOG_FILE"; then
        success "Загрузка в Google Drive завершена"
        return 0
    else
        warning "Ошибка загрузки в Google Drive"
        return 1
    fi
}

# Настройка логирования
setup_logging() {
    mkdir -p "$LOG_DIR"
    touch "$LOG_FILE"
    
    cat >> "$LOG_FILE" << EOF
=========================================
Backup session started: $(date)
Backup type: $BACKUP_TYPE
Host: $(hostname)
User: $(whoami)
Google Drive: $([ "$ENABLE_GDRIVE" = "true" ] && echo "Enabled" || echo "Disabled")
Telegram: $([ "$ENABLE_TELEGRAM" = "true" ] && echo "Enabled" || echo "Disabled")
=========================================
EOF
}

# Проверка дискового пространства
check_disk_space() {
    local available=$(df -h "$BACKUP_ROOT" | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$available" -gt 90 ]; then
        warning "Дисковое пространство: ${available}% использовано"
    fi
}

# Проверка директорий
check_directories() {
    log "Проверка директорий..."
    cd "$PROJECT_ROOT" || error "Не удалось перейти в $PROJECT_ROOT"
    
    mkdir -p "$BACKUP_ROOT"/{sql,code,static,updates,logs}
}

# Бэкап базы данных
backup_database() {
    log "Создание бэкапа базы данных..."
    
    BACKUP_FILE="$BACKUP_ROOT/sql/backup_${TIMESTAMP}.sql.gz"
    
    # Проверяем, запущен ли контейнер postgres
    if ! docker compose -f docker-compose.prod.yml ps postgres 2>/dev/null | grep -q "Up"; then
        error "Контейнер postgres не запущен"
    fi
    
    # Создаем дамп и сжимаем
    local start_time=$(date +%s)
    if docker compose -f docker-compose.prod.yml exec -T postgres \
        pg_dump -U prod_user decoy_tokens_prod 2>>"$LOG_FILE" | gzip > "$BACKUP_FILE"; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
        success "Бэкап БД создан: $BACKUP_FILE ($SIZE) за ${duration} сек"
        
        ln -sf "$BACKUP_FILE" "$BACKUP_ROOT/sql/latest.sql.gz"
        
        # Записываем информацию
        cat > "$BACKUP_ROOT/sql/latest.info" << EOF
Backup: $TIMESTAMP
Size: $SIZE
Duration: ${duration} sec
Type: database
Date: $(date)
EOF
        
        # Отправляем в Google Drive
        upload_to_gdrive "$BACKUP_FILE" "db"
    else
        error "Не удалось создать бэкап БД"
    fi
}

# Бэкап кода
backup_code() {
    log "Создание бэкапа кода..."
    
    BACKUP_FILE="$BACKUP_ROOT/code/code_${TIMESTAMP}.tar.gz"
    
    local start_time=$(date +%s)
    tar -czf "$BACKUP_FILE" \
        --exclude='**/__pycache__' \
        --exclude='*.pyc' \
        --exclude='.env' \
        --exclude='node_modules' \
        --exclude='.git' \
        --exclude='backups' \
        --exclude='*.log' \
        --exclude='*.pid' \
        backend/ alembic.ini docker-compose.prod.yml Makefile 2>>"$LOG_FILE"
    
    if [ $? -eq 0 ] && [ -f "$BACKUP_FILE" ]; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
        success "Бэкап кода создан: $BACKUP_FILE ($SIZE) за ${duration} сек"
        ln -sf "$BACKUP_FILE" "$BACKUP_ROOT/code/latest.tar.gz"
        
        # Отправляем в Google Drive
        upload_to_gdrive "$BACKUP_FILE" "code"
        
    else
        error "Не удалось создать бэкап кода"
    fi
}

# Бэкап статических файлов
backup_static() {
    log "Создание бэкапа статических файлов..."
    
    BACKUP_FILE="$BACKUP_ROOT/static/static_${TIMESTAMP}.tar.gz"
    
    if [ -d "backend/app/static" ]; then
        local start_time=$(date +%s)
        tar -czf "$BACKUP_FILE" \
            --exclude='*.pyc' \
            backend/app/static/ 2>>"$LOG_FILE"
        
        if [ $? -eq 0 ] && [ -f "$BACKUP_FILE" ]; then
            local end_time=$(date +%s)
            local duration=$((end_time - start_time))
            SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
            success "Бэкап статики создан: $BACKUP_FILE ($SIZE) за ${duration} сек"
            ln -sf "$BACKUP_FILE" "$BACKUP_ROOT/static/latest.tar.gz"
            
            # Отправляем в Google Drive
            upload_to_gdrive "$BACKUP_FILE" "static"
            
        fi
    else
        warning "Директория static не найдена"
    fi
}

# Бэкап обновлений
backup_updates() {
    log "Сохранение информации об обновлениях..."
    
    BACKUP_FILE="$BACKUP_ROOT/updates/update_${TIMESTAMP}.info"
    
    cat > "$BACKUP_FILE" << EOF
Update Information
==================
Timestamp: $TIMESTAMP
Date: $(date)
Git commit: $(git rev-parse HEAD 2>/dev/null || echo "N/A")
Git branch: $(git branch --show-current 2>/dev/null || echo "N/A")
Host: $(hostname)
User: $(whoami)

Changed files:
$(git diff --name-status HEAD 2>/dev/null || echo "N/A")
EOF
    
    success "Информация об обновлении сохранена: $BACKUP_FILE"
    
    # Отправляем в Google Drive
    upload_to_gdrive "$BACKUP_FILE" "updates"
}

# Очистка старых бэкапов
cleanup_old_backups() {
    log "Очистка бэкапов старше $RETENTION_DAYS дней..."
    
    # Локальная очистка
    removed_db=$(find "$BACKUP_ROOT/sql" -name "backup_*.sql.gz" -type f -mtime +$RETENTION_DAYS -delete -print | wc -l)
    removed_code=$(find "$BACKUP_ROOT/code" -name "code_*.tar.gz" -type f -mtime +$RETENTION_DAYS -delete -print | wc -l)
    removed_static=$(find "$BACKUP_ROOT/static" -name "static_*.tar.gz" -type f -mtime +$RETENTION_DAYS -delete -print | wc -l)
    removed_updates=$(find "$BACKUP_ROOT/updates" -name "update_*.info" -type f -mtime +$RETENTION_DAYS -delete -print | wc -l)
    removed_logs=$(find "$BACKUP_ROOT/logs" -name "backup_*.log" -type f -mtime +$RETENTION_DAYS -delete -print | wc -l)
    
    success "Локальная очистка: удалено $removed_db бэкапов БД, $removed_code кода, $removed_static статики"
}

# Показать информацию
show_backup_info() {
    echo ""
    echo "========================================="
    echo "Последние бэкапы:"
    echo "========================================="
    
    if [ -f "$BACKUP_ROOT/sql/latest.sql.gz" ]; then
        echo "БД:      $(ls -lh $BACKUP_ROOT/sql/latest.sql.gz | awk '{print $5, $9}')"
        echo "Инфо:    $(cat $BACKUP_ROOT/sql/latest.info 2>/dev/null | head -1)"
    fi
    
    if [ -f "$BACKUP_ROOT/code/latest.tar.gz" ]; then
        echo "Код:     $(ls -lh $BACKUP_ROOT/code/latest.tar.gz | awk '{print $5, $9}')"
    fi
    
    if [ -f "$BACKUP_ROOT/static/latest.tar.gz" ]; then
        echo "Стат:    $(ls -lh $BACKUP_ROOT/static/latest.tar.gz | awk '{print $5, $9}')"
    fi
    
    echo ""
    echo "Статистика:"
    echo "  БД:    $(ls -1 $BACKUP_ROOT/sql/backup_*.sql.gz 2>/dev/null | wc -l) бэкапов, $(du -sh $BACKUP_ROOT/sql 2>/dev/null | cut -f1)"
    echo "  Код:   $(ls -1 $BACKUP_ROOT/code/code_*.tar.gz 2>/dev/null | wc -l) бэкапов, $(du -sh $BACKUP_ROOT/code 2>/dev/null | cut -f1)"
    echo "  Стат:  $(ls -1 $BACKUP_ROOT/static/static_*.tar.gz 2>/dev/null | wc -l) бэкапов, $(du -sh $BACKUP_ROOT/static 2>/dev/null | cut -f1)"
    echo "  Логи:  $(ls -1 $BACKUP_ROOT/logs/backup_*.log 2>/dev/null | wc -l) файлов, $(du -sh $BACKUP_ROOT/logs 2>/dev/null | cut -f1)"
    echo "========================================="
}

# Создание полного бэкапа
backup_all() {
    local start_time=$(date +%s)
    
    log "=== Создание полного бэкапа ==="
    
    backup_database
    backup_code
    backup_static
    backup_updates
    cleanup_old_backups
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    log "Полный бэкап завершен за ${duration} секунд"
    show_backup_info
}

# Справка
show_help() {
    cat << EOF
Использование: $0 [COMMAND]

Команды:
  all          Создать полный бэкап (БД, код, статика)
  db           Создать бэкап только базы данных
  code         Создать бэкап только кода
  static       Создать бэкап только статических файлов
  cleanup      Очистить старые бэкапы
  list         Показать список бэкапов
  help         Показать эту справку

Примеры:
  $0 all              # Создать полный бэкап
  $0 db               # Создать бэкап БД
EOF
}

# Основная логика
main() {
    setup_logging
    check_directories
    check_disk_space
    
    case "${BACKUP_TYPE}" in
        all)
            backup_all
            ;;
        db)
            backup_database
            ;;
        code)
            backup_code
            ;;
        static)
            backup_static
            ;;
        cleanup)
            cleanup_old_backups
            ;;
        list)
            show_backup_info
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            show_help
            ;;
    esac
}

main "$@"
