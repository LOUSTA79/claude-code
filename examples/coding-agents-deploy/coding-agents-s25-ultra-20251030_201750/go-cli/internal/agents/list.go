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

type ListAgent struct {
	*BaseAgent
	filesystem *tools.Filesystem
}

func NewListAgent(client *api.Client, logger *logger.Logger) Agent {
	return &ListAgent{
		BaseAgent:  NewBaseAgent("list", client, logger),
		filesystem: tools.NewFilesystem(logger),
	}
}

func (a *ListAgent) Run() error {
	a.logger.Info("📁 List Agent started!")
	a.logger.Info("📂 Enter directory paths to list")
	a.logger.Info("🚪 Type 'exit' to quit")
	fmt.Println()

	scanner := bufio.NewScanner(os.Stdin)

	for {
		fmt.Print("Directory path (or '.' for current): ")
		if !scanner.Scan() {
			break
		}

		path := strings.TrimSpace(scanner.Text())
		if path == "exit" || path == "quit" {
			fmt.Println("👋 Goodbye!")
			break
		}

		if path == "" {
			path = "."
		}

		a.logger.Debugf("Listing directory: %s", path)

		files, err := a.filesystem.ListDirectory(path)
		if err != nil {
			a.logger.Errorf("Failed to list directory: %v", err)
			continue
		}

		fmt.Printf("\n📂 Directory: %s (%d items)\n", path, len(files))
		fmt.Println(strings.Repeat("─", 60))

		for _, file := range files {
			icon := "📄"
			typeStr := "file"
			if file.IsDir() {
				icon = "📁"
				typeStr = "dir "
			}
			fmt.Printf("%s %-50s %s %8d bytes\n",
				icon,
				file.Name(),
				typeStr,
				file.Size(),
			)
		}
		fmt.Println()
	}

	return nil
}
