# 📱 Quick Access Guide - Finding Your Coding Agent App

## Current Location

The app is currently in this repository at:
```
/home/user/claude-code/examples/s25-ultra-agent-app/
```

## 🚀 Access It in 3 Easy Steps

### Step 1: Navigate to the App

```bash
cd /home/user/claude-code/examples/s25-ultra-agent-app
```

### Step 2: Run Setup

```bash
bash setup.sh
```

### Step 3: Start the Server

```bash
npm start
```

Then open your browser on S25 Ultra and go to: **http://localhost:3000**

---

## 📂 Alternative: Copy to Your aic_projects Folder

If you want the app in your `~/aic_projects` directory:

```bash
# From the claude-code directory
cp -r examples/s25-ultra-agent-app ~/aic_projects/

# Then navigate there
cd ~/aic_projects/s25-ultra-agent-app

# Run setup
bash setup.sh

# Start the server
npm start
```

---

## 🗂️ What's Inside

```
s25-ultra-agent-app/
├── server/
│   └── index.js          ← Backend server (Express + OpenAI)
├── public/
│   ├── index.html        ← Mobile UI
│   ├── app.js            ← Client JavaScript
│   ├── sw.js             ← Service Worker (PWA)
│   └── manifest.json     ← App Manifest
├── setup.sh              ← Automated setup script
├── package.json          ← Dependencies
├── README.md             ← Full documentation
└── INSTALL.md            ← Installation guide

```

---

## ⚡ Quick Test

Check if the files are there:

```bash
ls -l /home/user/claude-code/examples/s25-ultra-agent-app/
```

You should see:
- ✅ server/
- ✅ public/
- ✅ setup.sh
- ✅ package.json
- ✅ README.md

---

## 🎯 One-Line Install

```bash
cd /home/user/claude-code/examples/s25-ultra-agent-app && bash setup.sh && npm start
```

That's it! Open http://localhost:3000 on your S25 Ultra browser.

---

## 🆘 Troubleshooting

**Can't find the directory?**
```bash
# Search for it
find ~ -name "s25-ultra-agent-app" -type d 2>/dev/null
```

**Want to see all files in the app?**
```bash
cd /home/user/claude-code/examples/s25-ultra-agent-app
tree
# or
find . -type f
```

**Need to check if it's working?**
```bash
cd /home/user/claude-code/examples/s25-ultra-agent-app
ls -la setup.sh  # Should show executable permissions
cat package.json  # Should show dependencies
```

---

## 📱 GitHub Access

The app is also available on GitHub in your repository:
- **Repo**: LOUSTA79/claude-code
- **Branch**: claude/fix-openai-initialization-011CUd3Gm4cr5swWrQBYjFyE
- **Path**: examples/s25-ultra-agent-app/

You can clone it anywhere:
```bash
git clone -b claude/fix-openai-initialization-011CUd3Gm4cr5swWrQBYjFyE \
  https://github.com/LOUSTA79/claude-code.git
```

---

## 🎉 Ready to Launch!

**Absolute path to your app:**
```
/home/user/claude-code/examples/s25-ultra-agent-app/
```

**Go there now:**
```bash
cd /home/user/claude-code/examples/s25-ultra-agent-app
```

**Start it:**
```bash
bash setup.sh
```

Enjoy your AI coding assistant on your S25 Ultra! 🚀
