#!/bin/bash

YELLOW='\033[0;33m'
NC='\033[0m'

echo -e "${YELLOW}0. Backup project...${NC}"
make prod-backup

echo -e "${YELLOW}1. Pulling latest changes...${NC}"
make prod-upgrade

echo -e "${YELLOW}2. Stopping containers...${NC}"
make prod-down

echo -e "${YELLOW}3. Rebuilding Docker image...${NC}"
make prod-rebuild

echo -e "${YELLOW}4. Starting containers...${NC}"
make prod-up

echo -e "${YELLOW}5. Running migrations...${NC}"
sleep 15
make prod-migrate

echo -e "${YELLOW}6. Checking status...${NC}"
sleep 3
make prod-status