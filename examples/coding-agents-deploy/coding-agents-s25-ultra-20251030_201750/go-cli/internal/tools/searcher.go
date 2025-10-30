package tools

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"coding-agent-workshop/internal/logger"
)

type SearchResult struct {
	File    string
	Line    int
	Content string
}

type Searcher struct {
	logger *logger.Logger
}

func NewSearcher(logger *logger.Logger) *Searcher {
	return &Searcher{logger: logger}
}

// Search performs a recursive grep-like search
func (s *Searcher) Search(query, dir string) ([]SearchResult, error) {
	s.logger.Debugf("Searching for '%s' in %s", query, dir)

	var results []SearchResult
	query = strings.ToLower(query) // Case-insensitive search

	err := filepath.Walk(dir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return nil // Skip files we can't access
		}

		// Skip directories
		if info.IsDir() {
			// Skip hidden directories and common ignore patterns
			name := info.Name()
			if strings.HasPrefix(name, ".") || name == "node_modules" || name == "vendor" {
				return filepath.SkipDir
			}
			return nil
		}

		// Only search text files (simple heuristic)
		if !isTextFile(path) {
			return nil
		}

		// Search within file
		matches, err := s.searchInFile(path, query)
		if err != nil {
			s.logger.Debugf("Error searching %s: %v", path, err)
			return nil // Continue despite errors
		}

		results = append(results, matches...)
		return nil
	})

	if err != nil {
		return nil, fmt.Errorf("search failed: %w", err)
	}

	// Limit results to avoid overwhelming output
	if len(results) > 50 {
		results = results[:50]
	}

	return results, nil
}

func (s *Searcher) searchInFile(path, query string) ([]SearchResult, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var results []SearchResult
	scanner := bufio.NewScanner(file)
	lineNum := 0

	for scanner.Scan() {
		lineNum++
		line := scanner.Text()
		lineLower := strings.ToLower(line)

		if strings.Contains(lineLower, query) {
			results = append(results, SearchResult{
				File:    path,
				Line:    lineNum,
				Content: strings.TrimSpace(line),
			})
		}
	}

	return results, scanner.Err()
}

func isTextFile(path string) bool {
	// Simple heuristic based on extension
	ext := strings.ToLower(filepath.Ext(path))
	textExts := map[string]bool{
		".go":   true,
		".js":   true,
		".ts":   true,
		".py":   true,
		".java": true,
		".c":    true,
		".cpp":  true,
		".h":    true,
		".hpp":  true,
		".rs":   true,
		".rb":   true,
		".php":  true,
		".html": true,
		".css":  true,
		".md":   true,
		".txt":  true,
		".json": true,
		".yaml": true,
		".yml":  true,
		".toml": true,
		".xml":  true,
		".sh":   true,
		".bash": true,
		".sql":  true,
	}

	return textExts[ext]
}
