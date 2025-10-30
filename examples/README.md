# Claude Code Examples

This directory contains example code demonstrating common patterns and solutions when working with Claude Code and AI-powered applications.

## Examples

### [openai-express-server-example.js](./openai-express-server-example.js)

A complete Express.js server demonstrating **proper OpenAI client initialization**. This example addresses the common error:

```
ReferenceError: oai is not defined
```

**What you'll learn:**
- Correct initialization order for OpenAI client
- CommonJS vs ES modules approaches
- Environment variable configuration
- Error handling for AI endpoints
- Complete working chat API implementation

**Quick start:**
```bash
cd examples
npm install express openai dotenv
node openai-express-server-example.js
```

**Test it:**
```bash
curl "http://localhost:3000/ai/chat?q=Hello"
```

### Hooks

The `hooks/` subdirectory contains examples of Claude Code hooks for customizing behavior:

- **[bash_command_validator_example.py](./hooks/bash_command_validator_example.py)** - Validates bash commands before execution

## Contributing Examples

If you have a useful pattern or solution you'd like to share:

1. Create a well-documented example file
2. Add it to this README with a brief description
3. Submit a pull request

Examples should be:
- Self-contained and runnable
- Well-commented
- Include common troubleshooting tips
- Follow best practices
