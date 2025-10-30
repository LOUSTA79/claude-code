#!/bin/bash

# Deployment Script for Coding Agents
# ====================================
# Package both JavaScript PWA and Go CLI for distribution

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║  📦 Coding Agents - Deployment Packager             ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Configuration
DEPLOY_DIR="coding-agents-deploy"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PACKAGE_NAME="coding-agents-s25-ultra-${TIMESTAMP}"

# Clean previous deployments
if [ -d "$DEPLOY_DIR" ]; then
    echo -e "${YELLOW}🧹 Cleaning previous deployment...${NC}"
    rm -rf "$DEPLOY_DIR"
fi

# Create deployment directory
echo -e "${BLUE}📁 Creating deployment directory...${NC}"
mkdir -p "$DEPLOY_DIR/$PACKAGE_NAME"
cd "$DEPLOY_DIR/$PACKAGE_NAME"

# ============================================================================
# Package JavaScript PWA
# ============================================================================

echo -e "\n${BLUE}📱 Packaging JavaScript PWA...${NC}"

if [ -d "../../s25-ultra-agent-app" ]; then
    mkdir -p javascript-pwa
    cp -r ../../s25-ultra-agent-app/* javascript-pwa/

    # Remove sensitive files
    rm -f javascript-pwa/.env
    rm -rf javascript-pwa/node_modules
    rm -rf javascript-pwa/.git

    # Create package.json if missing
    if [ ! -f "javascript-pwa/package.json" ]; then
        echo -e "${YELLOW}⚠️  package.json not found, creating...${NC}"
    fi

    echo -e "${GREEN}✅ JavaScript PWA packaged${NC}"
else
    echo -e "${RED}❌ JavaScript PWA not found${NC}"
fi

# ============================================================================
# Package Go CLI
# ============================================================================

echo -e "\n${BLUE}⚡ Packaging Go CLI...${NC}"

if [ -d "../../go-coding-agent-workshop" ]; then
    mkdir -p go-cli
    cp -r ../../go-coding-agent-workshop/* go-cli/

    # Remove build artifacts
    rm -rf go-cli/bin
    rm -rf go-cli/.git

    # Build for multiple architectures if possible
    if command -v go &> /dev/null; then
        echo -e "${BLUE}🔨 Building Go binaries...${NC}"

        cd go-cli
        mkdir -p bin

        # Build for Android ARM64 (Termux)
        echo -e "${YELLOW}  Building for ARM64...${NC}"
        GOOS=linux GOARCH=arm64 go build -ldflags="-s -w" -o bin/agent-arm64 cmd/main.go

        # Build for AMD64 (PC)
        echo -e "${YELLOW}  Building for AMD64...${NC}"
        GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o bin/agent-amd64 cmd/main.go

        echo -e "${GREEN}✅ Binaries built${NC}"
        cd ..
    else
        echo -e "${YELLOW}⚠️  Go not available, skipping binary builds${NC}"
    fi

    echo -e "${GREEN}✅ Go CLI packaged${NC}"
else
    echo -e "${RED}❌ Go CLI not found${NC}"
fi

# ============================================================================
# Copy Documentation
# ============================================================================

echo -e "\n${BLUE}📚 Copying documentation...${NC}"

if [ -f "../../CODING_AGENTS_GUIDE.md" ]; then
    cp ../../CODING_AGENTS_GUIDE.md ./
    echo -e "${GREEN}✅ Guide copied${NC}"
fi

if [ -f "../../launch-coding-agent.sh" ]; then
    cp ../../launch-coding-agent.sh ./
    chmod +x launch-coding-agent.sh
    echo -e "${GREEN}✅ Launcher copied${NC}"
fi

# ============================================================================
# Create Installation Script
# ============================================================================

echo -e "\n${BLUE}📝 Creating installation script...${NC}"

cat > install.sh << 'INSTALL_SCRIPT'
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
INSTALL_SCRIPT

chmod +x install.sh
echo -e "${GREEN}✅ Installation script created${NC}"

# ============================================================================
# Create README
# ============================================================================

echo -e "\n${BLUE}📝 Creating README...${NC}"

cat > README.md << 'README'
# 🤖 Coding Agents for Samsung S25 Ultra

Complete AI coding agent systems for mobile development.

## 📦 What's Included

### JavaScript PWA
- 7 AI agents (Chat, Read, List, Bash, Edit, Search, Generate)
- Beautiful mobile UI
- Installable as home screen app
- Voice input support

### Go CLI
- 6 AI agents (Chat, Read, List, Bash, Edit, Search)
- Native compiled binary
- Lightning fast startup
- Low memory usage

## 🚀 Quick Install

```bash
# Extract the package
unzip coding-agents-*.zip
cd coding-agents-*

# Run installer
bash install.sh

# Follow the instructions to configure API keys
```

## 📚 Documentation

See `CODING_AGENTS_GUIDE.md` for complete documentation.

## 🔑 API Keys Required

- **JavaScript PWA**: OpenAI API key (get from https://platform.openai.com/)
- **Go CLI**: Anthropic API key (get from https://console.anthropic.com/)

## 🆘 Support

For issues or questions, check the troubleshooting section in the guide.

---

Built for Samsung Galaxy S25 Ultra with Termux
README

echo -e "${GREEN}✅ README created${NC}"

# ============================================================================
# Create Archive
# ============================================================================

cd ..

echo -e "\n${BLUE}📦 Creating archive...${NC}"

# Create tar.gz
tar -czf "${PACKAGE_NAME}.tar.gz" "$PACKAGE_NAME"
echo -e "${GREEN}✅ Created ${PACKAGE_NAME}.tar.gz${NC}"

# Create zip
zip -r -q "${PACKAGE_NAME}.zip" "$PACKAGE_NAME"
echo -e "${GREEN}✅ Created ${PACKAGE_NAME}.zip${NC}"

# Show results
echo -e "\n${GREEN}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║  ✅ Deployment Complete!                            ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  Packages created:                                   ║"
echo "║"
du -h "${PACKAGE_NAME}.tar.gz" | awk '{printf "║  📦 %s (tar.gz)\n", $0}'
du -h "${PACKAGE_NAME}.zip" | awk '{printf "║  📦 %s (zip)\n", $0}'
echo "║"
echo "║  Location: $(pwd)"
echo "║"
echo "║  Distribution ready!                                 ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${CYAN}📤 To distribute:${NC}"
echo "   1. Upload to GitHub releases"
echo "   2. Share via USB/Bluetooth"
echo "   3. Host on web server"
echo ""
echo -e "${CYAN}🎯 Recipients can:${NC}"
echo "   1. Extract the archive"
echo "   2. Run bash install.sh"
echo "   3. Configure API keys"
echo "   4. Start coding with AI!"
echo ""
