#!/bin/bash

# Go Coding Agent Workshop - Build Script
# ========================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║  🤖 Go Coding Agent Workshop - Build                ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Go installation
echo -e "${BLUE}🔍 Checking Go installation...${NC}"
if ! command -v go &> /dev/null; then
    echo -e "${RED}❌ Go not found${NC}"
    echo -e "${YELLOW}Install with: pkg install golang${NC}"
    exit 1
fi

GO_VERSION=$(go version | awk '{print $3}')
echo -e "${GREEN}✅ Go ${GO_VERSION} found${NC}"

# Download dependencies
echo -e "\n${BLUE}📦 Downloading dependencies...${NC}"
go mod tidy

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies downloaded${NC}"
else
    echo -e "${RED}❌ Failed to download dependencies${NC}"
    exit 1
fi

# Create bin directory
mkdir -p bin

# Build
echo -e "\n${BLUE}🔨 Building agent...${NC}"
go build -ldflags="-s -w" -o bin/agent cmd/main.go

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Build successful!${NC}"

    # Show binary info
    SIZE=$(ls -lh bin/agent | awk '{print $5}')
    echo -e "${GREEN}📦 Binary size: ${SIZE}${NC}"
else
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi

# Check API key
echo -e "\n${BLUE}🔑 Checking API key...${NC}"
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  ANTHROPIC_API_KEY not set${NC}"
    echo -e "${YELLOW}Set it with: export ANTHROPIC_API_KEY='your-key'${NC}"
else
    echo -e "${GREEN}✅ API key is set${NC}"
fi

# Success message
echo -e "\n${GREEN}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║  ✅ Build Complete!                                  ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  Run the chat agent:                                 ║"
echo "║    ./bin/agent chat                                  ║"
echo "║                                                      ║"
echo "║  With verbose logging:                               ║"
echo "║    ./bin/agent chat --verbose                        ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"
