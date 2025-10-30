package agents

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"coding-agent-workshop/internal/api"
	"coding-agent-workshop/internal/logger"
	"coding-agent-workshop/internal/tools"
)

type ReadAgent struct {
	*BaseAgent
	filesystem *tools.Filesystem
}

func NewReadAgent(client *api.Client, logger *logger.Logger) Agent {
	return &ReadAgent{
		BaseAgent:  NewBaseAgent("read", client, logger),
		filesystem: tools.NewFilesystem(logger),
	}
}

func (a *ReadAgent) Run() error {
	a.logger.Info("📖 Read Agent started!")
	a.logger.Info("📄 Enter file paths to read and analyze")
	a.logger.Info("🚪 Type 'exit' to quit")
	fmt.Println()

	scanner := bufio.NewScanner(os.Stdin)

	for {
		fmt.Print("File path: ")
		if !scanner.Scan() {
			break
		}

		path := strings.TrimSpace(scanner.Text())
		if path == "exit" || path == "quit" {
			fmt.Println("👋 Goodbye!")
			break
		}

		if path == "" {
			continue
		}

		a.logger.Debugf("Reading file: %s", path)

		content, err := a.filesystem.ReadFile(path)
		if err != nil {
			a.logger.Errorf("Failed to read file: %v", err)
			continue
		}

		// Show file info
		lines := strings.Count(content, "\n") + 1
		fmt.Printf("\n📊 File: %s (%d lines)\n", path, lines)

		// Get AI analysis
		prompt := fmt.Sprintf("Analyze this code file (%s):\n\n%s\n\nProvide a concise summary of what this code does.", path, content)

		fmt.Println("🤖 Analyzing...")
		response, err := a.client.SendMessage(prompt)
		if err != nil {
			a.logger.Errorf("API Error: %v", err)
			continue
		}

		fmt.Printf("\n🔍 Analysis:\n%s\n\n", response)
	}

	return nil
}
