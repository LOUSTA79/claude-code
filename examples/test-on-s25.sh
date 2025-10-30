#!/bin/bash

# Quick Test Script for Samsung S25 Ultra
# ========================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

clear

echo -e "${PURPLE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🧪 TESTING CODING AGENTS ON S25 ULTRA                      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${BLUE}📱 System Check...${NC}\n"

# Check if we're in Termux
if [ -d "/data/data/com.termux" ]; then
    echo -e "${GREEN}✅ Running in Termux${NC}"
else
    echo -e "${YELLOW}⚠️  Not in Termux (but continuing)${NC}"
fi

# Check current location
echo -e "${BLUE}📂 Current directory: $(pwd)${NC}"

# Check if examples directory exists
if [ -d "examples" ]; then
    echo -e "${GREEN}✅ Examples directory found${NC}"
else
    echo -e "${RED}❌ Examples directory not found${NC}"
    echo -e "${YELLOW}Run this from the repository root${NC}"
    exit 1
fi

echo ""
echo -e "${CYAN}Choose what to test:${NC}\n"
echo -e "${GREEN}1) Test JavaScript PWA${NC}"
echo -e "   Quick check if Node.js server works"
echo ""
echo -e "${GREEN}2) Test Go CLI${NC}"
echo -e "   Build and test the Go binary"
echo ""
echo -e "${GREEN}3) Test Both${NC}"
echo -e "   Run both systems"
echo ""
echo -e "${GREEN}4) System Info Only${NC}"
echo -e "   Just check what's installed"
echo ""
echo -e "${RED}5) Exit${NC}"
echo ""

read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo -e "\n${BLUE}🧪 Testing JavaScript PWA...${NC}\n"

        # Check Node.js
        if command -v node &> /dev/null; then
            echo -e "${GREEN}✅ Node.js $(node -v) installed${NC}"
        else
            echo -e "${RED}❌ Node.js not installed${NC}"
            echo -e "${YELLOW}Install with: pkg install nodejs${NC}"
            exit 1
        fi

        # Check if app exists
        if [ ! -d "examples/s25-ultra-agent-app" ]; then
            echo -e "${RED}❌ JavaScript PWA not found${NC}"
            exit 1
        fi

        cd examples/s25-ultra-agent-app

        # Install dependencies
        if [ ! -d "node_modules" ]; then
            echo -e "${YELLOW}📦 Installing dependencies...${NC}"
            npm install
        fi

        # Check for .env
        if [ ! -f ".env" ]; then
            echo -e "${YELLOW}📝 Creating .env from example...${NC}"
            cp .env.example .env
            echo -e "${RED}⚠️  IMPORTANT: Edit .env and add your OPENAI_API_KEY${NC}"
            echo -e "${YELLOW}   nano .env${NC}"
            echo ""
            read -p "Press Enter after you've added your API key..."
        fi

        # Test syntax
        echo -e "${BLUE}🔍 Checking server code...${NC}"
        node -c server/index.js
        echo -e "${GREEN}✅ Server code is valid${NC}"

        # Offer to start
        echo ""
        echo -e "${CYAN}Ready to start the server!${NC}"
        echo -e "${CYAN}It will run on http://localhost:3000${NC}"
        echo ""
        read -p "Start server now? (y/n): " start

        if [[ "$start" =~ ^[Yy]$ ]]; then
            echo -e "${GREEN}🚀 Starting server...${NC}"
            echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
            echo ""
            npm start
        else
            echo -e "${YELLOW}To start later, run: npm start${NC}"
        fi
        ;;

    2)
        echo -e "\n${BLUE}🧪 Testing Go CLI...${NC}\n"

        # Check Go
        if command -v go &> /dev/null; then
            echo -e "${GREEN}✅ Go $(go version | awk '{print $3}') installed${NC}"
        else
            echo -e "${RED}❌ Go not installed${NC}"
            echo -e "${YELLOW}Install with: pkg install golang${NC}"
            exit 1
        fi

        # Check API key
        if [ -z "$ANTHROPIC_API_KEY" ]; then
            echo -e "${YELLOW}⚠️  ANTHROPIC_API_KEY not set${NC}"
            echo -e "${BLUE}Enter your Anthropic API key:${NC}"
            read -p "API Key: " api_key
            export ANTHROPIC_API_KEY="$api_key"
        else
            echo -e "${GREEN}✅ ANTHROPIC_API_KEY is set${NC}"
        fi

        # Check if workshop exists
        if [ ! -d "examples/go-coding-agent-workshop" ]; then
            echo -e "${RED}❌ Go workshop not found${NC}"
            exit 1
        fi

        cd examples/go-coding-agent-workshop

        # Download dependencies
        echo -e "${YELLOW}📦 Downloading dependencies...${NC}"
        go mod tidy

        # Build
        echo -e "${YELLOW}🔨 Building agent...${NC}"
        mkdir -p bin
        go build -ldflags="-s -w" -o bin/agent cmd/main.go

        if [ $? -eq 0 ]; then
            SIZE=$(ls -lh bin/agent | awk '{print $5}')
            echo -e "${GREEN}✅ Build successful! (${SIZE})${NC}"

            # Test help
            echo -e "\n${BLUE}📖 Available commands:${NC}"
            ./bin/agent --help

            echo ""
            echo -e "${CYAN}Ready to use!${NC}"
            echo ""
            read -p "Start chat agent now? (y/n): " start

            if [[ "$start" =~ ^[Yy]$ ]]; then
                echo -e "${GREEN}🚀 Starting chat agent...${NC}"
                echo -e "${YELLOW}Type 'exit' to quit${NC}"
                echo ""
                ./bin/agent chat
            else
                echo -e "${YELLOW}To start later, run: ./bin/agent chat${NC}"
            fi
        else
            echo -e "${RED}❌ Build failed${NC}"
            exit 1
        fi
        ;;

    3)
        echo -e "\n${BLUE}🧪 Testing Both Systems...${NC}\n"

        # Test JavaScript PWA
        echo -e "${PURPLE}═══ Testing JavaScript PWA ═══${NC}\n"

        if command -v node &> /dev/null && [ -d "examples/s25-ultra-agent-app" ]; then
            cd examples/s25-ultra-agent-app
            if [ ! -d "node_modules" ]; then
                npm install
            fi
            if [ ! -f ".env" ]; then
                cp .env.example .env
                echo -e "${YELLOW}⚠️  Edit .env and add OPENAI_API_KEY${NC}"
            fi
            node -c server/index.js && echo -e "${GREEN}✅ JavaScript PWA: OK${NC}" || echo -e "${RED}❌ JavaScript PWA: FAILED${NC}"
            cd ../..
        else
            echo -e "${RED}❌ JavaScript PWA: Prerequisites missing${NC}"
        fi

        echo ""

        # Test Go CLI
        echo -e "${PURPLE}═══ Testing Go CLI ═══${NC}\n"

        if command -v go &> /dev/null && [ -d "examples/go-coding-agent-workshop" ]; then
            cd examples/go-coding-agent-workshop
            go mod tidy
            mkdir -p bin
            go build -ldflags="-s -w" -o bin/agent cmd/main.go
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✅ Go CLI: OK${NC}"
            else
                echo -e "${RED}❌ Go CLI: FAILED${NC}"
            fi
            cd ../..
        else
            echo -e "${RED}❌ Go CLI: Prerequisites missing${NC}"
        fi

        echo ""
        echo -e "${GREEN}✅ Testing complete!${NC}"
        ;;

    4)
        echo -e "\n${BLUE}📊 System Information${NC}\n"

        echo -e "${PURPLE}═══ Environment ═══${NC}"
        echo "Device: $(uname -m)"
        echo "OS: $(uname -s)"
        echo "Kernel: $(uname -r)"

        echo ""
        echo -e "${PURPLE}═══ Installed Software ═══${NC}"

        # Node.js
        if command -v node &> /dev/null; then
            echo -e "${GREEN}✅ Node.js: $(node -v)${NC}"
        else
            echo -e "${RED}❌ Node.js: Not installed${NC}"
        fi

        # npm
        if command -v npm &> /dev/null; then
            echo -e "${GREEN}✅ npm: $(npm -v)${NC}"
        else
            echo -e "${RED}❌ npm: Not installed${NC}"
        fi

        # Go
        if command -v go &> /dev/null; then
            echo -e "${GREEN}✅ Go: $(go version | awk '{print $3}')${NC}"
        else
            echo -e "${RED}❌ Go: Not installed${NC}"
        fi

        # Git
        if command -v git &> /dev/null; then
            echo -e "${GREEN}✅ Git: $(git --version | awk '{print $3}')${NC}"
        else
            echo -e "${RED}❌ Git: Not installed${NC}"
        fi

        # PM2
        if command -v pm2 &> /dev/null; then
            echo -e "${GREEN}✅ PM2: $(pm2 -v)${NC}"
        else
            echo -e "${YELLOW}⚠️  PM2: Not installed${NC}"
        fi

        echo ""
        echo -e "${PURPLE}═══ API Keys ═══${NC}"

        if [ -z "$OPENAI_API_KEY" ]; then
            echo -e "${RED}❌ OPENAI_API_KEY: Not set${NC}"
        else
            echo -e "${GREEN}✅ OPENAI_API_KEY: Set${NC}"
        fi

        if [ -z "$ANTHROPIC_API_KEY" ]; then
            echo -e "${RED}❌ ANTHROPIC_API_KEY: Not set${NC}"
        else
            echo -e "${GREEN}✅ ANTHROPIC_API_KEY: Set${NC}"
        fi

        echo ""
        echo -e "${PURPLE}═══ Projects ═══${NC}"

        if [ -d "examples/s25-ultra-agent-app" ]; then
            echo -e "${GREEN}✅ JavaScript PWA: Found${NC}"
        else
            echo -e "${RED}❌ JavaScript PWA: Not found${NC}"
        fi

        if [ -d "examples/go-coding-agent-workshop" ]; then
            echo -e "${GREEN}✅ Go CLI: Found${NC}"
        else
            echo -e "${RED}❌ Go CLI: Not found${NC}"
        fi
        ;;

    5)
        echo -e "\n${GREEN}👋 Goodbye!${NC}\n"
        exit 0
        ;;

    *)
        echo -e "\n${RED}❌ Invalid choice${NC}\n"
        exit 1
        ;;
esac
