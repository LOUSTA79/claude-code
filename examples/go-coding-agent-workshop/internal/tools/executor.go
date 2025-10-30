package tools

import (
	"bytes"
	"fmt"
	"os/exec"
	"strings"
	"time"

	"coding-agent-workshop/internal/logger"
)

type Executor struct {
	logger *logger.Logger
}

func NewExecutor(logger *logger.Logger) *Executor {
	return &Executor{logger: logger}
}

// Execute runs a shell command and returns the output
func (e *Executor) Execute(command string) (string, error) {
	// Security check - block dangerous commands
	dangerous := []string{
		"rm -rf /",
		"dd if=",
		"mkfs",
		":(){:|:&};:",
		"> /dev/",
		"chmod -R 777 /",
		"chown -R",
	}

	for _, pattern := range dangerous {
		if strings.Contains(command, pattern) {
			return "", fmt.Errorf("dangerous command blocked: %s", pattern)
		}
	}

	e.logger.Debugf("Executing command: %s", command)

	// Create command
	cmd := exec.Command("sh", "-c", command)

	// Capture output
	var stdout bytes.Buffer
	var stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	// Set timeout
	done := make(chan error)
	go func() {
		done <- cmd.Run()
	}()

	select {
	case err := <-done:
		output := stdout.String()
		if stderr.Len() > 0 {
			output += "\n[stderr]\n" + stderr.String()
		}

		if err != nil {
			return output, fmt.Errorf("command failed: %w", err)
		}

		return output, nil

	case <-time.After(30 * time.Second):
		cmd.Process.Kill()
		return "", fmt.Errorf("command timed out after 30 seconds")
	}
}

// ExecuteWithTimeout runs a command with a custom timeout
func (e *Executor) ExecuteWithTimeout(command string, timeout time.Duration) (string, error) {
	e.logger.Debugf("Executing command with timeout %v: %s", timeout, command)

	cmd := exec.Command("sh", "-c", command)

	var stdout bytes.Buffer
	var stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	done := make(chan error)
	go func() {
		done <- cmd.Run()
	}()

	select {
	case err := <-done:
		output := stdout.String()
		if stderr.Len() > 0 {
			output += "\n[stderr]\n" + stderr.String()
		}

		if err != nil {
			return output, fmt.Errorf("command failed: %w", err)
		}

		return output, nil

	case <-time.After(timeout):
		cmd.Process.Kill()
		return "", fmt.Errorf("command timed out after %v", timeout)
	}
}
