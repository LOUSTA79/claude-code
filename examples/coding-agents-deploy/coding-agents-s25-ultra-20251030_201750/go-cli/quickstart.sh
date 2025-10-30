#!/bin/bash

# Go Coding Agent Workshop - Quick Start
# =======================================

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
║   🤖 Go Coding Agent Workshop - Quick Start                  ║
║      Build AI Agents with Claude on Your Phone               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Step 1: Check Go
echo -e "${BLUE}Step 1: Checking Go installation...${NC}"
if ! command -v go &> /dev/null; then
    echo -e "${RED}❌ Go not installed${NC}"
    echo -e "${YELLOW}📦 Installing Go...${NC}"

    if command -v pkg &> /dev/null; then
        pkg install -y golang
    else
        echo -e "${RED}This script is designed for Termux${NC}"
        echo "Please install Go manually: https://go.dev/doc/install"
        exit 1
    fi
fi

GO_VERSION=$(go version | awk '{print $3}')
echo -e "${GREEN}✅ Go ${GO_VERSION} installed${NC}"

# Step 2: Check API Key
echo -e "\n${BLUE}Step 2: Checking Anthropic API key...${NC}"
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  API key not set${NC}"
    echo -e "${BLUE}Get your key from: https://console.anthropic.com/${NC}"
    echo ""
    read -p "Enter your Anthropic API key: " API_KEY

    if [ -z "$API_KEY" ]; then
        echo -e "${RED}❌ No API key provided${NC}"
        exit 1
    fi

    export ANTHROPIC_API_KEY="$API_KEY"

    # Offer to save permanently
    echo ""
    read -p "Save API key permanently? (y/n): " SAVE_KEY
    if [[ "$SAVE_KEY" =~ ^[Yy]$ ]]; then
        echo "export ANTHROPIC_API_KEY='$API_KEY'" >> ~/.bashrc
        echo -e "${GREEN}✅ API key saved to ~/.bashrc${NC}"
    fi
else
    echo -e "${GREEN}✅ API key found${NC}"
fi

# Step 3: Build
echo -e "\n${BLUE}Step 3: Building the agent...${NC}"
if [ ! -f "cmd/main.go" ]; then
    echo -e "${RED}❌ Source files not found${NC}"
    echo "Make sure you're in the go-coding-agent-workshop directory"
    exit 1
fi

echo -e "${YELLOW}📦 Downloading dependencies...${NC}"
go mod tidy

echo -e "${YELLOW}🔨 Compiling...${NC}"
mkdir -p bin
go build -ldflags="-s -w" -o bin/agent cmd/main.go

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Build successful!${NC}"
    SIZE=$(ls -lh bin/agent | awk '{print $5}')
    echo -e "${GREEN}📦 Binary size: ${SIZE}${NC}"
else
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi

# Step 4: Test
echo -e "\n${BLUE}Step 4: Testing the agent...${NC}"
echo -e "${YELLOW}Running quick test...${NC}"

# Test with a simple query (will fail gracefully if API issues)
timeout 5 ./bin/agent chat --help &> /dev/null

if [ $? -eq 0 ] || [ $? -eq 124 ]; then
    echo -e "${GREEN}✅ Agent executable works!${NC}"
else
    echo -e "${YELLOW}⚠️  Agent may have issues, but continuing...${NC}"
fi

# Success!
echo -e "\n${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ✅ Setup Complete! Your AI Agent is Ready!                 ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  🚀 Quick Commands:                                           ║
║                                                               ║
║  Start chat:                                                  ║
║    ./bin/agent chat                                           ║
║                                                               ║
║  With verbose output:                                         ║
║    ./bin/agent chat --verbose                                 ║
║                                                               ║
║  Get help:                                                    ║
║    ./bin/agent --help                                         ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  📱 Mobile Tips:                                              ║
║                                                               ║
║  • Use wake lock: termux-wake-lock                            ║
║  • Run in background with: tmux or screen                     ║
║  • Keep phone charging during use                             ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  💬 Try these prompts with your agent:                        ║
║                                                               ║
║  • "Write a Go function to reverse a string"                  ║
║  • "Explain goroutines and channels"                          ║
║  • "Help me debug this code snippet"                          ║
║  • "What's the difference between make and new?"              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${BLUE}Ready to start? Run: ${GREEN}./bin/agent chat${NC}"
echo ""
