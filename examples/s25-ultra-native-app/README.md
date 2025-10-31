# 📱 S25 Ultra Coding Agent - Native Android App

Convert the Coding Agent Suite into a native Android APK that you can install directly on your Samsung Galaxy S25 Ultra.

## 🎯 What You Get

- **Native Android App** - Install from APK file
- **Offline Capable** - Works without constant internet (UI only)
- **Home Screen Icon** - Launch like any other app
- **No Browser Needed** - Standalone application
- **Full Screen** - Optimized for S25 Ultra display

## 📦 Three Ways to Get the App

### Option 1: Use the Standalone HTML App (Easiest)

The simplest way - just open the HTML file in your browser:

```bash
# On S25 Ultra in Termux
cd ~/claude-code/examples/s25-ultra-native-app
termux-open standalone-app.html
```

Then save to home screen:
1. Open in Chrome/Samsung Internet
2. Tap menu (⋮)
3. Select "Add to Home screen"
4. Done! Launch from home screen like an app

### Option 2: Build APK with Cordova (Recommended)

Build a real APK file you can install:

```bash
# On S25 Ultra in Termux
cd ~/claude-code/examples/s25-ultra-native-app
bash build-apk.sh
```

The script will:
- Install dependencies (Cordova, Java)
- Create Android project
- Build APK file
- Output: `cordova-app/platforms/android/app/build/outputs/apk/debug/app-debug.apk`

Then install the APK:
```bash
# Copy APK to accessible location
cp cordova-app/platforms/android/app/build/outputs/apk/debug/app-debug.apk ~/storage/downloads/

# Install via file manager or:
termux-open ~/storage/downloads/app-debug.apk
```

### Option 3: Use React Native (Advanced)

For a fully native experience:

```bash
cd ~/claude-code/examples/s25-ultra-native-app
npm install
npx react-native run-android
```

**Requirements**:
- Android SDK
- React Native CLI
- More setup required

## 🔧 What's Included

### Standalone App Features

✅ **Chat Agent** - AI-powered coding assistant
✅ **Read Agent** - File analysis
✅ **Bash Agent** - Command execution (simulation)
✅ **Edit Agent** - File editing
✅ **Search Agent** - Code search
✅ **Settings** - API key management

### Mobile Optimizations

✅ Touch-friendly interface
✅ Dark theme for AMOLED
✅ Full screen mode
✅ Responsive design
✅ Local storage for settings

## 🔑 API Keys Setup

The app needs API keys to work with AI models:

1. **Open the app**
2. **Go to Settings tab**
3. **Enter your API keys**:
   - OpenAI: Get from https://platform.openai.com/api-keys
   - Anthropic: Get from https://console.anthropic.com/settings/keys
4. **Click Save**

Keys are stored locally on your device.

## 📋 Building APK - Detailed Steps

### Prerequisites

```bash
# Install dependencies in Termux
pkg update
pkg install nodejs git openjdk-17 -y

# Install Cordova
npm install -g cordova
```

### Build Process

```bash
# 1. Navigate to app directory
cd ~/claude-code/examples/s25-ultra-native-app

# 2. Run build script
bash build-apk.sh

# 3. Wait for build to complete
# Output: cordova-app/platforms/android/app/build/outputs/apk/debug/app-debug.apk

# 4. Install APK
termux-open cordova-app/platforms/android/app/build/outputs/apk/debug/app-debug.apk
```

## 🐛 Troubleshooting

### Build Fails

**Issue**: Java not found
```bash
pkg install openjdk-17 -y
export JAVA_HOME=/data/data/com.termux/files/usr
```

**Issue**: Cordova not found
```bash
npm install -g cordova
```

**Issue**: Android SDK missing
```bash
# For full React Native builds, you need Android SDK
# Cordova build should work without it
```

### App Won't Install

**Issue**: "Unknown sources blocked"
1. Go to Settings → Security
2. Enable "Install unknown apps"
3. Allow for your file manager

**Issue**: "Parse error"
- APK may be corrupted
- Rebuild using `bash build-apk.sh`

### API Not Working

**Issue**: "API key invalid"
- Check you copied the full key
- Make sure key starts with `sk-` (OpenAI) or `sk-ant-` (Anthropic)
- Verify key at platform dashboard

**Issue**: "Network error"
- Check internet connection
- Some features need backend server running

## 🔄 Full App vs Standalone

### Standalone HTML App
✅ Instant - no build needed
✅ Works in any browser
✅ Can add to home screen
❌ Limited functionality (no backend)
❌ Requires browser

### Full APK (Cordova)
✅ True native app
✅ Installs like Play Store app
✅ Home screen icon
✅ Can bundle backend (with Node.js)
❌ Requires build process
❌ Larger file size

### Full React Native
✅ Best performance
✅ Full native features
✅ Professional app experience
❌ Complex build process
❌ Requires Android SDK
❌ Longer development time

## 📊 File Sizes

| Version | Size | Build Time |
|---------|------|------------|
| Standalone HTML | 30 KB | Instant |
| Cordova APK (debug) | ~5 MB | 2-5 min |
| Cordova APK (release) | ~3 MB | 3-7 min |
| React Native APK | ~20 MB | 10-20 min |

## 🚀 Next Steps

After installing the app:

1. **Configure API Keys** in Settings
2. **Test Chat Agent** with a simple question
3. **Try Other Agents** (Read, Bash, Edit, Search)
4. **Star the Repo** if you find it useful! 🌟

## 📚 Additional Resources

- **Main Guide**: `../CODING_AGENTS_GUIDE.md`
- **Video Tutorial**: `../VIDEO_TUTORIAL_SCRIPT.md`
- **Test Script**: `../test-on-s25.sh`

## 🆘 Support

- Check the main guide for troubleshooting
- GitHub Issues: https://github.com/LOUSTA79/claude-code/issues
- Make sure you're on the correct branch: `claude/fix-openai-initialization-011CUd3Gm4cr5swWrQBYjFyE`

---

**Built for Samsung Galaxy S25 Ultra** 📱
**Optimized for Termux on Android** 🤖
