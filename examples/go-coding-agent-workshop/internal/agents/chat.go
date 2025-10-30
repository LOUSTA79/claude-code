package agents

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"coding-agent-workshop/internal/api"
	"coding-agent-workshop/internal/logger"
)

type ChatAgent struct {
	*BaseAgent
}

func NewChatAgent(client *api.Client, logger *logger.Logger) Agent {
	return &ChatAgent{
		BaseAgent: NewBaseAgent("chat", client, logger),
	}
}

func (a *ChatAgent) Run() error {
	a.logger.Info("🤖 Chat Agent started!")
	a.logger.Info("💬 Type your messages and press Enter")
	a.logger.Info("🚪 Type 'exit' to quit")
	fmt.Println()

	scanner := bufio.NewScanner(os.Stdin)

	for {
		fmt.Print("You: ")
		if !scanner.Scan() {
			break
		}

		input := strings.TrimSpace(scanner.Text())
		if input == "exit" || input == "quit" {
			fmt.Println("👋 Goodbye!")
			break
		}

		if input == "" {
			continue
		}

		a.logger.Debugf("User input: %s", input)

		response, err := a.client.SendMessage(input)
		if err != nil {
			a.logger.Errorf("API Error: %v", err)
			continue
		}

		fmt.Printf("\n🤖 Claude: %s\n\n", response)
	}

	return nil
}
