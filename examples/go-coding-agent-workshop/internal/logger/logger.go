package logger

import (
	"log"
	"os"
)

type Logger struct {
	verbose bool
	info    *log.Logger
	debug   *log.Logger
	error   *log.Logger
}

func New(verbose bool) *Logger {
	return &Logger{
		verbose: verbose,
		info:    log.New(os.Stdout, "ℹ️  ", log.Ltime),
		debug:   log.New(os.Stdout, "🐛 ", log.Ltime),
		error:   log.New(os.Stderr, "❌ ", log.Ltime),
	}
}

func (l *Logger) Info(msg string) {
	l.info.Println(msg)
}

func (l *Logger) Debug(msg string) {
	if l.verbose {
		l.debug.Println(msg)
	}
}

func (l *Logger) Error(msg string) {
	l.error.Println(msg)
}

func (l *Logger) Fatal(msg string) {
	l.error.Fatal(msg)
}

func (l *Logger) Infof(format string, args ...interface{}) {
	l.info.Printf(format, args...)
}

func (l *Logger) Debugf(format string, args ...interface{}) {
	if l.verbose {
		l.debug.Printf(format, args...)
	}
}

func (l *Logger) Errorf(format string, args ...interface{}) {
	l.error.Printf(format, args...)
}

func (l *Logger) Fatalf(format string, args ...interface{}) {
	l.error.Fatalf(format, args...)
}
