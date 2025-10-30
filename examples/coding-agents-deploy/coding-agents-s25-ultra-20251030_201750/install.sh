#!/bin/bash

# Coding Agents Installation Script for Samsung S25 Ultra
# ========================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║  🤖 Coding Agents - Installation                    ║"
echo "║     Samsung Galaxy S25 Ultra Edition                 ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"

INSTALL_DIR="${HOME}/aic_projects/coding-agents"

echo -e "${BLUE}📂 Installation directory: ${INSTALL_DIR}${NC}\n"

# Create installation directory
mkdir -p "$INSTALL_DIR"

# Install JavaScript PWA
if [ -d "javascript-pwa" ]; then
    echo -e "${GREEN}📱 Installing JavaScript PWA...${NC}"
    cp -r javascript-pwa "$INSTALL_DIR/"
    echo -e "${GREEN}✅ JavaScript PWA installed${NC}"
fi

# Install Go CLI
if [ -d "go-cli" ]; then
    echo -e "${GREEN}⚡ Installing Go CLI...${NC}"
    cp -r go-cli "$INSTALL_DIR/"

    # Make binaries executable
    if [ -d "$INSTALL_DIR/go-cli/bin" ]; then
        chmod +x "$INSTALL_DIR/go-cli/bin/"*
    fi

    echo -e "${GREEN}✅ Go CLI installed${NC}"
fi

# Copy documentation and launcher
if [ -f "CODING_AGENTS_GUIDE.md" ]; then
    cp CODING_AGENTS_GUIDE.md "$INSTALL_DIR/"
fi

if [ -f "launch-coding-agent.sh" ]; then
    cp launch-coding-agent.sh "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/launch-coding-agent.sh"
fi

echo -e "\n${GREEN}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║  ✅ Installation Complete!                          ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  Next Steps:                                         ║"
echo "║                                                      ║"
echo "║  1. Configure API Keys:                              ║"
echo "║                                                      ║"
echo "║     JavaScript PWA (OpenAI):                         ║"
echo "║     cd ${INSTALL_DIR}/javascript-pwa"
echo "║     cp .env.example .env"
echo "║     nano .env  # Add OPENAI_API_KEY"
echo "║"
echo "║     Go CLI (Anthropic):                              ║"
echo "║     export ANTHROPIC_API_KEY='your-key'"
echo "║     # Or add to ~/.bashrc"
echo "║"
echo "║  2. Launch:                                          ║"
echo "║     cd ${INSTALL_DIR}"
echo "║     ./launch-coding-agent.sh"
echo "║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"
