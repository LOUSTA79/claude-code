package tools

import (
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"

	"coding-agent-workshop/internal/logger"
)

type Filesystem struct {
	logger *logger.Logger
}

func NewFilesystem(logger *logger.Logger) *Filesystem {
	return &Filesystem{logger: logger}
}

func (fs *Filesystem) ReadFile(path string) (string, error) {
	fs.logger.Debugf("Reading file: %s", path)

	content, err := ioutil.ReadFile(path)
	if err != nil {
		return "", fmt.Errorf("failed to read file: %w", err)
	}

	return string(content), nil
}

func (fs *Filesystem) WriteFile(path, content string) error {
	fs.logger.Debugf("Writing file: %s", path)

	dir := filepath.Dir(path)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return fmt.Errorf("failed to create directory: %w", err)
	}

	if err := ioutil.WriteFile(path, []byte(content), 0644); err != nil {
		return fmt.Errorf("failed to write file: %w", err)
	}

	return nil
}

func (fs *Filesystem) ListDirectory(path string) ([]os.FileInfo, error) {
	fs.logger.Debugf("Listing directory: %s", path)

	files, err := ioutil.ReadDir(path)
	if err != nil {
		return nil, fmt.Errorf("failed to read directory: %w", err)
	}

	return files, nil
}

func (fs *Filesystem) FileExists(path string) bool {
	_, err := os.Stat(path)
	return err == nil
}

func (fs *Filesystem) IsDirectory(path string) bool {
	info, err := os.Stat(path)
	if err != nil {
		return false
	}
	return info.IsDir()
}
