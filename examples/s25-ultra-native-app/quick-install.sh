#!/bin/bash

# S25 Ultra Coding Agent - Quick Install for Native App
# Choose your installation method

set -e

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║  📱 S25 ULTRA CODING AGENT - APP INSTALLER              ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}Choose installation method:${NC}"
echo ""
echo "1) Standalone HTML App (Easiest - 30 seconds)"
echo "   ✓ No build needed"
echo "   ✓ Opens in browser"
echo "   ✓ Add to home screen"
echo ""
echo "2) Build APK with Cordova (5-10 minutes)"
echo "   ✓ True native app"
echo "   ✓ Installs like Play Store app"
echo "   ✓ Requires build tools"
echo ""
echo "3) React Native App (Advanced - 20+ minutes)"
echo "   ✓ Best performance"
echo "   ✓ Full native features"
echo "   ✓ Requires Android SDK"
echo ""
echo "4) Just show me the files"
echo ""

read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}Installing Standalone HTML App...${NC}"
        echo ""

        if [ -f "standalone-app.html" ]; then
            echo -e "${GREEN}✓${NC} App file found"

            # Check if termux-open is available
            if command -v termux-open &> /dev/null; then
                echo -e "${GREEN}✓${NC} Opening app in browser..."
                termux-open standalone-app.html
                echo ""
                echo -e "${YELLOW}📱 Next steps:${NC}"
                echo "1. App should open in your browser"
                echo "2. Tap menu (⋮) → 'Add to Home screen'"
                echo "3. Tap 'Add' to install"
                echo "4. Launch from home screen!"
            else
                echo -e "${YELLOW}⚠${NC}  termux-open not available"
                echo ""
                echo "Manual installation:"
                echo "1. Copy this path: $(pwd)/standalone-app.html"
                echo "2. Open in Chrome or Samsung Internet"
                echo "3. Tap menu → 'Add to Home screen'"
            fi
        else
            echo -e "${YELLOW}✗${NC} standalone-app.html not found"
            echo "Run this script from: examples/s25-ultra-native-app/"
        fi
        ;;

    2)
        echo ""
        echo -e "${GREEN}Building APK with Cordova...${NC}"
        echo ""

        if [ -f "build-apk.sh" ]; then
            bash build-apk.sh
        else
            echo -e "${YELLOW}✗${NC} build-apk.sh not found"
        fi
        ;;

    3)
        echo ""
        echo -e "${GREEN}Setting up React Native...${NC}"
        echo ""

        # Check for package.json
        if [ -f "package.json" ]; then
            echo "Installing dependencies..."
            npm install

            echo ""
            echo -e "${YELLOW}Next steps:${NC}"
            echo "1. Set up Android SDK"
            echo "2. Run: npx react-native run-android"
            echo ""
            echo "See: https://reactnative.dev/docs/environment-setup"
        else
            echo -e "${YELLOW}✗${NC} package.json not found"
        fi
        ;;

    4)
        echo ""
        echo -e "${BLUE}App Files:${NC}"
        echo ""
        ls -lh
        echo ""
        echo -e "${BLUE}Quick Access:${NC}"
        echo "• Standalone: $(pwd)/standalone-app.html"
        echo "• APK Builder: $(pwd)/build-apk.sh"
        echo "• README: $(pwd)/README.md"
        ;;

    *)
        echo ""
        echo -e "${YELLOW}Invalid choice. Please run again.${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo "📚 For detailed instructions, see: README.md"
echo "🆘 Need help? Check: ../CODING_AGENTS_GUIDE.md"
echo ""
