#!/bin/bash

# Unified Coding Agent Launcher for Samsung S25 Ultra
# ====================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

clear

echo -e "${PURPLE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║           🤖 CODING AGENT LAUNCHER                           ║
║              Samsung Galaxy S25 Ultra Edition                 ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${CYAN}Choose your coding agent:${NC}\n"

echo -e "${GREEN}1) JavaScript PWA${NC} - Web-based with beautiful UI"
echo -e "   📱 7 agents (Chat, Read, List, Bash, Edit, Search, Generate)"
echo -e "   🌐 Install to home screen"
echo -e "   🎤 Voice input support"
echo -e "   💾 Memory: ~50-100 MB"
echo ""

echo -e "${GREEN}2) Go CLI${NC} - Terminal-based, lightning fast"
echo -e "   ⚡ 6 agents (Chat, Read, List, Bash, Edit, Search)"
echo -e "   🚀 Instant startup (<100ms)"
echo -e "   ⌨️  Keyboard-driven workflow"
echo -e "   💾 Memory: ~10-30 MB"
echo ""

echo -e "${GREEN}3) Both${NC} - Launch both systems"
echo -e "   🔄 Best of both worlds"
echo -e "   💡 Use PWA for visual tasks, CLI for quick queries"
echo ""

echo -e "${YELLOW}4) Help${NC} - Show detailed comparison"
echo ""
echo -e "${RED}5) Exit${NC}"
echo ""

read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo -e "\n${BLUE}🚀 Launching JavaScript PWA...${NC}\n"

        # Check if exists
        if [ ! -d "s25-ultra-agent-app" ]; then
            echo -e "${RED}❌ JavaScript PWA not found${NC}"
            echo -e "${YELLOW}Expected location: $(pwd)/s25-ultra-agent-app${NC}"
            echo -e "${YELLOW}Run the setup first!${NC}"
            exit 1
        fi

        cd s25-ultra-agent-app

        # Check dependencies
        if [ ! -d "node_modules" ]; then
            echo -e "${YELLOW}📦 Installing dependencies...${NC}"
            npm install
        fi

        # Check .env
        if [ ! -f ".env" ]; then
            echo -e "${YELLOW}📝 Creating .env file...${NC}"
            cp .env.example .env
            echo -e "${RED}⚠️  Please edit .env and add your OPENAI_API_KEY${NC}"
            echo -e "${YELLOW}   nano .env${NC}"
            exit 1
        fi

        # Check API key
        if grep -q "your-api-key-here" .env; then
            echo -e "${RED}⚠️  Please configure your API key in .env${NC}"
            echo -e "${YELLOW}   nano .env${NC}"
            exit 1
        fi

        echo -e "${GREEN}✅ Starting server...${NC}"
        echo -e "${CYAN}📱 Open http://localhost:3000 in your browser${NC}"
        echo -e "${CYAN}📲 Tap menu (⋮) → 'Add to Home screen' to install${NC}"
        echo ""

        npm start
        ;;

    2)
        echo -e "\n${BLUE}🚀 Launching Go CLI...${NC}\n"

        # Check if exists
        if [ ! -d "go-coding-agent-workshop" ]; then
            echo -e "${RED}❌ Go CLI not found${NC}"
            echo -e "${YELLOW}Expected location: $(pwd)/go-coding-agent-workshop${NC}"
            echo -e "${YELLOW}Run the setup first!${NC}"
            exit 1
        fi

        cd go-coding-agent-workshop

        # Check if binary exists
        if [ ! -f "bin/agent" ]; then
            echo -e "${YELLOW}🔨 Building agent...${NC}"

            if ! command -v go &> /dev/null; then
                echo -e "${RED}❌ Go not installed${NC}"
                echo -e "${YELLOW}Install with: pkg install golang${NC}"
                exit 1
            fi

            go mod tidy
            mkdir -p bin
            go build -ldflags="-s -w" -o bin/agent cmd/main.go
        fi

        # Check API key
        if [ -z "$ANTHROPIC_API_KEY" ]; then
            echo -e "${RED}❌ ANTHROPIC_API_KEY not set${NC}"
            echo -e "${YELLOW}Set it with: export ANTHROPIC_API_KEY='your-key'${NC}"
            echo -e "${YELLOW}Or add to ~/.bashrc for permanence${NC}"
            exit 1
        fi

        echo -e "${GREEN}✅ Ready!${NC}"
        echo -e "${CYAN}💬 Available commands:${NC}"
        echo -e "   ./bin/agent chat    - Interactive chat"
        echo -e "   ./bin/agent read    - Read and analyze files"
        echo -e "   ./bin/agent list    - List directories"
        echo -e "   ./bin/agent bash    - Execute commands"
        echo -e "   ./bin/agent edit    - Create/edit files"
        echo -e "   ./bin/agent search  - Search code"
        echo ""
        echo -e "${CYAN}Starting chat agent...${NC}"
        echo ""

        ./bin/agent chat
        ;;

    3)
        echo -e "\n${BLUE}🚀 Launching both systems...${NC}\n"

        # Start JavaScript PWA in background
        if [ -d "s25-ultra-agent-app" ]; then
            echo -e "${GREEN}📱 Starting JavaScript PWA...${NC}"
            cd s25-ultra-agent-app

            if [ -d "node_modules" ] && [ -f ".env" ] && ! grep -q "your-api-key-here" .env; then
                npm run pm2:start &> /dev/null || npm start &
                echo -e "${GREEN}✅ JavaScript PWA started on http://localhost:3000${NC}"
            else
                echo -e "${YELLOW}⚠️  JavaScript PWA needs setup${NC}"
            fi

            cd ..
        fi

        # Start Go CLI in foreground
        if [ -d "go-coding-agent-workshop" ]; then
            echo -e "${GREEN}⚡ Starting Go CLI...${NC}"
            cd go-coding-agent-workshop

            if [ -f "bin/agent" ] && [ ! -z "$ANTHROPIC_API_KEY" ]; then
                echo ""
                ./bin/agent chat
            else
                echo -e "${YELLOW}⚠️  Go CLI needs setup${NC}"
            fi
        fi
        ;;

    4)
        echo -e "\n${CYAN}📚 Opening comparison guide...${NC}\n"

        if [ -f "CODING_AGENTS_GUIDE.md" ]; then
            if command -v bat &> /dev/null; then
                bat CODING_AGENTS_GUIDE.md
            elif command -v less &> /dev/null; then
                less CODING_AGENTS_GUIDE.md
            else
                cat CODING_AGENTS_GUIDE.md
            fi
        else
            echo -e "${RED}❌ Guide not found${NC}"
            echo -e "${YELLOW}Expected: $(pwd)/CODING_AGENTS_GUIDE.md${NC}"
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
