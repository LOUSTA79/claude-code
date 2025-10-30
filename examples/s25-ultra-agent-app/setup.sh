#!/bin/bash

# Coding Agent App - Setup Script for Samsung S25 Ultra (Termux)
# ================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║  🤖 Coding Agent App Setup                          ║"
echo "║     Samsung Galaxy S25 Ultra Edition                 ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running in Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo -e "${YELLOW}⚠️  Not running in Termux. This script is optimized for Termux.${NC}"
    echo -e "${YELLOW}   Continuing anyway...${NC}"
fi

# Check Node.js
echo -e "${BLUE}🔍 Checking Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found${NC}"
    echo -e "${YELLOW}Installing Node.js in Termux:${NC}"
    echo -e "  pkg install nodejs"
    exit 1
fi

NODE_VERSION=$(node -v)
echo -e "${GREEN}✅ Node.js ${NODE_VERSION} found${NC}"

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm not found${NC}"
    exit 1
fi

NPM_VERSION=$(npm -v)
echo -e "${GREEN}✅ npm ${NPM_VERSION} found${NC}"

# Create .env if it doesn't exist
echo -e "\n${BLUE}📝 Configuration...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"

    # Prompt for API key
    echo -e "${BLUE}Enter your OpenAI API key:${NC}"
    read -p "API Key: " API_KEY

    if [ -z "$API_KEY" ]; then
        echo -e "${YELLOW}⚠️  No API key provided. You'll need to add it manually to .env${NC}"
        API_KEY="your-api-key-here"
    fi

    cat > .env << EOF
# OpenAI Configuration
OPENAI_API_KEY=${API_KEY}
OPENAI_MODEL=gpt-4o-mini

# Server Configuration
PORT=3000

# Device
DEVICE=Samsung S25 Ultra
EOF

    echo -e "${GREEN}✅ .env file created${NC}"
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

# Install dependencies
echo -e "\n${BLUE}📦 Installing dependencies...${NC}"
npm install

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

# Check if PM2 is installed
echo -e "\n${BLUE}🔍 Checking PM2...${NC}"
if ! command -v pm2 &> /dev/null; then
    echo -e "${YELLOW}PM2 not found. Installing globally...${NC}"
    npm install -g pm2

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ PM2 installed${NC}"
    else
        echo -e "${YELLOW}⚠️  PM2 installation failed. You can still use 'npm start'${NC}"
    fi
else
    echo -e "${GREEN}✅ PM2 already installed${NC}"
fi

# Create public directory icons (placeholder)
echo -e "\n${BLUE}🎨 Creating app icons...${NC}"
mkdir -p public

# Create a simple SVG icon that can be converted
cat > public/icon.svg << 'EOF'
<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="80" fill="#6c5ce7"/>
  <text x="256" y="340" font-size="280" text-anchor="middle" fill="white" font-family="Arial, sans-serif">🤖</text>
</svg>
EOF

echo -e "${GREEN}✅ Icon created (icon.svg)${NC}"
echo -e "${YELLOW}   Note: Convert icon.svg to PNG for production:${NC}"
echo -e "${YELLOW}   - icon-192.png (192x192)${NC}"
echo -e "${YELLOW}   - icon-512.png (512x512)${NC}"

# Test server start
echo -e "\n${BLUE}🧪 Testing server...${NC}"
timeout 5 node server/index.js &
SERVER_PID=$!
sleep 3

if ps -p $SERVER_PID > /dev/null; then
    echo -e "${GREEN}✅ Server starts successfully${NC}"
    kill $SERVER_PID 2>/dev/null || true
else
    echo -e "${YELLOW}⚠️  Server test inconclusive${NC}"
fi

# Get local IP
echo -e "\n${BLUE}🌐 Network Information:${NC}"
if command -v ifconfig &> /dev/null; then
    LOCAL_IP=$(ifconfig 2>/dev/null | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}' | head -1)
    if [ ! -z "$LOCAL_IP" ]; then
        echo -e "${GREEN}   Local IP: ${LOCAL_IP}${NC}"
        echo -e "${GREEN}   Access URL: http://${LOCAL_IP}:3000${NC}"
    fi
fi

# Final instructions
echo -e "\n${PURPLE}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║  ✅ Setup Complete!                                  ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  Quick Start:                                        ║"
echo "║                                                      ║"
echo "║  1. Start server:                                    ║"
echo "║     npm start                                        ║"
echo "║     or                                               ║"
echo "║     npm run pm2:start                                ║"
echo "║                                                      ║"
echo "║  2. Open browser on your S25 Ultra:                  ║"
echo "║     http://localhost:3000                            ║"
echo "║                                                      ║"
echo "║  3. Install as PWA:                                  ║"
echo "║     Tap menu (⋮) → Add to Home screen                ║"
echo "║                                                      ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  Useful Commands:                                    ║"
echo "║                                                      ║"
echo "║  npm run pm2:logs    - View logs                     ║"
echo "║  npm run pm2:restart - Restart server                ║"
echo "║  npm run pm2:stop    - Stop server                   ║"
echo "║                                                      ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${GREEN}🚀 Ready to launch!${NC}"
echo -e "${BLUE}Run 'npm start' to begin${NC}"
