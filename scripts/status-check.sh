#!/bin/bash

BOLD='\033[1m'
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

DOCKER_COMPOSE_PROD="docker compose -f docker-compose.prod.yml"

echo -e "${BOLD}${CYAN}======================== Docker ps ========================${NC}"
$DOCKER_COMPOSE_PROD ps
echo ""

echo -e "${BOLD}${CYAN}======================== Docker Service ========================${NC}"
echo -n "docker.service status: "
sudo systemctl is-active docker 2>/dev/null || echo "not found"
echo -n "  ├─ Loaded: "
sudo systemctl show docker --property=LoadState --value 2>/dev/null | sed 's/loaded/✓/' || echo "not found"
echo -n "  ├─ Enabled: "
enabled=$(sudo systemctl is-enabled docker 2>/dev/null)
if [ "$enabled" = "enabled" ]; then
    echo "✓"
elif [ "$enabled" = "disabled" ]; then
    echo -e "${RED}disabled${NC}"
else
    echo "not found"
fi
echo -n "  └─ Active: "
active=$(sudo systemctl show docker --property=ActiveState --value 2>/dev/null)
if [ "$active" = "active" ]; then
    echo "✓"
elif [ "$active" = "inactive" ]; then
    echo -e "${RED}✗ inactive${NC}"
elif [ "$active" = "failed" ]; then
    echo -e "${RED}✗ failed${NC}"
else
    echo "not found"
fi
echo ""

echo -n "Docker version: "
docker --version 2>/dev/null || echo "not found"
echo -n "Docker Compose version: "
docker compose version 2>/dev/null | cut -d' ' -f3,4 || echo "not found"
echo ""

echo -e "${BOLD}${CYAN}======================== Healthcheck ========================${NC}"
echo -n "Backend health (localhost:8000): "
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health || echo " FAILED"
echo ""
echo -n "HTTP (tokenguard.ru): "
curl -s -o /dev/null -w "%{http_code}" http://tokenguard.ru || echo " FAILED"
echo ""
echo -n "HTTPS (tokenguard.ru): "
curl -s -o /dev/null -w "%{http_code}" https://tokenguard.ru || echo " FAILED"
echo ""
echo -n "HTTPS response time: "
curl -s -o /dev/null -w "%{time_total}s\n" https://tokenguard.ru || echo " N/A"
echo ""

echo -e "${BOLD}${CYAN}======================== Database ========================${NC}"
echo -n "Postgres status: "
$DOCKER_COMPOSE_PROD exec -T postgres pg_isready -U prod_user -d decoy_tokens_prod 2>/dev/null
echo -n "Active connections: "
$DOCKER_COMPOSE_PROD exec -T postgres psql -U prod_user -d decoy_tokens_prod -tAc "SELECT count(*) FROM pg_stat_activity;" 2>/dev/null || echo "N/A"
echo -n "Database size: "
$DOCKER_COMPOSE_PROD exec -T postgres psql -U prod_user -d decoy_tokens_prod -tAc "SELECT pg_database_size(current_database()) / 1024 / 1024 || ' MB';" 2>/dev/null || echo "N/A"
echo ""

echo -e "${BOLD}${CYAN}======================== Redis ========================${NC}"
echo -n "Redis status: "
$DOCKER_COMPOSE_PROD exec -T redis redis-cli ping 2>/dev/null || echo "Not available"
echo ""

echo -e "${BOLD}${CYAN}======================== SSL Certificate ========================${NC}"
echo -n "SSL issuer: "
echo | openssl s_client -servername tokenguard.ru -connect tokenguard.ru:443 2>/dev/null | openssl x509 -noout -issuer 2>/dev/null | sed 's/issuer=//' || echo "N/A"
echo -n "SSL expiry date: "
echo | openssl s_client -servername tokenguard.ru -connect tokenguard.ru:443 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2 || echo "N/A"
echo -n "SSL days remaining: "
expiry=$(echo | openssl s_client -servername tokenguard.ru -connect tokenguard.ru:443 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)
if [ -n "$expiry" ]; then
    expiry_epoch=$(date -d "$expiry" +%s 2>/dev/null)
    now_epoch=$(date +%s)
    days=$(( (expiry_epoch - now_epoch) / 86400 ))
    if [ $days -lt 7 ]; then
        echo -e "${RED}$days days${NC}"
    elif [ $days -lt 30 ]; then
        echo -e "${YELLOW}$days days${NC}"
    else
        echo -e "${GREEN}$days days${NC}"
    fi
else
    echo "N/A"
fi
echo -n "HTTP/2 support: "
curl -sI https://tokenguard.ru --http2 -o /dev/null -w "%{http_version}" 2>/dev/null | grep -q "2" && echo -e "${GREEN}Enabled${NC}" || echo -e "${RED}Not enabled${NC}"
echo ""

echo -e "${BOLD}${CYAN}======================== Nginx ========================${NC}"
echo -n "nginx.service status: "
sudo systemctl is-active nginx 2>/dev/null || echo "not found"
echo -n "  ├─ Loaded: "
sudo systemctl show nginx --property=LoadState --value 2>/dev/null | sed 's/loaded/✓/' || echo "not found"
echo -n "  ├─ Enabled: "
enabled=$(sudo systemctl is-enabled nginx 2>/dev/null)
if [ "$enabled" = "enabled" ]; then
    echo "✓"
elif [ "$enabled" = "disabled" ]; then
    echo -e "${RED}disabled${NC}"
else
    echo "not found"
fi
echo -n "  └─ Active: "
active=$(sudo systemctl show nginx --property=ActiveState --value 2>/dev/null)
if [ "$active" = "active" ]; then
    echo "✓"
elif [ "$active" = "inactive" ]; then
    echo -e "${RED}✗ inactive${NC}"
elif [ "$active" = "failed" ]; then
    echo -e "${RED}✗ failed${NC}"
else
    echo "not found"
fi
echo ""

echo -n "Nginx config test: "
sudo nginx -t 2>&1 | grep -q "successful" && echo -e "${GREEN}OK${NC}" || echo -e "${RED}Failed${NC}"
echo ""

echo -e "${BOLD}${CYAN}======================== Systemd Services ========================${NC}"
echo -n "tokenguard.service status: "
sudo systemctl is-active tokenguard 2>/dev/null || echo "not found"
echo -n "  ├─ Loaded: "
sudo systemctl show tokenguard --property=LoadState --value 2>/dev/null | sed 's/loaded/✓/' || echo "not found"
echo -n "  ├─ Enabled: "
enabled=$(sudo systemctl is-enabled tokenguard 2>/dev/null)
if [ "$enabled" = "enabled" ]; then
    echo "✓"
elif [ "$enabled" = "disabled" ]; then
    echo -e "${RED}disabled${NC}"
else
    echo "not found"
fi
echo -n "  └─ Active: "
active=$(sudo systemctl show tokenguard --property=ActiveState --value 2>/dev/null)
if [ "$active" = "active" ]; then
    echo "✓"
elif [ "$active" = "inactive" ]; then
    echo -e "${RED}✗ inactive${NC}"
elif [ "$active" = "failed" ]; then
    echo -e "${RED}✗ failed${NC}"
else
    echo "not found"
fi
echo ""

echo -e "${BOLD}${CYAN}======================== System Resources ========================${NC}"
echo -n "CPU load: "
uptime | awk -F'load average:' '{print $2}'
echo -n "Memory usage: "
free -h | awk '/^Mem:/ {print $3 "/" $2}'
echo -n "Disk usage: "
df -h / | awk 'NR==2 {print $5 " used (" $3 "/" $2 ")"}'
echo ""

echo -e "${BOLD}${GREEN}======================== Summary ========================${NC}"
echo -n "Overall status: "
if curl -s -f http://localhost:8000/health > /dev/null 2>&1 && \
   curl -s -f https://tokenguard.ru > /dev/null 2>&1 && \
   $DOCKER_COMPOSE_PROD exec -T postgres pg_isready -U prod_user > /dev/null 2>&1; then
    echo -e "${GREEN}All systems operational${NC}"
else
    echo -e "${RED}Some services may have issues${NC}"
fi
echo ""

echo "Last 5 backend errors:"
$DOCKER_COMPOSE_PROD logs --tail=50 backend 2>/dev/null | grep -i "error\|exception\|fail" | tail -5 || echo "No recent errors"
echo ""