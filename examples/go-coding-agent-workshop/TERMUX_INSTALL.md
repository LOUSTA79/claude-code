# 📱 Termux Installation Guide

Complete guide for installing and running the Go Coding Agent Workshop on your Samsung Galaxy S25 Ultra using Termux.

## 🚀 Quick Install (Recommended)

```bash
# 1. Copy the project to your phone
cd ~/aic_projects
git clone -b claude/fix-openai-initialization-011CUd3Gm4cr5swWrQBYjFyE \
  https://github.com/LOUSTA79/claude-code.git
cp -r claude-code/examples/go-coding-agent-workshop .
cd go-coding-agent-workshop

# 2. Run the quick start script
bash quickstart.sh

# 3. Start chatting with Claude!
./bin/agent chat
```

That's it! The quickstart script will:
- ✅ Install Go (if needed)
- ✅ Ask for your API key
- ✅ Build the agent
- ✅ Test everything
- ✅ Show you how to use it

## 📋 Prerequisites

### 1. Install Termux

Download from [F-Droid](https://f-droid.org/packages/com.termux/):
- Don't use Google Play version (outdated)
- F-Droid version is official and up-to-date

### 2. Initial Termux Setup

```bash
# Update packages
pkg update && pkg upgrade

# Install essential tools
pkg install git curl wget

# Grant storage access (optional, for file operations)
termux-setup-storage
```

### 3. Install Go

```bash
# Install Go
pkg install golang

# Verify installation
go version
# Should show: go version go1.21.x linux/arm64
```

### 4. Get Anthropic API Key

1. Visit https://console.anthropic.com/
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-ant-api03-...`)

## 🛠️ Manual Installation

If you prefer manual installation or the quickstart script fails:

### Step 1: Copy the Project

```bash
# Create projects directory
mkdir -p ~/aic_projects
cd ~/aic_projects

# Option A: Clone from GitHub
git clone -b claude/fix-openai-initialization-011CUd3Gm4cr5swWrQBYjFyE \
  https://github.com/LOUSTA79/claude-code.git
cp -r claude-code/examples/go-coding-agent-workshop .

# Option B: Download as ZIP and extract
# (If you downloaded manually)
cd ~/storage/downloads
unzip go-coding-agent-workshop.zip -d ~/aic_projects/

cd ~/aic_projects/go-coding-agent-workshop
```

### Step 2: Set API Key

```bash
# Temporary (current session only)
export ANTHROPIC_API_KEY="sk-ant-api03-your-full-key-here"

# Permanent (recommended)
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-your-full-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Step 3: Download Dependencies

```bash
go mod tidy
```

You should see:
```
go: downloading github.com/spf13/cobra v1.8.0
go: downloading github.com/spf13/pflag v1.0.5
...
```

### Step 4: Build

```bash
# Create bin directory
mkdir -p bin

# Build the agent
go build -o bin/agent cmd/main.go

# Verify it works
./bin/agent --help
```

### Step 5: Run

```bash
./bin/agent chat
```

## 💬 Usage Examples

### Basic Chat

```bash
./bin/agent chat
```

Example session:
```
ℹ️  Starting chat agent...
ℹ️  🤖 Chat Agent started!
ℹ️  💬 Type your messages and press Enter
ℹ️  🚪 Type 'exit' to quit

You: Write a Go function to check if a number is prime

🤖 Claude: Here's a Go function that checks if a number is prime:

```go
func isPrime(n int) bool {
    if n <= 1 {
        return false
    }
    if n <= 3 {
        return true
    }
    if n%2 == 0 || n%3 == 0 {
        return false
    }
    for i := 5; i*i <= n; i += 6 {
        if n%i == 0 || n%(i+2) == 0 {
            return false
        }
    }
    return true
}
```

This function efficiently checks primality by...
[continues...]

You: exit
👋 Goodbye!
```

### Verbose Mode

```bash
./bin/agent chat --verbose
```

Shows debug information:
```
ℹ️  Starting chat agent...
🐛 Using API key: sk-ant-api03-***************
ℹ️  🤖 Chat Agent started!
...
🐛 Sending message: Hello
🐛 API response received: 249 bytes
...
```

### Custom API Key

```bash
./bin/agent chat --api-key="sk-ant-api03-different-key"
```

## 🔧 Troubleshooting

### Go Not Found

```bash
# Check if installed
which go

# If not found, install
pkg install golang

# Add to PATH (if needed)
export PATH=$PATH:/data/data/com.termux/files/usr/lib/go/bin
echo 'export PATH=$PATH:/data/data/com.termux/files/usr/lib/go/bin' >> ~/.bashrc
```

### Build Errors

```bash
# Clean everything
go clean
rm -rf bin/
rm go.sum

# Re-download dependencies
go mod tidy

# Try building again
go build -o bin/agent cmd/main.go
```

### API Key Issues

```bash
# Check if set
echo $ANTHROPIC_API_KEY

# If empty or wrong, set it again
export ANTHROPIC_API_KEY="sk-ant-api03-your-correct-key"

# Verify it's a valid format (should start with sk-ant-api03-)
```

### Permission Denied

```bash
# Make scripts executable
chmod +x *.sh
chmod +x bin/agent

# Run again
./bin/agent chat
```

### API Error 401 (Unauthorized)

Your API key is invalid:
1. Check for extra spaces or quotes
2. Verify at https://console.anthropic.com/
3. Generate a new key if needed

### API Error 429 (Rate Limited)

You've exceeded your rate limit:
1. Wait a few minutes
2. Check your plan at https://console.anthropic.com/
3. Upgrade if needed

### Connection Errors

```bash
# Check internet connection
ping -c 3 api.anthropic.com

# If using VPN, try disabling it
# Try on WiFi instead of mobile data
```

## 📱 Mobile Tips

### Keep Phone Active

```bash
# Prevent sleep during builds/runs
termux-wake-lock

# Release when done
termux-wake-unlock
```

### Run in Background

```bash
# Install tmux
pkg install tmux

# Start session
tmux new -s agent

# Run your agent
./bin/agent chat

# Detach: Press Ctrl+B, then D
# Phone can sleep, agent keeps running

# Later, reattach:
tmux attach -s agent

# List sessions:
tmux ls
```

### Save Battery

```bash
# Build once, run many times
go build -ldflags="-s -w" -o bin/agent cmd/main.go

# The -ldflags="-s -w" reduces binary size
# Smaller binary = less memory = less battery usage
```

### Storage Management

```bash
# Check sizes
du -sh ~/aic_projects/go-coding-agent-workshop
du -sh ~/aic_projects/go-coding-agent-workshop/bin/agent

# Clean up (if needed)
rm -rf ~/go/pkg/mod/cache  # Go module cache
go clean -cache            # Build cache
```

## 🎯 Performance

### Build Time

On Samsung S25 Ultra:
- First build (with downloads): ~30-60 seconds
- Subsequent builds: ~5-10 seconds

### Binary Size

- Without optimization: ~8-10 MB
- With `-ldflags="-s -w"`: ~6-7 MB

### Memory Usage

- Idle: ~10-15 MB
- During API call: ~20-30 MB

### Battery Impact

- Minimal when idle
- Low during normal use
- Moderate during heavy API usage

## 🔄 Updates

### Update Go Version

```bash
pkg upgrade golang
go version
```

### Update Dependencies

```bash
cd ~/aic_projects/go-coding-agent-workshop
go get -u ./...
go mod tidy
```

### Update Project

```bash
cd ~/aic_projects
git clone -b latest-branch https://github.com/LOUSTA79/claude-code.git
cp -r claude-code/examples/go-coding-agent-workshop .
```

## 🆘 Getting Help

### Check Logs

```bash
# Run with verbose mode
./bin/agent chat --verbose 2>&1 | tee debug.log

# View log
cat debug.log
```

### Test API Connection

```bash
# Test with curl
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-3-sonnet-20240229",
    "max_tokens": 10,
    "messages": [{"role": "user", "content": "Hi"}]
  }'
```

### System Info

```bash
# Phone info
uname -a

# Go info
go version
go env

# Termux info
pkg list-installed | grep golang
```

## 🎉 What's Next?

After successful installation:

1. **Try the examples** in the README.md
2. **Explore the code** in `internal/` directories
3. **Add new agents** following the guide
4. **Customize** the prompts and behavior
5. **Share** your creations!

## 📚 Additional Resources

- [Go Documentation](https://go.dev/doc/)
- [Anthropic API Docs](https://docs.anthropic.com/)
- [Termux Wiki](https://wiki.termux.com/)
- [Cobra CLI Framework](https://cobra.dev/)

---

**Happy Coding on Your S25 Ultra! 🚀📱**

Need help? Check the README.md or open an issue on GitHub.
