package agents

import (
	"coding-agent-workshop/internal/api"
	"coding-agent-workshop/internal/logger"
)

type Agent interface {
	Run() error
	Stop() error
	Name() string
}

type BaseAgent struct {
	client *api.Client
	logger *logger.Logger
	name   string
}

func NewBaseAgent(name string, client *api.Client, logger *logger.Logger) *BaseAgent {
	return &BaseAgent{
		client: client,
		logger: logger,
		name:   name,
	}
}

func (a *BaseAgent) Name() string {
	return a.name
}

func (a *BaseAgent) Stop() error {
	a.logger.Info("Agent stopped")
	return nil
}
