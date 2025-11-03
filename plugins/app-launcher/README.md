# App Launcher Plugin

One-click automated application launch system for Claude Code that intelligently detects your application type, validates dependencies, and launches your app with a single command.

## Features

- **Intelligent App Detection**: Automatically identifies your application type (Node.js, TypeScript, Python, Agent SDK, Docker, and more)
- **Dependency Management**: Checks if dependencies are installed and can automatically install them
- **Environment Validation**: Verifies required environment variables and configuration files
- **Smart Launch**: Uses the most appropriate launch command for your app type
- **Pre-flight Checks**: Validates your app is ready to run before attempting to launch
- **Comprehensive Feedback**: Provides clear status updates and actionable error messages

## Commands

### `/launch`

One-click command to launch your application.

**Usage:**
```bash
/launch [options]
```

**Options:**
- `--install` or `-i`: Force dependency installation even if they appear installed
- `--skip-validation` or `-s`: Skip all validation checks and attempt to launch immediately
- `--background` or `-b`: Run the application in the background
- `--production` or `-p`: Launch in production mode

**Examples:**
```bash
# Simple launch
/launch

# Force install dependencies and launch
/launch --install

# Launch in background mode
/launch --background

# Skip validation and launch immediately
/launch --skip-validation
```

## Agents

### `launch-validator`

Performs comprehensive pre-flight checks to ensure your application is ready to launch.

**What it checks:**
- Application type detection
- Dependency installation status
- Configuration file validity
- Environment variable setup
- Entry point existence and validity
- Framework-specific requirements

**Returns:**
- Detailed readiness report
- Overall readiness score
- List of blockers (if any)
- Warnings and recommendations
- Suggested launch command

## Supported Application Types

### Node.js / TypeScript
- Auto-detects package.json
- Checks for node_modules
- Validates tsconfig.json (for TypeScript)
- Runs TypeScript type checking
- Uses npm/yarn/pnpm/bun scripts

### Python
- Auto-detects requirements.txt, pyproject.toml, setup.py
- Checks for virtual environment
- Validates installed packages
- Supports Django, Flask, FastAPI frameworks

### Claude Agent SDK
- Detects Agent SDK TypeScript and Python apps
- Validates SDK installation
- Checks for ANTHROPIC_API_KEY
- Ensures proper SDK configuration

### Docker
- Detects docker-compose.yml and Dockerfile
- Validates Docker installation
- Checks if images are built
- Can launch with docker-compose up

### Other Supported Types
- Go (go.mod)
- Rust (Cargo.toml)
- Java (pom.xml, build.gradle)

## How It Works

1. **Detection Phase**: Scans current directory for package files, config files, and entry points
2. **Validation Phase**: Checks dependencies, configuration, and environment setup
3. **Preparation Phase**: Installs missing dependencies if needed
4. **Launch Phase**: Executes the appropriate start command
5. **Monitoring Phase**: Captures startup output and reports status

## Example Workflows

### Node.js Application

```bash
$ /launch

Detected: Node.js application with TypeScript
✓ package.json found
✓ tsconfig.json found
✓ Dependencies installed (node_modules exists)
✓ Found start script: "tsx index.ts"

Launching application...
$ npm start

> my-app@1.0.0 start
> tsx index.ts

Server listening on http://localhost:3000

✓ Application launched successfully!
Access your app at: http://localhost:3000
Press Ctrl+C to stop the server
```

### Python Application with Missing Dependencies

```bash
$ /launch

Detected: Python application
✓ main.py found
✗ Dependencies not installed

Installing dependencies...
$ pip install -r requirements.txt

Successfully installed 15 packages

Launching application...
$ python main.py

Application running!
```

### Agent SDK Application with Missing API Key

```bash
$ /launch

Detected: Claude Agent SDK (TypeScript)
✓ @anthropic-ai/claude-agent-sdk installed
✓ index.ts entry point found
✗ .env file not found

You need to set up your environment:
1. Create .env file: cp .env.example .env
2. Add your API key from https://console.anthropic.com/
3. Run /launch again

Would you like me to create the .env file for you?
```

## Error Handling

The launcher provides specific error messages and solutions for common issues:

- **Missing dependencies**: Shows installation command
- **Port conflicts**: Helps identify what's using the port
- **Missing environment variables**: Guides through setup process
- **Configuration errors**: Suggests specific fixes
- **Type errors** (TypeScript): Lists errors and suggests fixes

## Best Practices

1. **Always use /launch first**: Let the launcher detect and validate before manually running commands
2. **Check the validation report**: The launch-validator agent provides detailed insights
3. **Keep .env.example updated**: Helps the launcher know what environment variables are needed
4. **Use standard entry points**: Follow conventions (index.ts, main.py, etc.) for better detection
5. **Define scripts in package.json**: Makes launch detection more reliable for Node.js apps

## Troubleshooting

### Application not detected correctly
- Ensure you have standard config files (package.json, requirements.txt, etc.)
- Check that files are in the current directory
- Try using `--skip-validation` if detection is incorrect

### Dependencies install but app won't start
- Check error messages carefully
- Ensure environment variables are set (especially for Agent SDK apps)
- Verify entry point files exist and are named correctly
- Run the launch-validator agent for detailed diagnostics

### Type errors in TypeScript apps
- The launcher runs `npx tsc --noEmit` to check types
- Fix all reported type errors before the app will launch
- Check that SDK types are correctly imported

## Integration with Other Plugins

Works seamlessly with:
- **agent-sdk-dev**: Can launch apps created with `/new-sdk-app`
- **commit-commands**: Launch after committing changes
- **feature-dev**: Launch apps after feature development

## Contributing

To improve application type detection or add support for new frameworks, modify:
- `commands/launch.md` - Main launch logic
- `agents/launch-validator.md` - Validation logic

## License

Part of the Claude Code plugin ecosystem by Anthropic.
