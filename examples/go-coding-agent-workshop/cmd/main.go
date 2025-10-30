package main

import (
	"fmt"
	"log"
	"os"

	"coding-agent-workshop/internal/agents"
	"coding-agent-workshop/internal/api"
	"coding-agent-workshop/internal/logger"

	"github.com/spf13/cobra"
)

var (
	verbose bool
	apiKey  string
)

func main() {
	var rootCmd = &cobra.Command{
		Use:   "agent",
		Short: "Coding Agent Workshop",
		Long:  "Build AI-powered coding agents with Anthropic's Claude",
	}

	rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "Enable verbose logging")
	rootCmd.PersistentFlags().StringVar(&apiKey, "api-key", os.Getenv("ANTHROPIC_API_KEY"), "Anthropic API key")

	createCmd := func(name, desc string, factory func(*api.Client, *logger.Logger) agents.Agent) *cobra.Command {
		return &cobra.Command{
			Use:   name,
			Short: desc,
			Run: func(cmd *cobra.Command, args []string) {
				log := logger.New(verbose)
				if apiKey == "" {
					log.Fatal("ANTHROPIC_API_KEY required. Set with: export ANTHROPIC_API_KEY='your-key'")
				}
				client := api.NewClient(apiKey, log)
				agent := factory(client, log)
				log.Infof("Starting %s agent...", name)
				if err := agent.Run(); err != nil {
					log.Fatalf("Agent failed: %v", err)
				}
			},
		}
	}

	rootCmd.AddCommand(
		createCmd("chat", "💬 Interactive chat", agents.NewChatAgent),
	)

	if err := rootCmd.Execute(); err != nil {
		log.Fatal(err)
	}
}
