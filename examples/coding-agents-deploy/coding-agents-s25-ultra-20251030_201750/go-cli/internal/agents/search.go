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

type SearchAgent struct {
	*BaseAgent
	searcher *tools.Searcher
}

func NewSearchAgent(client *api.Client, logger *logger.Logger) Agent {
	return &SearchAgent{
		BaseAgent: NewBaseAgent("search", client, logger),
		searcher:  tools.NewSearcher(logger),
	}
}

func (a *SearchAgent) Run() error {
	a.logger.Info("🔍 Search Agent started!")
	a.logger.Info("🔎 Enter search queries")
	a.logger.Info("🚪 Type 'exit' to quit")
	fmt.Println()

	scanner := bufio.NewScanner(os.Stdin)

	for {
		fmt.Print("Search query: ")
		if !scanner.Scan() {
			break
		}

		query := strings.TrimSpace(scanner.Text())
		if query == "exit" || query == "quit" {
			fmt.Println("👋 Goodbye!")
			break
		}

		if query == "" {
			continue
		}

		fmt.Print("Directory to search (default: '.'): ")
		scanner.Scan()
		dir := strings.TrimSpace(scanner.Text())
		if dir == "" {
			dir = "."
		}

		a.logger.Debugf("Searching for '%s' in %s", query, dir)
		fmt.Println("🔍 Searching...")

		results, err := a.searcher.Search(query, dir)
		if err != nil {
			a.logger.Errorf("Search failed: %v", err)
			continue
		}

		if len(results) == 0 {
			fmt.Println("❌ No results found\n")
			continue
		}

		fmt.Printf("\n📊 Found %d matches:\n", len(results))
		fmt.Println(strings.Repeat("─", 60))

		for _, result := range results {
			fmt.Printf("📄 %s:%d\n", result.File, result.Line)
			fmt.Printf("   %s\n\n", result.Content)
		}
	}

	return nil
}
