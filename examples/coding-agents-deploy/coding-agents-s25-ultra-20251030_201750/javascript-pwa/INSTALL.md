# 📱 Installation Guide - Samsung S25 Ultra

## Quick Install (Termux - Recommended)

### Step 1: Get the App

```bash
# If you're in ~/aic_projects
cd ~/aic_projects

# Download/copy the s25-ultra-agent-app folder here
# Or clone from repository
```

### Step 2: Run Setup

```bash
cd s25-ultra-agent-app
bash setup.sh
```

The setup script will:
- ✅ Check Node.js and npm
- ✅ Create .env configuration
- ✅ Install dependencies
- ✅ Install PM2 process manager
- ✅ Test the server
- ✅ Display your local IP

### Step 3: Start the Server

```bash
# Option 1: Simple start
npm start

# Option 2: With PM2 (recommended)
npm run pm2:start

# Option 3: Development mode (auto-reload)
npm run dev
```

### Step 4: Install on Your S25 Ultra

1. **Open Browser**
   - Open Chrome or Samsung Internet
   - Navigate to `http://localhost:3000`

2. **Install as App**
   - Tap the menu button (⋮)
   - Select "Add to Home screen" or "Install app"
   - Tap "Install" or "Add"
   - Name it "Coding Agent"

3. **Launch**
   - Find the "Coding Agent" icon on your home screen
   - Tap to launch
   - Enjoy native-like experience!

## Manual Installation

If the setup script doesn't work, follow these manual steps:

### 1. Install Dependencies

```bash
cd s25-ultra-agent-app
npm install
```

### 2. Create Configuration

```bash
cat > .env << 'EOF'
OPENAI_API_KEY=sk-proj-your-actual-key-here
OPENAI_MODEL=gpt-4o-mini
PORT=3000
EOF
```

### 3. Start Server

```bash
node server/index.js
```

## Troubleshooting

### "Node.js not found"

Install Node.js in Termux:

```bash
pkg update
pkg install nodejs
```

### "Cannot find module 'express'"

Install dependencies:

```bash
npm install
```

### "Port 3000 already in use"

Change the port in `.env`:

```bash
echo "PORT=8080" >> .env
```

Or kill the process using port 3000:

```bash
# Find the process
lsof -i :3000

# Kill it (replace PID with actual process ID)
kill -9 <PID>
```

### "API Key Invalid"

1. Check your OpenAI API key at https://platform.openai.com/api-keys
2. Update `.env` with the correct key:
   ```bash
   nano .env
   # Change OPENAI_API_KEY=your-key-here
   ```
3. Restart the server

### "Can't install PWA"

PWAs require:
- HTTPS or localhost
- A valid manifest.json
- A service worker

Try:
1. Clear browser cache
2. Use Chrome or Samsung Internet
3. Make sure you're on `localhost:3000`

### Voice Input Not Working

1. Grant microphone permissions:
   - Settings → Apps → Chrome/Samsung Internet → Permissions → Microphone
2. Make sure you're on localhost (HTTPS not required for localhost)
3. Tap the 🎤 button and allow microphone access when prompted

## Network Access (Other Devices)

To access from other devices on WiFi:

```bash
# Find your IP address
ifconfig wlan0 | grep inet

# Example output: inet 192.168.1.100

# Access from any device on same WiFi:
http://192.168.1.100:3000
```

## Auto-Start on Boot

To make the server start automatically when Termux launches:

```bash
# Install PM2
npm install -g pm2

# Start your app
npm run pm2:start

# Generate startup script
pm2 startup

# Save current process list
pm2 save
```

Add this to `~/.bashrc`:

```bash
echo "pm2 resurrect" >> ~/.bashrc
```

## Uninstallation

### Remove from Home Screen

1. Long-press the app icon
2. Select "Uninstall" or "Remove"

### Remove from Termux

```bash
# Stop the server
npm run pm2:stop

# Remove PM2 process
pm2 delete coding-agent

# Delete the app folder
cd ~/aic_projects
rm -rf s25-ultra-agent-app
```

## Advanced Configuration

### Using a Different AI Model

Edit `.env`:

```bash
OPENAI_MODEL=gpt-4-turbo-preview
# or
OPENAI_MODEL=gpt-3.5-turbo
```

### Increase Response Length

Edit `server/index.js`, find `max_tokens` and increase the value:

```javascript
max_tokens: 2000  // Default is 1000
```

### Add Custom Agents

1. Open `server/index.js`
2. Add a new endpoint:

```javascript
app.post('/api/agent/myagent', async (req, res) => {
  // Your custom logic here
});
```

3. Update `public/index.html` to add UI
4. Update `public/app.js` to add client logic

### Enable Debug Logging

Start with verbose output:

```bash
DEBUG=* node server/index.js
```

Or check PM2 logs:

```bash
npm run pm2:logs
```

## System Requirements

- **Device**: Samsung Galaxy S25 Ultra (or any Android device)
- **OS**: Android with Termux installed
- **Node.js**: v18.0.0 or higher
- **RAM**: At least 200MB free
- **Storage**: 50MB for app + dependencies
- **Network**: Internet connection for API calls

## Performance Tips

1. **Use PM2** - Better memory management
2. **Clear cache** - Periodically clear browser cache
3. **Limit history** - Chat history is kept in memory
4. **Close tabs** - Close other heavy browser tabs
5. **WiFi** - Use WiFi instead of mobile data for faster responses

## Security Considerations

- ✅ Server runs locally (localhost only by default)
- ✅ Dangerous bash commands are blocked
- ✅ File operations validate paths
- ⚠️ Keep your `.env` file secure
- ⚠️ Don't expose your API key
- ⚠️ Be careful with bash agent

## Getting Help

1. **Check logs**:
   ```bash
   npm run pm2:logs
   ```

2. **Test server**:
   ```bash
   curl http://localhost:3000/health
   ```

3. **Verify API key**:
   ```bash
   curl -X POST http://localhost:3000/api/agent/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "test"}'
   ```

4. **Check the README.md** for detailed usage instructions

## What's Next?

After installation:

1. **Explore all 7 agents** - Try each tab to see what they can do
2. **Use voice input** - Tap the 🎤 button for hands-free coding
3. **Generate code** - Ask the AI to write code for you
4. **Automate tasks** - Use bash agent to run commands
5. **Customize** - Modify the app to fit your workflow

Enjoy coding on your S25 Ultra! 🚀
