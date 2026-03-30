#!/bin/bash

YELLOW='\033[0;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

CLEAN_CACHE=false

if [ "$1" == "--clean" ] || [ "$1" == "-c" ]; then
    CLEAN_CACHE=true
    echo -e "${YELLOW}[!] Full cache clean mode enabled${NC}"
fi

echo -e "${YELLOW}0. Backup project...${NC}"
make prod-backup

echo -e "${YELLOW}1. Pulling latest changes...${NC}"
make prod-upgrade

echo -e "${YELLOW}2. Stopping containers...${NC}"
make prod-down

if [ "$CLEAN_CACHE" = true ]; then
    echo -e "${YELLOW}3. Cleaning Docker cache...${NC}"
    
    docker builder prune -f
    
    docker image prune -f
    
    echo -e "${YELLOW}   Removing backend image...${NC}"
    docker rmi $(docker images -q decoy-tokens-backend) 2>/dev/null || true
    
    # docker system prune -a -f
    
    echo -e "${GREEN}   Cache cleaned successfully${NC}"
fi

echo -e "${YELLOW}4. Rebuilding Docker image...${NC}"
if [ "$CLEAN_CACHE" = true ]; then
    docker compose -f docker-compose.prod.yml build --no-cache backend
else
    make prod-rebuild
fi

echo -e "${YELLOW}5. Starting containers...${NC}"
make prod-up

echo -e "${YELLOW}6. Running migrations...${NC}"
sleep 15
make prod-migrate

echo -e "${YELLOW}7. Checking status...${NC}"
sleep 3
make prod-status

echo -e "${GREEN}[+] Deployment completed!${NC}"