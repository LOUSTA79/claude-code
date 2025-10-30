# 🤖 Coding Agent App for Samsung S25 Ultra

A powerful AI-powered coding assistant app designed specifically for the Samsung Galaxy S25 Ultra. This Progressive Web App (PWA) provides a complete suite of coding agents directly on your mobile device.

## ✨ Features

### 7 Specialized AI Agents

1. **💬 Chat Agent** - General conversation and coding assistance
2. **📖 Read Agent** - File reading with AI analysis
3. **📁 List Agent** - Directory browsing and navigation
4. **⚡ Bash Agent** - Execute terminal commands safely
5. **✏️ Edit Agent** - File creation and editing
6. **🔍 Search Agent** - Code search across your project
7. **🤖 Generate Agent** - AI-powered code generation

### Mobile-Optimized

- 🎨 Beautiful dark theme optimized for S25 Ultra's display
- 📱 Full PWA support - install like a native app
- 🔊 Voice input support (Web Speech API)
- 📴 Offline support with service worker
- ⚡ Fast and responsive UI
- 🎯 Touch-optimized controls

## 🚀 Quick Start (Termux)

### 1. Installation

```bash
# Navigate to the app directory
cd ~/aic_projects

# Clone or download the app
# (or copy the s25-ultra-agent-app folder to ~/aic_projects/)

cd s25-ultra-agent-app

# Install dependencies
npm install
```

### 2. Configuration

Create a `.env` file in the `server` directory:

```bash
cat > .env << 'EOF'
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4o-mini
PORT=3000
EOF
```

### 3. Start the Server

```bash
# Development mode (auto-restart on changes)
npm run dev

# Or production mode
npm start

# Or with PM2 (recommended for Termux)
npm run pm2:start
```

### 4. Access the App

1. Open your browser on the S25 Ultra
2. Navigate to `http://localhost:3000`
3. Tap the "Install" button when prompted
4. The app will be added to your home screen!

## 📱 Installation as PWA

### On Samsung S25 Ultra (Chrome/Samsung Internet)

1. Open `http://localhost:3000` in your browser
2. Tap the menu (⋮) button
3. Select "Add to Home screen" or "Install app"
4. Tap "Install" or "Add"
5. The app icon will appear on your home screen

### Network Access (WiFi)

To access from other devices on your network:

```bash
# Find your device IP
ifconfig wlan0 | grep inet

# Access from any device on same WiFi
http://192.168.x.x:3000
```

## 🎯 Usage Guide

### Chat Agent

```
1. Select the "💬 Chat" tab
2. Type your question or use voice input (🎤)
3. Press "Send" to get AI-powered responses
4. Conversation history is maintained
```

### Read & Analyze Files

```
1. Select the "📖 Read" tab
2. Enter file path (e.g., /home/user/script.js)
3. Tap "Read & Analyze"
4. View file content + AI analysis
```

### List & Navigate Directories

```
1. Select the "📁 List" tab
2. Enter directory path (default: .)
3. Tap "List Files"
4. Tap any item to navigate or read
```

### Execute Bash Commands

```
1. Select the "⚡ Bash" tab
2. Enter command (e.g., ls -la)
3. Tap "Execute"
4. View output instantly

⚠️ Dangerous commands are blocked for safety
```

### Edit Files

```
1. Select the "✏️ Edit" tab
2. Enter file path
3. Type or paste content
4. Tap "Save File"
```

### Search Code

```
1. Select the "🔍 Search" tab
2. Enter search term
3. Optionally specify path
4. Tap "Search"
5. View all matches with line numbers
```

### Generate Code

```
1. Select the "🤖 Generate" tab
2. Describe what you want to create
3. Choose programming language
4. Tap "Generate"
5. Copy the generated code
```

## 🔧 Advanced Configuration

### PM2 Management

```bash
# Start with PM2
npm run pm2:start

# View logs
npm run pm2:logs

# Restart
npm run pm2:restart

# Stop
npm run pm2:stop

# Make it auto-start on boot
pm2 startup
pm2 save
```

### Custom Port

Edit `.env`:
```
PORT=8080
```

### Different AI Model

Edit `.env`:
```
OPENAI_MODEL=gpt-4-turbo-preview
```

## 📁 Project Structure

```
s25-ultra-agent-app/
├── server/
│   └── index.js          # Express server with all agents
├── public/
│   ├── index.html        # Mobile-optimized UI
│   ├── app.js            # Client-side JavaScript
│   ├── sw.js             # Service worker (offline support)
│   └── manifest.json     # PWA manifest
├── package.json          # Dependencies
├── .env                  # Configuration (create this)
└── README.md            # This file
```

## 🎨 Customization

### Change Theme Colors

Edit `index.html` CSS variables:

```css
:root {
    --primary: #6c5ce7;      /* Purple */
    --secondary: #00b894;    /* Green */
    --danger: #d63031;       /* Red */
    --dark: #1a1a2e;         /* Background */
}
```

### Add Custom Agents

Edit `server/index.js` to add new endpoints:

```javascript
app.post('/api/agent/custom', async (req, res) => {
    // Your custom agent logic
});
```

## 🐛 Troubleshooting

### App won't install

- Make sure you're using HTTPS or localhost
- Try Chrome or Samsung Internet browser
- Clear browser cache and try again

### API Key Error

```bash
# Verify your API key is set
cat .env | grep OPENAI_API_KEY

# Test with curl
curl -X POST http://localhost:3000/api/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

### Port Already in Use

```bash
# Find process using port 3000
lsof -i :3000

# Kill it
kill -9 <PID>

# Or use a different port in .env
```

### Voice Input Not Working

- Voice input requires HTTPS (except on localhost)
- Grant microphone permissions to your browser
- Check if Web Speech API is supported in your browser

## 🔒 Security Notes

- **Local Only**: By default, only accessible on localhost
- **Command Filtering**: Dangerous bash commands are blocked
- **Path Validation**: File operations validate paths to prevent directory traversal
- **API Key**: Keep your `.env` file secure, never commit it

## 📚 API Endpoints

All endpoints accept `POST` requests with JSON body:

| Endpoint | Purpose | Parameters |
|----------|---------|------------|
| `/api/agent/chat` | AI conversation | `{message, history}` |
| `/api/agent/read` | Read file | `{path}` |
| `/api/agent/list` | List directory | `{path}` |
| `/api/agent/bash` | Execute command | `{command, cwd}` |
| `/api/agent/edit` | Edit file | `{path, content, operation}` |
| `/api/agent/search` | Search code | `{query, path, fileType}` |
| `/api/agent/generate` | Generate code | `{prompt, language}` |

## 🚀 Performance Tips

1. **Use PM2** for process management
2. **Enable PWA** for faster loading
3. **Clear chat history** periodically (use "Clear" button)
4. **Limit file sizes** when reading large files
5. **Use specific paths** for faster search

## 🤝 Contributing

Feel free to customize and extend this app for your needs!

## 📄 License

MIT License - Feel free to use and modify

## 🙏 Credits

- Built with Express.js and OpenAI API
- Designed for Samsung Galaxy S25 Ultra
- Optimized for Termux environment

---

**Made with ❤️ for mobile coding**

For issues or questions, check the server logs:
```bash
npm run pm2:logs
```
