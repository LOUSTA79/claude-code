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

type EditAgent struct {
	*BaseAgent
	filesystem *tools.Filesystem
}

func NewEditAgent(client *api.Client, logger *logger.Logger) Agent {
	return &EditAgent{
		BaseAgent:  NewBaseAgent("edit", client, logger),
		filesystem: tools.NewFilesystem(logger),
	}
}

func (a *EditAgent) Run() error {
	a.logger.Info("✏️  Edit Agent started!")
	a.logger.Info("📝 Enter file path to create/edit")
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

		// Check if file exists
		exists := a.filesystem.FileExists(path)
		if exists {
			fmt.Printf("📄 File exists. Enter new content (or type '//cancel' to cancel):\n")
		} else {
			fmt.Printf("📝 Creating new file. Enter content (or type '//cancel' to cancel):\n")
		}

		fmt.Println("(Press Ctrl+D when done, or type '//end' on a new line)")
		fmt.Println(strings.Repeat("─", 60))

		// Read multiline input
		var content strings.Builder
		lineScanner := bufio.NewScanner(os.Stdin)
		for lineScanner.Scan() {
			line := lineScanner.Text()
			if line == "//cancel" {
				fmt.Println("❌ Cancelled")
				break
			}
			if line == "//end" {
				break
			}
			content.WriteString(line + "\n")
		}

		if content.Len() == 0 {
			continue
		}

		// Write file
		a.logger.Debugf("Writing file: %s", path)
		err := a.filesystem.WriteFile(path, content.String())
		if err != nil {
			a.logger.Errorf("Failed to write file: %v", err)
			continue
		}

		fmt.Printf("\n✅ File saved: %s (%d bytes)\n\n", path, content.Len())
	}

	return nil
}
