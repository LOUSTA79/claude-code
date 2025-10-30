# 🤖 Go Coding Agent Workshop

Build AI-powered coding agents with Anthropic's Claude API using Go. Designed for mobile development with Termux on Android devices like the Samsung Galaxy S25 Ultra.

## ✨ Features

- 💬 **Chat Agent** - Interactive conversation with Claude
- 🏗️ **Modular Architecture** - Easy to extend with new agents
- 📱 **Termux Compatible** - Runs perfectly on Android
- 🪶 **Lightweight** - Minimal dependencies
- 🎯 **CLI Interface** - Clean command-line interface with Cobra

## 🚀 Quick Start (Termux)

### Prerequisites

```bash
# Install Go in Termux
pkg update
pkg install golang

# Verify installation
go version
```

### Installation

```bash
# Clone or copy the project
cd ~/aic_projects
git clone [your-repo-url] coding-agent-workshop
cd coding-agent-workshop

# Or if you copied the files manually
cd ~/aic_projects/go-coding-agent-workshop

# Set your Anthropic API key
export ANTHROPIC_API_KEY="sk-ant-api03-your-key-here"

# Download dependencies
go mod tidy

# Build the agent
go build -o bin/agent cmd/main.go

# Run the chat agent
./bin/agent chat
```

## 📁 Project Structure

```
go-coding-agent-workshop/
├── cmd/
│   └── main.go              # Application entry point
├── internal/
│   ├── agents/
│   │   ├── agent.go         # Base agent interface
│   │   └── chat.go          # Chat agent implementation
│   ├── api/
│   │   └── client.go        # Anthropic API client
│   ├── logger/
│   │   └── logger.go        # Logging utilities
│   └── tools/               # Future: file ops, bash, etc.
├── go.mod                   # Go module definition
├── go.sum                   # Dependency checksums
└── README.md               # This file
```

## 🎯 Usage

### Chat Agent

Start an interactive chat session with Claude:

```bash
# Basic usage
./bin/agent chat

# With verbose logging
./bin/agent chat --verbose
./bin/agent chat -v

# With custom API key
./bin/agent chat --api-key="sk-ant-api03-your-key"
```

### Example Session

```
$ ./bin/agent chat

ℹ️  Starting chat agent...
ℹ️  🤖 Chat Agent started!
ℹ️  💬 Type your messages and press Enter
ℹ️  🚪 Type 'exit' to quit

You: Hello! Can you help me write a Go function?

🤖 Claude: Of course! I'd be happy to help you write a Go function.
What kind of function would you like to create? Please describe what
you want it to do, including:
- The function's purpose
- Input parameters
- Expected output/return value
- Any specific requirements or constraints

You: exit
👋 Goodbye!
```

## 🔧 Development

### Building

```bash
# Build for current platform
go build -o bin/agent cmd/main.go

# Build with optimizations
go build -ldflags="-s -w" -o bin/agent cmd/main.go

# Cross-compile for different platforms
GOOS=linux GOARCH=arm64 go build -o bin/agent-linux-arm64 cmd/main.go
```

### Testing

```bash
# Run tests (when added)
go test ./...

# With coverage
go test -cover ./...

# Verbose output
go test -v ./...
```

### Adding New Agents

To add a new agent (e.g., "read" agent for file operations):

1. **Create agent file**: `internal/agents/read.go`

```go
package agents

import (
	"coding-agent-workshop/internal/api"
	"coding-agent-workshop/internal/logger"
)

type ReadAgent struct {
	*BaseAgent
}

func NewReadAgent(client *api.Client, logger *logger.Logger) Agent {
	return &ReadAgent{
		BaseAgent: NewBaseAgent("read", client, logger),
	}
}

func (a *ReadAgent) Run() error {
	// Your implementation here
	return nil
}
```

2. **Register in main.go**:

```go
rootCmd.AddCommand(
	createCmd("chat", "💬 Interactive chat", agents.NewChatAgent),
	createCmd("read", "📖 Read files", agents.NewReadAgent),
)
```

3. **Rebuild and run**:

```bash
go build -o bin/agent cmd/main.go
./bin/agent read
```

## 📚 API Reference

### Logger

```go
type Logger interface {
	Info(msg string)
	Debug(msg string)
	Error(msg string)
	Fatal(msg string)
	Infof(format string, args ...interface{})
	Debugf(format string, args ...interface{})
	Errorf(format string, args ...interface{})
	Fatalf(format string, args ...interface{})
}
```

### API Client

```go
type Client interface {
	SendMessage(message string) (string, error)
}
```

### Agent

```go
type Agent interface {
	Run() error
	Stop() error
	Name() string
}
```

## 🔑 Configuration

### Environment Variables

- `ANTHROPIC_API_KEY` - Your Anthropic API key (required)

### API Key Setup

Get your API key from [Anthropic Console](https://console.anthropic.com/):

```bash
# Temporary (current session)
export ANTHROPIC_API_KEY="sk-ant-api03-your-key-here"

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

## 🐛 Troubleshooting

### "go: command not found"

Install Go in Termux:
```bash
pkg install golang
```

### "ANTHROPIC_API_KEY required"

Set your API key:
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### "API error: 401"

Your API key is invalid. Verify it at https://console.anthropic.com/

### "API error: 429"

You've exceeded your rate limit. Check your plan at https://console.anthropic.com/

### Build errors

Clean and rebuild:
```bash
go clean
rm -rf bin/
go mod tidy
go build -o bin/agent cmd/main.go
```

## 🎨 Customization

### Change Claude Model

Edit `internal/api/client.go`:

```go
Model: "claude-3-opus-20240229",  // Or claude-3-haiku-20240307
```

### Adjust Response Length

Edit `internal/api/client.go`:

```go
MaxTokens: 2000,  // Default is 1000
```

### Custom Log Formatting

Edit `internal/logger/logger.go`:

```go
info: log.New(os.Stdout, "INFO: ", log.LstdFlags),
```

## 📱 Mobile Development Tips

### Termux Best Practices

1. **Keep phone charging** during long builds
2. **Use wake lock** to prevent sleep: `termux-wake-lock`
3. **Storage access**: `termux-setup-storage`
4. **Background execution**: Use `tmux` or `screen`

### Running in Background

```bash
# Install tmux
pkg install tmux

# Start tmux session
tmux new -s agent

# Run your agent
./bin/agent chat

# Detach: Ctrl+B, then D
# Reattach: tmux attach -t agent
```

## 🚀 Performance

### Binary Size

```bash
# Check size
ls -lh bin/agent

# Reduce size with flags
go build -ldflags="-s -w" -o bin/agent cmd/main.go

# Further compression with upx (if available)
upx --best --lzma bin/agent
```

### Memory Usage

The agent is lightweight and uses minimal memory:
- Base: ~10-15MB
- Per request: +2-5MB temporarily

## 🤝 Contributing

Future agents to add:
- 📖 **Read Agent** - File reading and analysis
- 📁 **List Agent** - Directory listing
- ⚡ **Bash Agent** - Command execution
- ✏️ **Edit Agent** - File modification
- 🔍 **Search Agent** - Code searching

## 📄 License

MIT License - Free to use and modify

## 🙏 Credits

- Built with [Anthropic Claude API](https://www.anthropic.com/claude)
- CLI framework: [Cobra](https://github.com/spf13/cobra)
- Designed for mobile development on Samsung Galaxy S25 Ultra

## 📞 Support

For issues or questions:
- Check the troubleshooting section above
- Review Anthropic API docs: https://docs.anthropic.com/
- Test with verbose logging: `./bin/agent chat -v`

---

**Made with ❤️ for mobile AI development on Android**

Happy coding! 🚀📱
