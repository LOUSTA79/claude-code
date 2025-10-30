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

type BashAgent struct {
	*BaseAgent
	executor *tools.Executor
}

func NewBashAgent(client *api.Client, logger *logger.Logger) Agent {
	return &BashAgent{
		BaseAgent: NewBaseAgent("bash", client, logger),
		executor:  tools.NewExecutor(logger),
	}
}

func (a *BashAgent) Run() error {
	a.logger.Info("⚡ Bash Agent started!")
	a.logger.Info("💻 Enter commands to execute")
	a.logger.Info("⚠️  Dangerous commands are blocked for safety")
	a.logger.Info("🚪 Type 'exit' to quit")
	fmt.Println()

	scanner := bufio.NewScanner(os.Stdin)

	for {
		fmt.Print("$ ")
		if !scanner.Scan() {
			break
		}

		command := strings.TrimSpace(scanner.Text())
		if command == "exit" || command == "quit" {
			fmt.Println("👋 Goodbye!")
			break
		}

		if command == "" {
			continue
		}

		a.logger.Debugf("Executing: %s", command)

		output, err := a.executor.Execute(command)
		if err != nil {
			a.logger.Errorf("Command failed: %v", err)
			if output != "" {
				fmt.Printf("\n%s\n", output)
			}
			continue
		}

		fmt.Printf("\n%s\n", output)
	}

	return nil
}
