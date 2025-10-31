# 📱 Installation Guide - S25 Ultra Coding Agent App

**3 simple ways to install the app on your Samsung Galaxy S25 Ultra**

---

## 🚀 Method 1: Standalone HTML App (EASIEST - 2 minutes)

**Best for**: Quick setup, no build tools needed

### Steps:

1. **Open Termux** on your S25 Ultra

2. **Clone the repository**:
   ```bash
   git clone https://github.com/LOUSTA79/claude-code.git
   cd claude-code
   git checkout claude/fix-openai-initialization-011CUd3Gm4cr5swWrQBYjFyE
   ```

3. **Navigate to app directory**:
   ```bash
   cd examples/s25-ultra-native-app
   ```

4. **Open the app**:
   ```bash
   termux-open standalone-app.html
   ```

5. **Add to Home Screen**:
   - App opens in your browser
   - Tap menu button (⋮)
   - Select "Add to Home screen"
   - Tap "Add"
   - Done! 🎉

6. **Configure API Keys**:
   - Open app from home screen
   - Go to Settings tab
   - Enter your OpenAI API key
   - Save

### What You Get:
✅ Works immediately
✅ No build process
✅ ~30 KB size
✅ Launches from home screen
❌ Runs in browser (not true native app)

---

## 📦 Method 2: Build Native APK (RECOMMENDED - 10 minutes)

**Best for**: True native app experience

### Steps:

1. **Follow steps 1-3 from Method 1** (clone and navigate)

2. **Run the installer**:
   ```bash
   bash quick-install.sh
   ```

3. **Choose Option 2** (Build APK with Cordova)

4. **Wait for build** (~5-10 minutes):
   - Script installs dependencies
   - Creates Cordova project
   - Builds APK file

5. **Install the APK**:
   ```bash
   # APK will be at:
   # cordova-app/platforms/android/app/build/outputs/apk/debug/app-debug.apk

   # Install it:
   termux-open cordova-app/platforms/android/app/build/outputs/apk/debug/app-debug.apk
   ```

6. **Allow installation**:
   - Enable "Install unknown apps" if prompted
   - Tap "Install"
   - Tap "Open"

7. **Configure and use**!

### What You Get:
✅ True native Android app
✅ Installs like Play Store apps
✅ Home screen icon
✅ ~5 MB size
✅ Better performance
❌ Requires build process

---

## ⚡ Method 3: Use Without Installing (INSTANT)

**Best for**: Just want to try it

### Steps:

1. **Clone repository** (steps 1-3 from Method 1)

2. **Open in browser**:
   ```bash
   cd examples/s25-ultra-native-app
   python3 -m http.server 8080
   ```

3. **Access in browser**:
   - Open Chrome/Samsung Internet
   - Go to: `http://localhost:8080/standalone-app.html`

4. **Use immediately** - no installation needed!

### What You Get:
✅ Instant access
✅ No installation
❌ Must keep terminal open
❌ Not on home screen

---

## 🔑 Setting Up API Keys

**All methods require API keys to work:**

### Get Your Keys:

1. **OpenAI** (for Chat agent):
   - Visit: https://platform.openai.com/api-keys
   - Sign up (free $5 credits for new accounts)
   - Create new API key
   - Copy the key (starts with `sk-...`)

2. **Anthropic** (optional, for advanced features):
   - Visit: https://console.anthropic.com/settings/keys
   - Sign up (limited free tier)
   - Create new API key
   - Copy the key (starts with `sk-ant-...`)

### Add Keys to App:

1. Open the app
2. Go to **Settings** tab (⚙️)
3. Paste your OpenAI key
4. (Optional) Paste your Anthropic key
5. Tap **Save**

Keys are stored securely on your device only.

---

## ✅ Verification

**Test that everything works:**

1. **Open the app**
2. **Go to Chat tab** (💬)
3. **Type**: "Hello, can you explain what async/await does in JavaScript?"
4. **Tap Send**
5. **You should see**: AI response explaining async/await

If you see a response, it's working! 🎉

---

## 🐛 Troubleshooting

### App Won't Open

**Issue**: "File not found"
```bash
# Make sure you're in the right directory:
pwd
# Should show: /data/data/com.termux/files/home/claude-code/examples/s25-ultra-native-app
```

**Issue**: Browser doesn't open
```bash
# Install termux-open:
pkg install termux-api -y
```

### Build Fails

**Issue**: "Cordova not found"
```bash
npm install -g cordova
```

**Issue**: "Java not found"
```bash
pkg install openjdk-17 -y
```

### API Key Errors

**Issue**: "Invalid API key"
- Check you copied the full key
- Make sure there are no spaces
- Key should start with `sk-` (OpenAI) or `sk-ant-` (Anthropic)

**Issue**: "API quota exceeded"
- You've used your free credits
- Check usage at platform dashboard
- Add payment method or wait for reset

### APK Won't Install

**Issue**: "Unknown sources blocked"
1. Go to **Settings** → **Security**
2. Enable "**Install unknown apps**"
3. Allow for your file manager

**Issue**: "Parse error"
- APK may be corrupted
- Rebuild: `bash quick-install.sh` → Option 2

---

## 📊 Comparison

| Feature | Method 1 (HTML) | Method 2 (APK) | Method 3 (Server) |
|---------|----------------|----------------|-------------------|
| **Setup Time** | 2 min | 10 min | 1 min |
| **File Size** | 30 KB | 5 MB | N/A |
| **Performance** | Good | Excellent | Good |
| **Home Screen** | ✅ Yes | ✅ Yes | ❌ No |
| **Offline** | Partial | Partial | ❌ No |
| **Build Needed** | ❌ No | ✅ Yes | ❌ No |
| **Native Feel** | Good | Excellent | Basic |

**Recommendation**: Start with Method 1, upgrade to Method 2 if you like it!

---

## 🎯 Next Steps

After installation:

1. ✅ Test all agents (Chat, Read, Bash, Edit, Search)
2. ✅ Check out the full documentation: `../CODING_AGENTS_GUIDE.md`
3. ✅ Try the Go CLI version: `../go-coding-agent-workshop/`
4. ✅ Star the repo if useful! ⭐

---

## 🆘 Need Help?

- **Full Guide**: `README.md` (in same folder)
- **Main Docs**: `../CODING_AGENTS_GUIDE.md`
- **GitHub Issues**: https://github.com/LOUSTA79/claude-code/issues
- **Quick Test**: `../test-on-s25.sh`

---

**Happy Coding on Your S25 Ultra!** 🚀📱
