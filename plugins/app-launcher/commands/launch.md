---
description: One-click automated application launch with dependency management
argument-hint: [--install|--skip-validation|--background]
---

You are tasked with automatically detecting, validating, and launching an application in the current directory. Follow these steps carefully to provide a seamless one-click launch experience.

## Overview

This command provides automated application launch with:
- **Auto-detection** of application type (Node.js, Python, Agent SDK, etc.)
- **Dependency validation** and automatic installation if needed
- **Configuration verification** to ensure the app is ready to run
- **Smart launch** with the appropriate command for the detected app type
- **Startup monitoring** with clear feedback and error handling

## Step 1: Detect Application Type

First, scan the current directory to determine what type of application this is. Look for these indicators:

### Package Files
- `package.json` → Node.js/TypeScript application
- `requirements.txt` or `pyproject.toml` or `setup.py` → Python application
- `Cargo.toml` → Rust application
- `go.mod` → Go application
- `pom.xml` or `build.gradle` → Java application

### Configuration Files
- `tsconfig.json` → TypeScript application
- `.python-version` or `Pipfile` → Python application
- `docker-compose.yml` → Docker application

### Entry Point Files
- `index.ts`, `index.js`, `main.ts`, `main.js`, `app.ts`, `app.js` → Node.js/TypeScript
- `main.py`, `app.py`, `__main__.py` → Python
- `main.go` → Go
- `main.rs` → Rust

### Special Markers
- If `package.json` contains `@anthropic-ai/claude-agent-sdk` dependency → Agent SDK TypeScript
- If `requirements.txt` or `pyproject.toml` contains `claude-agent-sdk` → Agent SDK Python

Use the Glob and Read tools to scan for these files. Read relevant configuration files to understand the project structure.

## Step 2: Validate Project Configuration

Based on the detected application type, perform validation checks:

### For Node.js/TypeScript Applications:
1. Check if `node_modules/` exists
2. Read `package.json` to identify:
   - Main entry point (`main`, `module`, or `exports` field)
   - Available scripts in `scripts` section
   - Required dependencies
3. Check for TypeScript configuration (`tsconfig.json`)
4. Look for environment file requirements (`.env.example` or `.env`)

### For Python Applications:
1. Check if virtual environment exists (`venv/`, `.venv/`, `env/`)
2. Read `requirements.txt` or `pyproject.toml` to identify dependencies
3. Check if dependencies are installed (use `pip list` or `pip show` for key packages)
4. Look for environment file requirements (`.env.example` or `.env`)

### For Agent SDK Applications:
1. Verify SDK is installed (check in dependencies or installed packages)
2. Check for `.env` file and `ANTHROPIC_API_KEY` presence
3. Validate entry point exists and has correct imports
4. Optionally invoke the appropriate verifier agent:
   - For TypeScript: Consider using `agent-sdk-verifier-ts` agent
   - For Python: Consider using `agent-sdk-verifier-py` agent

### For Docker Applications:
1. Check if `docker-compose.yml` or `Dockerfile` exists
2. Verify Docker is available (`docker --version`)

## Step 3: Install Dependencies (if needed)

Based on validation results and user arguments:

### Check User Arguments:
- If `--skip-validation` is present in $ARGUMENTS, skip dependency checks and proceed to launch
- If `--install` is present, force dependency installation even if they appear installed
- Otherwise, install only if dependencies are missing

### For Node.js/TypeScript:
```bash
npm install
```
Or use the detected package manager (yarn, pnpm, bun) if identified in `package.json` or lockfiles.

### For Python:
```bash
# Create virtual environment if it doesn't exist
python -m venv venv

# Activate and install dependencies
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### For Docker:
```bash
docker-compose build
```

**Important**: Show progress and provide clear feedback during installation. If installation fails, report the error and suggest fixes.

## Step 4: Verify Environment Configuration

Check for required environment variables:

### For Agent SDK Applications:
1. Check if `.env` file exists
2. If not, but `.env.example` exists:
   - Inform the user they need to create a `.env` file
   - Show them the example: `cp .env.example .env`
   - Remind them to add their `ANTHROPIC_API_KEY` from https://console.anthropic.com/
   - **STOP and wait for user confirmation before launching**
3. If `.env` exists, check if `ANTHROPIC_API_KEY` is set (read the file and look for non-empty value)

### For Other Applications:
1. Check for `.env.example` and suggest creating `.env` if it doesn't exist
2. Do not block launch if `.env` is missing (unless it's an Agent SDK app)

## Step 5: Determine Launch Command

Based on the application type and configuration, determine the appropriate launch command:

### For Node.js/TypeScript Applications:

**Priority order**:
1. If `package.json` has `"start"` script → `npm start`
2. If `package.json` has `"dev"` script → `npm run dev`
3. If TypeScript with `index.ts` or `main.ts` → `npx tsx index.ts` (or appropriate entry point)
4. If JavaScript with `index.js` or `main.js` → `node index.js` (or appropriate entry point)
5. Otherwise, check `main` field in `package.json` and run that

### For Python Applications:

**Priority order**:
1. If `main.py` exists → `python main.py`
2. If `app.py` exists → `python app.py`
3. If `__main__.py` exists → `python .`
4. If `setup.py` exists and package is installed → `python -m <package_name>`
5. Otherwise, ask user which file to run

### For Agent SDK Applications:

**TypeScript**:
- If `"start"` script exists → `npm start`
- Otherwise → `npx tsx index.ts` (or detected entry point)

**Python**:
- `python main.py` (or detected entry point)
- Ensure virtual environment is activated if it exists

### For Docker Applications:
```bash
docker-compose up
```

## Step 6: Launch the Application

Now launch the application with the determined command:

### Check for Background Flag:
- If `--background` is present in $ARGUMENTS, run the command in the background
- Otherwise, provide instructions for running in foreground

### Launch Process:

1. **Inform the user** of the launch command you're about to run
2. **Execute the launch command** using the Bash tool:
   - If `--background` flag is used, set `run_in_background: true`
   - Otherwise, set a reasonable timeout (e.g., 30 seconds) to capture initial output
3. **Capture startup output** and analyze it for:
   - Success indicators (server started, listening on port, etc.)
   - Error messages (port already in use, missing dependencies, etc.)
   - Warnings that should be addressed

### For Background Launches:
- Return the shell ID for the user to monitor with BashOutput
- Provide instructions on how to check logs and stop the process

## Step 7: Monitor and Report

After launching:

1. **Analyze the output**:
   - Look for successful startup messages
   - Identify any errors or warnings
   - Check if the application is listening on a port

2. **Provide clear feedback**:
   - ✓ Success: Report successful launch with any important info (port numbers, URLs, etc.)
   - ✗ Error: Report the error clearly and suggest troubleshooting steps
   - ⚠ Warning: Report any warnings that might affect functionality

3. **Give next steps**:
   - How to access the application (URLs, ports)
   - How to stop the application (Ctrl+C, docker-compose down, etc.)
   - How to view logs if running in background

## Error Handling

If launch fails at any step:

1. **Provide clear error message** with context about what went wrong
2. **Suggest specific fixes** based on the error type:
   - Missing dependencies → Run installation command
   - Port in use → Show how to find and stop the conflicting process
   - Missing environment variables → Show how to configure them
   - Configuration errors → Suggest fixes based on error messages

3. **Offer to help fix** the issue if possible

## Special Cases

### Multiple Possible Entry Points:
If multiple entry points are found (e.g., both `app.py` and `main.py`), ask the user which one to launch.

### Development vs Production:
- Default to development mode (use `dev` scripts, development servers)
- If the user wants production mode, they can specify via arguments or we can add a `--production` flag

### Port Conflicts:
If the application fails to start due to a port conflict:
1. Detect the error message
2. Try to identify the port number
3. Show how to find what's using the port: `lsof -i :<port>` or `netstat -ano | grep <port>`
4. Suggest killing the process or changing the port

## Example Workflows

### Successful Node.js Launch:
```
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

### Python with Missing Dependencies:
```
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

### Agent SDK with Missing API Key:
```
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

## Important Notes

- **Always be informative**: Tell the user what you're detecting, checking, and doing
- **Handle errors gracefully**: Provide actionable feedback when things go wrong
- **Respect user's setup**: Don't override existing configurations without asking
- **Be smart about defaults**: Choose sensible defaults but allow user overrides
- **Validate before launching**: Don't launch if critical requirements are missing
- **Monitor startup**: Capture enough output to determine if launch was successful
- **Provide context**: Always explain what the application is and how to use it

## Arguments

This command supports these optional arguments:

- `--install` or `-i`: Force dependency installation even if they appear installed
- `--skip-validation` or `-s`: Skip all validation checks and attempt to launch immediately
- `--background` or `-b`: Run the application in the background
- `--production` or `-p`: Launch in production mode (use production scripts/settings)

Begin by detecting the application type in the current directory.
