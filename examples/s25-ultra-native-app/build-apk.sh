#!/bin/bash

# S25 Ultra Coding Agent - APK Builder for Termux
# This script builds a native Android APK using Cordova

set -e

echo "🤖 S25 Ultra Coding Agent - APK Builder"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if running in Termux
if [ -d "/data/data/com.termux" ]; then
    echo -e "${GREEN}✓${NC} Running in Termux"
else
    echo -e "${YELLOW}⚠${NC}  Not in Termux (but continuing...)"
fi

# Check dependencies
echo ""
echo -e "${BLUE}Checking dependencies...${NC}"

check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 found"
        return 0
    else
        echo -e "${RED}✗${NC} $1 not found"
        return 1
    fi
}

MISSING_DEPS=0

check_command node || MISSING_DEPS=$((MISSING_DEPS + 1))
check_command npm || MISSING_DEPS=$((MISSING_DEPS + 1))

if [ $MISSING_DEPS -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}Installing missing dependencies...${NC}"
    pkg install nodejs -y
fi

# Check for Cordova
if ! command -v cordova &> /dev/null; then
    echo -e "${BLUE}Installing Cordova...${NC}"
    npm install -g cordova
fi

# Check for Java (required for Android build)
if ! command -v java &> /dev/null; then
    echo -e "${YELLOW}⚠${NC}  Java not found. Installing..."
    pkg install openjdk-17 -y
fi

# Initialize Cordova project if needed
if [ ! -d "cordova-app" ]; then
    echo ""
    echo -e "${BLUE}Creating Cordova project...${NC}"
    cordova create cordova-app com.s25.codingagent "S25 Coding Agent"
    cd cordova-app

    # Add Android platform
    echo -e "${BLUE}Adding Android platform...${NC}"
    cordova platform add android

    # Add plugins
    echo -e "${BLUE}Adding plugins...${NC}"
    cordova plugin add cordova-plugin-whitelist
    cordova plugin add cordova-plugin-inappbrowser
    cordova plugin add cordova-plugin-splashscreen

    cd ..
fi

# Copy web app files
echo ""
echo -e "${BLUE}Copying app files...${NC}"
rm -rf cordova-app/www/*
cp -r ../s25-ultra-agent-app/public/* cordova-app/www/
cp -r ../s25-ultra-agent-app/server cordova-app/www/

# Update config.xml
cat > cordova-app/config.xml << 'EOF'
<?xml version='1.0' encoding='utf-8'?>
<widget id="com.s25.codingagent" version="1.0.0" xmlns="http://www.w3.org/ns/widgets" xmlns:cdv="http://cordova.apache.org/ns/1.0">
    <name>S25 Coding Agent</name>
    <description>AI Coding Assistant for Samsung S25 Ultra</description>
    <author email="contact@example.com" href="https://github.com/LOUSTA79/claude-code">
        LOUSTA79
    </author>
    <content src="index.html" />
    <access origin="*" />
    <allow-intent href="http://*/*" />
    <allow-intent href="https://*/*" />
    <allow-intent href="tel:*" />
    <allow-intent href="sms:*" />
    <allow-intent href="mailto:*" />
    <allow-intent href="geo:*" />
    <platform name="android">
        <allow-intent href="market:*" />
        <preference name="android-minSdkVersion" value="24" />
        <preference name="android-targetSdkVersion" value="33" />
        <icon density="ldpi" src="res/icon/android/ldpi.png" />
        <icon density="mdpi" src="res/icon/android/mdpi.png" />
        <icon density="hdpi" src="res/icon/android/hdpi.png" />
        <icon density="xhdpi" src="res/icon/android/xhdpi.png" />
        <icon density="xxhdpi" src="res/icon/android/xxhdpi.png" />
        <icon density="xxxhdpi" src="res/icon/android/xxxhdpi.png" />
    </platform>
    <preference name="Fullscreen" value="false" />
    <preference name="Orientation" value="default" />
    <preference name="SplashScreenDelay" value="1000" />
    <preference name="BackgroundColor" value="0xFF1A1A1A" />
</widget>
EOF

# Build APK
echo ""
echo -e "${BLUE}Building APK...${NC}"
cd cordova-app

# Build debug APK (no signing needed)
cordova build android --debug

echo ""
echo -e "${GREEN}✓${NC} APK built successfully!"
echo ""
echo "APK Location:"
echo "  $(pwd)/platforms/android/app/build/outputs/apk/debug/app-debug.apk"
echo ""
echo -e "${BLUE}To install on your S25 Ultra:${NC}"
echo "  1. Copy APK to your phone"
echo "  2. Enable 'Install from Unknown Sources' in Settings"
echo "  3. Tap the APK file to install"
echo ""

# For release build (requires signing)
echo -e "${YELLOW}Note:${NC} This is a debug APK. For production, you need to sign it."
echo "See: https://cordova.apache.org/docs/en/latest/guide/platforms/android/index.html#signing-an-app"
