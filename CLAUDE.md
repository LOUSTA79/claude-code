# CLAUDE.md - AI Assistant Guide for Claude Code Repository

**Last Updated**: 2025-12-07
**Repository**: Claude Code - Agentic coding tool and plugin ecosystem
**Version**: 2.0.13+

This document provides comprehensive guidance for AI assistants working with the Claude Code repository. It covers codebase structure, development workflows, conventions, and best practices.

---

## Table of Contents

1. [Repository Overview](#repository-overview)
2. [Codebase Structure](#codebase-structure)
3. [Plugin System Architecture](#plugin-system-architecture)
4. [Development Workflows](#development-workflows)
5. [Code Conventions](#code-conventions)
6. [Testing and Quality](#testing-and-quality)
7. [Git Workflow](#git-workflow)
8. [GitHub Automation](#github-automation)
9. [Plugin Development Guide](#plugin-development-guide)
10. [Common Patterns](#common-patterns)
11. [Important Files and Locations](#important-files-and-locations)
12. [Resources](#resources)

---

## Repository Overview

### Purpose
Claude Code is an agentic coding tool that lives in your terminal. It helps developers code faster by executing routine tasks, explaining complex code, and handling git workflows through natural language commands.

**Key Features**:
- Terminal-based AI coding assistant
- Extensible plugin system with marketplace
- Specialized agents for different development tasks
- Git and GitHub workflow automation
- Custom slash commands and hooks
- Integration with the Claude Agent SDK

### Technology Stack
- **Runtime**: Node.js 20+
- **Languages**: TypeScript (primary), Python (hooks and utilities)
- **Package Manager**: npm
- **Version Control**: Git with GitHub integration
- **Development Environment**: DevContainer support (VS Code)

### Current State
- **Latest Version**: 2.0.13
- **Latest Major Release**: 2.0.12 (Plugin System)
- **Active Development**: Yes (frequent commits and releases)
- **NPM Package**: `@anthropic-ai/claude-code`

---

## Codebase Structure

### Directory Layout

```
/home/user/claude-code/
├── .claude/                          # Repository-level Claude Code configuration
│   └── commands/                     # Custom slash commands for this repo
│       ├── commit-push-pr.md        # Composite git workflow command
│       └── dedupe.md                # GitHub issue deduplication
│
├── .claude-plugin/                   # Plugin marketplace configuration
│   └── marketplace.json              # Central registry of bundled plugins
│
├── .devcontainer/                    # VS Code DevContainer setup
│   ├── Dockerfile                    # Node 20 + Claude Code environment
│   ├── devcontainer.json             # Container configuration
│   └── init-firewall.sh              # Network initialization script
│
├── .github/
│   ├── workflows/                    # GitHub Actions (10 workflows)
│   │   ├── claude.yml                # @claude mentions on issues/PRs
│   │   ├── claude-issue-triage.yml  # Automated issue categorization
│   │   ├── claude-dedupe-issues.yml # Duplicate issue detection
│   │   ├── auto-close-duplicates.yml
│   │   ├── stale-issue-manager.yml
│   │   └── ... (5 more workflows)
│   └── ISSUE_TEMPLATE/               # GitHub issue forms
│
├── .vscode/
│   └── extensions.json               # Recommended VS Code extensions
│
├── examples/
│   └── hooks/
│       └── bash_command_validator_example.py  # Example PreToolUse hook
│
├── plugins/                          # Bundled plugin collection (5 plugins)
│   ├── agent-sdk-dev/                # Agent SDK scaffolding & verification
│   ├── pr-review-toolkit/            # 6-agent PR review system
│   ├── feature-dev/                  # Feature development workflow
│   ├── commit-commands/              # Git workflow commands
│   └── security-guidance/            # Security linting hooks
│
├── scripts/                          # Utility scripts (TypeScript)
│   ├── auto-close-duplicates.ts
│   └── backfill-duplicate-comments.ts
│
├── Script/                           # PowerShell scripts (Windows)
│   └── run_devcontainer_claude_code.ps1
│
├── CHANGELOG.md                      # Detailed release notes (777 lines, 30+ versions)
├── README.md                         # Project overview and quick start
├── SECURITY.md                       # Security policy
└── LICENSE.md                        # License information
```

### Key Directories

#### `/plugins/` - Bundled Plugins
Each plugin is self-contained with the following structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json                   # Plugin metadata (name, version, author)
├── commands/                         # Slash commands (*.md files)
├── agents/                           # Specialized agents (*.md files)
└── hooks/                            # Execution hooks (Python + hooks.json)
```

#### `/.claude/` - Repository Configuration
Contains commands and configuration specific to working on this repository itself.

#### `/.github/workflows/` - CI/CD Automation
Contains 10 GitHub Actions workflows for automated issue management, PR handling, and Claude integration.

---

## Plugin System Architecture

### Plugin Types and Categories

The Claude Code plugin system supports four categories:

1. **development** - Development tools and SDKs
2. **productivity** - Workflow automation and utilities
3. **security** - Security validation and guidance
4. **testing** - Test automation and quality assurance (not yet in use)

### Bundled Plugins Overview

#### 1. **agent-sdk-dev** (Development)
**Purpose**: Scaffolding and validation for Claude Agent SDK projects

**Components**:
- **Commands**:
  - `/new-sdk-app` - Interactive project generator for TypeScript/Python SDK apps
- **Agents**:
  - `agent-sdk-verifier-ts` - Validates TypeScript SDK setup
  - `agent-sdk-verifier-py` - Validates Python SDK setup

**Author**: Ashwin Bhat (ashwin@anthropic.com)

---

#### 2. **pr-review-toolkit** (Productivity)
**Purpose**: Comprehensive multi-agent PR review system

**Specialized Agents** (6 total):
1. `comment-analyzer` - Code comment accuracy and documentation quality
2. `pr-test-analyzer` - Test coverage and test quality assessment
3. `silent-failure-hunter` - Error handling and failure mode detection
4. `type-design-analyzer` - Type system design quality (rates 4 dimensions 1-10)
5. `code-reviewer` - General code quality and CLAUDE.md compliance
6. `code-simplifier` - Code clarity and refactoring suggestions

**Commands**:
- `/review-pr` - Triggers appropriate review agents based on request context

**Author**: Daisy (daisy@anthropic.com)

---

#### 3. **feature-dev** (Development)
**Purpose**: Systematic feature implementation with exploration and architecture design

**Workflow Phases**:
1. **Discovery** - Understand requirements and constraints
2. **Codebase Exploration** - Deep analysis of existing code
3. **Clarifying Questions** - Resolve ambiguities
4. **Architecture Design** - Multiple approaches with trade-offs
5. **Implementation** - Build with quality gates

**Specialized Agents** (3 total):
1. `code-explorer` (Sonnet, Yellow) - Traces execution paths, maps architecture
   - Tools: Glob, Grep, Read, WebFetch, TodoWrite, WebSearch
   - Outputs: Entry points, execution flows, dependencies, architecture insights

2. `code-architect` (Sonnet) - Designs feature architectures based on codebase patterns
   - Outputs: Architecture decisions, component design, implementation blueprint

3. `code-reviewer` (Sonnet) - Reviews code for bugs and guideline adherence
   - Uses confidence scoring (0-100), only reports issues >= 80 confidence

**Commands**:
- `/feature-dev` - Comprehensive feature development guide

**Author**: Siddharth Bidasaria (sbidasaria@anthropic.com)

---

#### 4. **commit-commands** (Productivity)
**Purpose**: Streamlined git and GitHub workflows

**Commands**:
- `/commit` - Create commits with automatic message generation
- `/commit-push-pr` - Atomic workflow: commit → push → create PR
- `/clean_gone` - Clean up stale branches marked as [gone]

**Allowed Tools**: Limited to git commands only (Bash with git restrictions)

**Author**: Anthropic team

---

#### 5. **security-guidance** (Security)
**Purpose**: Real-time security warnings during file editing

**Mechanism**: PreToolUse hook that triggers on Edit/Write/MultiEdit operations

**Implementation**:
- `hooks/security_reminder_hook.py` - Python validation script
- `hooks/hooks.json` - Hook configuration with matcher

**Detection Patterns**:
- Command injection vulnerabilities
- XSS (Cross-site scripting)
- Unsafe code patterns
- OWASP Top 10 vulnerabilities

**Author**: David Dworken (dworken@anthropic.com)

---

### Plugin Component Types

#### Agents (`.md` files in `agents/`)
Specialized AI assistants with specific focus areas.

**Agent File Format** (YAML frontmatter + Markdown):
```yaml
---
name: code-explorer
description: Deeply analyzes existing codebase features...
tools: Glob, Grep, Read, WebFetch, TodoWrite, WebSearch
model: sonnet
color: yellow
---

You are an expert code analyst...
[Agent instructions in markdown]
```

**Key Fields**:
- `name`: Agent identifier (kebab-case)
- `description`: What the agent does (shown in UI)
- `tools`: Comma-separated list of allowed tools
- `model`: AI model to use (sonnet, opus, haiku)
- `color`: UI color for visual distinction

**Available Tools for Agents**:
- `Glob` - File pattern matching
- `Grep` - Code search (ripgrep-based)
- `Read` - File reading
- `Write` - File writing
- `Edit` - File editing
- `Bash` - Shell commands (can be restricted to specific commands)
- `WebFetch` - Fetch web content
- `WebSearch` - Search the web
- `TodoWrite` - Task management
- `KillShell`, `BashOutput` - Background process management

---

#### Commands (`.md` files in `commands/`)
Slash commands that expand to prompts with context injection.

**Command File Format** (YAML frontmatter + Markdown):
```yaml
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Context
- Current git status: !`git status`
- Current git diff: !`git diff HEAD`

## Your task
Based on the above changes, create a single git commit.
```

**Key Fields**:
- `allowed-tools`: Restrict which tools can be used (security)
- `description`: Command description (shown in `/help`)

**Context Injection Syntax**:
- `!`command`` - Execute shell command and inject output
- Example: `` !`git status` `` becomes the output of `git status`

**Tool Restriction Format**:
- `Bash(git add:*)` - Allow only `git add` commands
- `Bash(gh issue view:*)` - Allow only `gh issue view` commands
- Multiple tools: `allowed-tools: Bash(git:*), Read, Grep`

---

#### Hooks (Python scripts + `hooks.json`)
Execute custom validation or modification logic before/after tool use.

**Hook Types**:
- `PreToolUse` - Run before tool execution (can block or modify)
- `PostToolUse` - Run after tool execution (can process results)

**Hook Configuration** (`hooks.json`):
```json
{
  "description": "Security reminder hook...",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/security_reminder_hook.py"
          }
        ]
      }
    ]
  }
}
```

**Hook Script Interface** (Python):
- **Input**: JSON via stdin with tool name and parameters
- **Output**: JSON via stdout (can modify parameters)
- **Exit Codes**:
  - `0` - Success, continue
  - `1` - Show stderr to user only (warning)
  - `2` - Block tool call (error)

**Example Hook Script**:
```python
#!/usr/bin/env python3
import json
import sys

# Read input
input_data = json.loads(sys.stdin.read())
tool_name = input_data.get("tool")
params = input_data.get("parameters", {})

# Validate
if needs_warning(params):
    print("Warning: Potential security issue", file=sys.stderr)
    sys.exit(1)  # Show warning but continue

# Optionally modify parameters
params["new_field"] = "value"
print(json.dumps(params))
sys.exit(0)
```

---

### Plugin Registry (`marketplace.json`)

Located at `.claude-plugin/marketplace.json`, this file registers all bundled plugins.

**Format**:
```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "claude-code-plugins",
  "version": "1.0.0",
  "description": "Bundled plugins for Claude Code...",
  "owner": {
    "name": "Anthropic",
    "email": "support@anthropic.com"
  },
  "plugins": [
    {
      "name": "agent-sdk-dev",
      "description": "Development kit for working with the Claude Agent SDK",
      "source": "./plugins/agent-sdk-dev",
      "category": "development"
    },
    ...
  ]
}
```

**Plugin Registration Fields**:
- `name`: Plugin identifier (must match directory name)
- `description`: User-facing description
- `source`: Relative path to plugin directory
- `category`: One of: development, productivity, security, testing
- `version`: Semantic version (optional)
- `author`: Author info (optional)

---

## Development Workflows

### Working on This Repository

#### Prerequisites
1. Node.js 20+
2. Git
3. Claude Code installed globally: `npm install -g @anthropic-ai/claude-code`

#### DevContainer Setup (Recommended)
The repository includes a DevContainer configuration for VS Code:

```bash
# Open in VS Code
code .

# VS Code will prompt to "Reopen in Container"
# This provides a consistent development environment
```

**DevContainer Features**:
- Node.js 20
- Git, GitHub CLI (gh)
- Claude Code pre-installed
- Zsh shell with fzf
- Persistent bash history

#### Local Development
```bash
# Clone the repository
git clone https://github.com/anthropics/claude-code.git
cd claude-code

# Explore plugins
ls -la plugins/

# Test a plugin locally
claude --plugin ./plugins/feature-dev

# Run repository commands
claude
> /dedupe 1234
> /commit-push-pr
```

### Creating a New Plugin

**Step 1: Create Plugin Directory**
```bash
mkdir -p plugins/my-plugin/.claude-plugin
mkdir -p plugins/my-plugin/commands
mkdir -p plugins/my-plugin/agents
mkdir -p plugins/my-plugin/hooks
```

**Step 2: Create `plugin.json`**
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Brief description of what this plugin does",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com"
  }
}
```

**Step 3: Add to Marketplace**
Edit `.claude-plugin/marketplace.json`:
```json
{
  "plugins": [
    ...existing plugins,
    {
      "name": "my-plugin",
      "description": "Brief description",
      "source": "./plugins/my-plugin",
      "category": "development"
    }
  ]
}
```

**Step 4: Create Commands or Agents**

Example command (`commands/my-command.md`):
```yaml
---
description: Does something useful
allowed-tools: Bash(git:*), Read, Grep
---

## Context
- Current directory: !`pwd`

## Task
Perform the requested operation...
```

Example agent (`agents/my-agent.md`):
```yaml
---
name: my-agent
description: Specialized agent for specific tasks
tools: Glob, Grep, Read, TodoWrite
model: sonnet
color: blue
---

You are an expert at [specific domain].

## Mission
[Agent's purpose and capabilities]

## Approach
[How the agent should work]
```

**Step 5: Validate Plugin**
```bash
claude
> /plugin validate ./plugins/my-plugin
```

### Adding Repository Commands

Repository-level commands go in `.claude/commands/`:

```bash
# Create a new command
cat > .claude/commands/my-command.md << 'EOF'
---
description: Brief description
allowed-tools: Bash(git:*)
---

Perform task...
EOF

# Test it
claude
> /my-command
```

---

## Code Conventions

### General Principles

1. **Quality Over Quantity** - Focus on correct, clear code over extensive code
2. **Minimal Changes** - Only modify what's necessary for the task
3. **No Over-Engineering** - Avoid premature abstractions or unnecessary features
4. **Security First** - Always check for OWASP Top 10 vulnerabilities
5. **Confidence-Based Reporting** - Only report issues with >= 80% confidence

### File Naming

- **Commands**: `kebab-case.md` (e.g., `commit-push-pr.md`)
- **Agents**: `kebab-case.md` (e.g., `code-explorer.md`)
- **Hooks**: `snake_case.py` (e.g., `security_reminder_hook.py`)
- **Scripts**: `kebab-case.ts` or `snake_case.py`

### Markdown Format

All agent and command files use YAML frontmatter + Markdown:

```markdown
---
key: value
---

# Heading

Content...
```

### Tool Restrictions

When limiting tools in commands, use the format:
```yaml
allowed-tools: Bash(git:*), Bash(gh:*), Read, Grep
```

**Security Note**: Always restrict tools in commands to prevent misuse. Never allow unrestricted `Bash` access.

### Agent Configurations

**Model Selection**:
- `sonnet` - Default for most agents (balanced performance)
- `opus` - For complex reasoning or architecture design
- `haiku` - For quick, simple tasks (cost-effective)

**Color Options**:
- `yellow`, `blue`, `green`, `red`, `purple`, `cyan`, `magenta`
- Used for visual distinction in UI

### Git Conventions

**Commit Messages**:
- Follow repository's existing commit style (check recent commits)
- Focus on "why" rather than "what"
- Format: `type: Brief description`
- Types: `feat:`, `fix:`, `refactor:`, `chore:`, `docs:`

**Examples from Repository**:
```
chore: Update CHANGELOG.md
feat: add security-guidance plugin to marketplace.json
refactor: Update agent-sdk-dev plugin structure
```

**Branch Naming**:
- Feature branches: `claude/descriptive-name-sessionid`
- Always include session ID for authentication
- Never push to `main` or `master` without permission

---

## Testing and Quality

### Quality Assurance Approach

This repository uses **agent-based quality assurance** rather than traditional unit tests:

1. **Code Review Agents** - Specialized agents review code changes
2. **Confidence Scoring** - Only report issues with >= 80% confidence
3. **Multiple Perspectives** - Different agents focus on different quality aspects
4. **Continuous Validation** - Hooks provide real-time validation

### Review Dimensions (from pr-review-toolkit)

1. **Documentation Quality** (comment-analyzer)
   - Code comment accuracy
   - Documentation completeness
   - Explanation clarity

2. **Test Coverage** (pr-test-analyzer)
   - Test completeness
   - Edge case coverage
   - Test quality and maintainability

3. **Error Handling** (silent-failure-hunter)
   - Failure mode detection
   - Error propagation analysis
   - Silent failure prevention

4. **Type Design** (type-design-analyzer)
   - Type safety
   - API design quality
   - Type system effectiveness

5. **Code Quality** (code-reviewer)
   - CLAUDE.md compliance
   - Code clarity
   - Best practices adherence

6. **Simplicity** (code-simplifier)
   - Code complexity
   - Refactoring opportunities
   - Clarity improvements

### Validation Commands

**TypeScript Type Checking**:
```bash
npx tsc --noEmit
```

**Plugin Validation**:
```bash
claude
> /plugin validate ./plugins/my-plugin
```

**Agent SDK Verification** (for SDK projects):
```bash
claude
> @agent-sdk-verifier-ts
> @agent-sdk-verifier-py
```

### Security Validation

The `security-guidance` plugin automatically checks for:
- Command injection
- XSS vulnerabilities
- SQL injection
- Unsafe eval/exec usage
- OWASP Top 10 patterns

**Triggered On**:
- `Edit` tool usage
- `Write` tool usage
- `MultiEdit` tool usage

---

## Git Workflow

### Standard Development Flow

1. **Create Feature Branch**
   ```bash
   git checkout -b claude/feature-name-sessionid
   ```

2. **Make Changes**
   - Edit files as needed
   - Follow code conventions
   - Run validation

3. **Commit Changes** (using `/commit` command)
   ```bash
   claude
   > /commit
   ```
   - Automatically stages relevant files
   - Generates commit message from changes
   - Follows repository commit style

4. **Push and Create PR** (using `/commit-push-pr` command)
   ```bash
   claude
   > /commit-push-pr
   ```
   - Creates commit
   - Pushes to remote
   - Creates GitHub PR with summary
   - Includes test plan

### Git Command Patterns

**Status Checking**:
```bash
git status
git diff HEAD
git log --oneline -10
```

**Branch Management**:
```bash
git branch --show-current
git fetch origin branch-name
git pull origin branch-name
```

**Commit Creation** (via command):
```bash
# Stage files
git add file1.md file2.ts

# Commit with heredoc for formatting
git commit -m "$(cat <<'EOF'
feat: Add new feature

Detailed description here.
EOF
)"
```

**Push with Retries** (network failure handling):
```bash
# Always use -u flag for new branches
git push -u origin claude/branch-name-sessionid

# Retry logic: 2s, 4s, 8s, 16s exponential backoff
```

### GitHub PR Workflow

**PR Creation Using `gh` CLI**:
```bash
# Create branch and push
git checkout -b claude/feature-sessionid
git push -u origin claude/feature-sessionid

# Create PR with body
gh pr create --title "Feature title" --body "$(cat <<'EOF'
## Summary
- Bullet point 1
- Bullet point 2

## Test plan
- [ ] Test item 1
- [ ] Test item 2
EOF
)"
```

**PR Review Process**:
1. PR created automatically triggers GitHub Actions
2. Can manually trigger reviews: `@claude review this PR`
3. Review agents analyze changes
4. Feedback provided as PR comments

### Branch Cleanup

```bash
claude
> /clean_gone
```

Removes local branches that are:
- Marked as `[gone]` (deleted on remote)
- Already merged
- No longer needed

---

## GitHub Automation

### GitHub Actions Workflows (10 total)

Located in `.github/workflows/`:

#### 1. **claude.yml** - Main Claude Integration
**Trigger**: `@claude` mentions on issues or PRs
**Function**: Invokes Claude Code to respond to requests
**Use Case**: `@claude fix this bug`, `@claude review this PR`

#### 2. **claude-issue-triage.yml** - Issue Categorization
**Trigger**: New issues opened
**Function**: Automatically categorizes and labels issues
**Labels**: bug, feature-request, question, documentation, etc.

#### 3. **claude-dedupe-issues.yml** - Duplicate Detection
**Trigger**: New issues opened
**Function**: Finds potential duplicate issues using specialized search
**Process**:
1. Summarize new issue
2. Run 5 parallel searches with diverse keywords
3. Filter false positives
4. Comment with up to 3 duplicates
5. Auto-close in 3 days if not disputed

#### 4. **auto-close-duplicates.yml** - Duplicate Closure
**Trigger**: Scheduled (cron)
**Function**: Closes issues marked as duplicates after 3 days
**Conditions**: No disputes (reactions or comments)

#### 5. **stale-issue-manager.yml** - Stale Issue Handling
**Trigger**: Scheduled (cron)
**Function**: Marks and closes stale issues
**Workflow**:
- Mark stale after 60 days of inactivity
- Close after additional 7 days
- Exclude labeled issues

#### 6. **lock-closed-issues.yml** - Issue Locking
**Trigger**: Scheduled (cron)
**Function**: Locks resolved issues to prevent necro-posting
**Timing**: 30 days after closure

#### 7-10. **Supporting Workflows**
- `issue-opened-dispatch.yml` - Dispatch event for new issues
- `log-issue-events.yml` - Issue event logging for analytics
- `remove-autoclose-label.yml` - Remove auto-close labels on activity
- `backfill-duplicate-comments.yml` - Backfill duplicate detection

### Automation Scripts

Located in `scripts/`:

#### `auto-close-duplicates.ts`
TypeScript script for automated duplicate closure logic.

#### `backfill-duplicate-comments.ts`
TypeScript script to backfill duplicate comments on existing issues.

### Using GitHub Automation

**Trigger Claude on Issues**:
```
@claude can you help me understand this error?
@claude please analyze this feature request
```

**Trigger Claude on PRs**:
```
@claude review this PR
@claude check for security issues
```

**Manual Issue Deduplication**:
```bash
claude
> /dedupe 1234
```

---

## Plugin Development Guide

### Plugin Architecture Patterns

#### 1. **Single-Purpose Commands**
Simple commands that perform one task.

**Example**: `/commit` command
```yaml
---
allowed-tools: Bash(git:*)
description: Create a git commit
---

Based on git status and diff, create a commit.
Do not use any other tools.
```

**Best For**:
- Git operations
- Simple file operations
- Quick utilities

---

#### 2. **Multi-Agent Workflows**
Commands that orchestrate multiple specialized agents.

**Example**: `/dedupe` command
```markdown
1. Use agent to check if issue is closed/needs deduping
2. Use agent to view and summarize issue
3. Launch 5 parallel agents to search for duplicates
4. Use agent to filter false positives
5. Comment with results
```

**Best For**:
- Complex analysis tasks
- Research workflows
- Quality assurance

---

#### 3. **Exploration + Architecture + Implementation**
Feature development pattern with phases.

**Example**: `feature-dev` plugin
```
Phase 1: code-explorer agent - Understand codebase
Phase 2: code-architect agent - Design solution
Phase 3: code-reviewer agent - Validate implementation
```

**Best For**:
- Feature development
- Large refactorings
- System redesigns

---

#### 4. **Hook-Based Validation**
Real-time validation during tool use.

**Example**: `security-guidance` plugin
```python
# PreToolUse hook on Edit/Write
if contains_vulnerability(code):
    print("Warning: XSS risk", file=sys.stderr)
    sys.exit(1)  # Show warning
```

**Best For**:
- Security checks
- Policy enforcement
- Code standards

---

### Agent Design Patterns

#### Pattern 1: Explorer Agent
**Purpose**: Deep codebase analysis
**Model**: Sonnet (balanced)
**Tools**: Glob, Grep, Read, WebSearch

**Template**:
```yaml
---
name: explorer-agent
description: Explores and maps codebase structure
tools: Glob, Grep, Read, WebSearch, TodoWrite
model: sonnet
color: yellow
---

You are an expert code analyst.

## Mission
Understand how [feature/pattern] works in this codebase.

## Approach
1. Find entry points
2. Trace execution flow
3. Map dependencies
4. Document architecture

## Output
- Entry points (file:line)
- Execution flow
- Key components
- Dependencies
- Observations
```

---

#### Pattern 2: Architect Agent
**Purpose**: Design solutions based on codebase patterns
**Model**: Opus (complex reasoning)
**Tools**: Read, TodoWrite

**Template**:
```yaml
---
name: architect-agent
description: Designs architecture following codebase patterns
tools: Read, TodoWrite
model: opus
color: blue
---

You are an expert software architect.

## Mission
Design [feature] that fits naturally into this codebase.

## Approach
1. Understand existing patterns
2. Propose 2-3 approaches with trade-offs
3. Recommend best approach
4. Create implementation blueprint

## Output
- Architecture decision rationale
- Component design
- Data flow
- Integration points
```

---

#### Pattern 3: Reviewer Agent
**Purpose**: Quality assurance with confidence scoring
**Model**: Sonnet
**Tools**: Read, Grep

**Template**:
```yaml
---
name: reviewer-agent
description: Reviews code for bugs and guideline compliance
tools: Read, Grep
model: sonnet
color: red
---

You are an expert code reviewer.

## Mission
Review code for bugs and CLAUDE.md compliance.

## Approach
1. Read changed files
2. Check for common issues
3. Score confidence (0-100)
4. Only report if confidence >= 80

## Output Format
**Issue**: [Brief description]
**Confidence**: [0-100]
**Location**: file:line
**Recommendation**: [How to fix]
```

---

### Hook Development Patterns

#### Pattern 1: Validation Hook
**Purpose**: Block invalid tool calls

```python
#!/usr/bin/env python3
import json
import sys

def validate(tool, params):
    """Return (is_valid, error_message)"""
    if tool == "Bash":
        command = params.get("command", "")
        if "rm -rf /" in command:
            return False, "Dangerous command blocked"
    return True, None

def main():
    input_data = json.loads(sys.stdin.read())
    is_valid, error = validate(input_data["tool"], input_data["parameters"])

    if not is_valid:
        print(error, file=sys.stderr)
        sys.exit(2)  # Block

    print(json.dumps(input_data["parameters"]))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

---

#### Pattern 2: Warning Hook
**Purpose**: Show warnings but allow execution

```python
def check_for_issues(params):
    """Return list of warnings"""
    warnings = []
    if "password" in params.get("file_path", ""):
        warnings.append("Editing password file")
    return warnings

def main():
    input_data = json.loads(sys.stdin.read())
    warnings = check_for_issues(input_data["parameters"])

    if warnings:
        for w in warnings:
            print(f"Warning: {w}", file=sys.stderr)
        sys.exit(1)  # Warn but continue

    print(json.dumps(input_data["parameters"]))
    sys.exit(0)
```

---

#### Pattern 3: Modification Hook
**Purpose**: Modify tool parameters before execution

```python
def modify_params(tool, params):
    """Return modified parameters"""
    if tool == "Bash" and "grep" in params.get("command", ""):
        # Replace grep with rg
        params["command"] = params["command"].replace("grep", "rg")
    return params

def main():
    input_data = json.loads(sys.stdin.read())
    modified = modify_params(input_data["tool"], input_data["parameters"])

    print(json.dumps(modified))
    sys.exit(0)
```

---

### Command Development Patterns

#### Pattern 1: Context-Rich Command
Inject git context for git operations.

```yaml
---
allowed-tools: Bash(git:*)
description: Git operation with full context
---

## Context
- Current branch: !`git branch --show-current`
- Status: !`git status`
- Recent commits: !`git log --oneline -10`

## Task
Perform git operation based on above context.
```

---

#### Pattern 2: Restricted Tool Command
Limit tools to specific operations.

```yaml
---
allowed-tools: Bash(gh issue view:*), Bash(gh api:*), Read
description: GitHub issue analysis
---

Analyze the GitHub issue using ONLY gh commands and Read.
Do not use other tools.
```

---

#### Pattern 3: Multi-Step Workflow Command
Orchestrate agents for complex workflows.

```yaml
---
allowed-tools: Task, TodoWrite
description: Complex multi-agent workflow
---

1. Use TodoWrite to create task list
2. Launch explorer agent to analyze codebase
3. Launch architect agent to design solution
4. Launch reviewer agent to validate
5. Mark tasks complete as you go
```

---

## Common Patterns

### Code Reference Format

When referencing code locations, always use `file:line` format:

```
The bug is in src/main.ts:42
See the implementation in lib/parser.ts:156-178
```

This allows users to click and navigate directly to the code.

### Confidence Scoring

When reporting issues or making suggestions, use confidence scoring:

```
**Issue**: Potential null pointer dereference
**Confidence**: 85
**Location**: src/app.ts:23
**Recommendation**: Add null check before accessing property
```

Only report issues with confidence >= 80.

### Tool Usage Patterns

#### File Discovery
```yaml
# Use Glob for pattern matching
tools: Glob
---
Find all TypeScript files: *.ts
Find all test files: **/*.test.ts
```

#### Code Search
```yaml
# Use Grep for content search
tools: Grep
---
Search for function: pattern="function processData"
Search with context: -A 5 -B 5 pattern="TODO"
```

#### File Reading
```yaml
# Use Read for file contents
tools: Read
---
Read entire file: file_path="/path/to/file.ts"
Read section: file_path="/path" offset=100 limit=50
```

### Task Management with TodoWrite

Always use TodoWrite for multi-step tasks:

```markdown
1. Create todo list at start
2. Mark task as in_progress before starting
3. Mark as completed immediately after finishing
4. Add new tasks as discovered
5. Keep exactly ONE task in_progress at a time
```

**Example**:
```json
[
  {"content": "Analyze codebase", "status": "completed", "activeForm": "Analyzing codebase"},
  {"content": "Design solution", "status": "in_progress", "activeForm": "Designing solution"},
  {"content": "Implement feature", "status": "pending", "activeForm": "Implementing feature"},
  {"content": "Write tests", "status": "pending", "activeForm": "Writing tests"}
]
```

### Agent Collaboration

When multiple agents work together:

1. **Sequential**: One agent's output feeds the next
   ```
   explorer → architect → implementer → reviewer
   ```

2. **Parallel**: Multiple agents run simultaneously
   ```
   5 search agents all looking for duplicates with different keywords
   ```

3. **Hierarchical**: Coordinator agent manages sub-agents
   ```
   dedupe command → view agent → search agents → filter agent → comment
   ```

---

## Important Files and Locations

### Configuration Files

| File | Purpose | Format |
|------|---------|--------|
| `.claude-plugin/marketplace.json` | Plugin registry | JSON |
| `plugins/*/.claude-plugin/plugin.json` | Plugin metadata | JSON |
| `plugins/*/hooks/hooks.json` | Hook configuration | JSON |
| `.devcontainer/devcontainer.json` | DevContainer config | JSON |
| `.vscode/extensions.json` | VS Code extensions | JSON |

### Documentation Files

| File | Purpose | Lines |
|------|---------|-------|
| `README.md` | Quick start guide | 43 |
| `CHANGELOG.md` | Release history | 777 |
| `SECURITY.md` | Security policy | Short |
| `CLAUDE.md` (this file) | AI assistant guide | Comprehensive |

### Plugin Files

#### Agent SDK Dev Plugin
```
plugins/agent-sdk-dev/
├── .claude-plugin/plugin.json
├── commands/new-sdk-app.md
└── agents/
    ├── agent-sdk-verifier-ts.md
    └── agent-sdk-verifier-py.md
```

#### PR Review Toolkit Plugin
```
plugins/pr-review-toolkit/
├── .claude-plugin/plugin.json
├── commands/review-pr.md
└── agents/
    ├── comment-analyzer.md
    ├── pr-test-analyzer.md
    ├── silent-failure-hunter.md
    ├── type-design-analyzer.md
    ├── code-reviewer.md
    └── code-simplifier.md
```

#### Feature Dev Plugin
```
plugins/feature-dev/
├── .claude-plugin/plugin.json
├── commands/feature-dev.md
└── agents/
    ├── code-explorer.md
    ├── code-architect.md
    └── code-reviewer.md
```

#### Commit Commands Plugin
```
plugins/commit-commands/
├── .claude-plugin/plugin.json
└── commands/
    ├── commit.md
    ├── commit-push-pr.md
    └── clean_gone.md
```

#### Security Guidance Plugin
```
plugins/security-guidance/
├── .claude-plugin/plugin.json
└── hooks/
    ├── hooks.json
    └── security_reminder_hook.py
```

### GitHub Automation Files

```
.github/
├── workflows/
│   ├── claude.yml                    # @claude mentions
│   ├── claude-issue-triage.yml      # Auto-categorization
│   ├── claude-dedupe-issues.yml     # Duplicate detection
│   ├── auto-close-duplicates.yml    # Auto-close duplicates
│   ├── stale-issue-manager.yml      # Stale issue handling
│   ├── lock-closed-issues.yml       # Lock old issues
│   ├── issue-opened-dispatch.yml    # Dispatch events
│   ├── log-issue-events.yml         # Event logging
│   ├── remove-autoclose-label.yml   # Label management
│   └── backfill-duplicate-comments.yml
└── ISSUE_TEMPLATE/                   # Issue forms
```

---

## Resources

### Official Documentation

- **Claude Code Overview**: https://docs.anthropic.com/en/docs/claude-code/overview
- **Plugin System**: https://docs.anthropic.com/en/docs/claude-code/plugins
- **Hooks Guide**: https://docs.anthropic.com/en/docs/claude-code/hooks
- **Agent SDK**: https://docs.anthropic.com/en/docs/claude-code/agent-sdk
- **Plugin Announcement**: https://www.anthropic.com/news/claude-code-plugins

### Community

- **Discord**: https://anthropic.com/discord (Claude Developers community)
- **GitHub Issues**: https://github.com/anthropics/claude-code/issues
- **Bug Reports**: Use `/bug` command in Claude Code

### Package Information

- **NPM Package**: `@anthropic-ai/claude-code`
- **NPM URL**: https://www.npmjs.com/package/@anthropic-ai/claude-code
- **Current Version**: 2.0.13

### Related Repositories

- **Claude Agent SDK**: For building custom AI-powered applications
- **MCP (Model Context Protocol)**: For building context servers

### Development Tools

**Recommended VS Code Extensions** (from `.vscode/extensions.json`):
- GitLens
- ESLint
- Prettier
- Other extensions as specified in the file

**Command Line Tools**:
- `gh` (GitHub CLI) - For GitHub operations
- `git` - Version control
- `rg` (ripgrep) - Fast code search
- `jq` - JSON processing
- `fzf` - Fuzzy finder

### Getting Help

1. **In Claude Code**: Use `/help` command
2. **Diagnostics**: Use `/doctor` command
3. **Bug Reports**: Use `/bug` command or file GitHub issue
4. **Discord**: Join Claude Developers Discord for community support
5. **Documentation**: Check official docs at docs.anthropic.com

---

## Appendix: Quick Reference

### Essential Commands

```bash
# Plugin management
/plugin install <name>
/plugin enable <name>
/plugin disable <name>
/plugin marketplace
/plugin validate <path>

# Git workflows (from commit-commands plugin)
/commit
/commit-push-pr
/clean_gone

# Repository commands
/dedupe <issue-number>

# Feature development (from feature-dev plugin)
/feature-dev

# PR review (from pr-review-toolkit plugin)
/review-pr

# Agent SDK (from agent-sdk-dev plugin)
/new-sdk-app
@agent-sdk-verifier-ts
@agent-sdk-verifier-py

# System commands
/help
/doctor
/bug
/model
/context
/permissions
```

### Directory Quick Reference

```
Repository Root
├── .claude/              → Repo commands
├── .claude-plugin/       → Plugin registry
├── .github/workflows/    → Automation
├── plugins/              → Bundled plugins
│   ├── agent-sdk-dev/    → SDK tools
│   ├── pr-review-toolkit/ → PR reviews
│   ├── feature-dev/      → Feature workflow
│   ├── commit-commands/  → Git commands
│   └── security-guidance/ → Security hooks
├── examples/hooks/       → Hook examples
└── scripts/              → Utilities
```

### Plugin Component Reference

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json       → Metadata
├── commands/
│   └── *.md              → Slash commands
├── agents/
│   └── *.md              → Specialized agents
└── hooks/
    ├── hooks.json        → Hook config
    └── *.py              → Hook scripts
```

---

**End of CLAUDE.md**

*This document is maintained by the Claude Code team and community contributors. For updates or corrections, please submit a PR or file an issue.*
