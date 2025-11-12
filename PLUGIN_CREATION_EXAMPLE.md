# Example: Creating a Plugin with the Deployment Script

This is a practical walkthrough of creating a plugin for Claude Code using the new deployment script.

## Scenario: Creating a "Code Quality" Plugin

Let's create a plugin that helps developers improve code quality.

---

## Step 1: Run the Deployment Script

```bash
cd /path/to/claude-code
./scripts/deploy-claude-code.sh
```

**Select Option 1:** Create new plugin

---

## Step 2: Enter Plugin Details

```
Plugin name (e.g., my-awesome-plugin): code-quality
Plugin display name: Code Quality Analyzer
Plugin description: Automated code quality checks and suggestions
```

The script creates:
```
plugins/code-quality/
├── README.md
├── commands/
│   └── example.md
└── agents/
    └── example-agent.md
```

---

## Step 3: Customize the Plugin

### Edit: `plugins/code-quality/commands/quality-check.md`

```markdown
---
name: quality-check
description: Run code quality analysis on current file or project
---

# Code Quality Check

Analyze the code for quality issues and provide suggestions.

## What to Check

1. **Code Complexity**
   - Long functions (>50 lines)
   - Deep nesting (>3 levels)
   - High cyclomatic complexity

2. **Code Smells**
   - Duplicate code
   - Magic numbers
   - Poor naming
   - Missing error handling

3. **Best Practices**
   - Proper error handling
   - Type safety
   - Documentation
   - Test coverage

## Output Format

Provide a report with:
- Issues found (severity: high/medium/low)
- Specific line numbers
- Suggested fixes
- Code examples

## Example Usage

\`\`\`bash
claude
> /quality-check src/utils/helper.js
\`\`\`
```

### Edit: `plugins/code-quality/agents/refactor-advisor.md`

```markdown
---
name: refactor-advisor
description: Suggests refactoring opportunities for better code quality
model: sonnet
---

# Refactor Advisor Agent

An AI agent that identifies refactoring opportunities and guides developers through code improvements.

## Capabilities

1. **Identify Refactoring Opportunities**
   - Extract method
   - Extract class
   - Rename for clarity
   - Simplify conditionals
   - Remove duplication

2. **Provide Context-Aware Suggestions**
   - Consider project patterns
   - Maintain consistency
   - Preserve functionality

3. **Guide Implementation**
   - Step-by-step refactoring
   - Safe transformation
   - Automated testing

## When Activated

This agent activates when:
- User requests code refactoring
- Quality issues are detected
- Code review suggests improvements
- Developer asks for best practices

## Interaction Style

- Explain WHY refactoring is beneficial
- Show BEFORE and AFTER code
- Provide migration path
- Consider trade-offs
```

---

## Step 4: Test the Plugin Locally

```bash
# Link to Claude Code
mkdir -p ~/.claude/plugins
ln -s $(pwd)/plugins/code-quality ~/.claude/plugins/

# Test in a project
cd ~/my-project
claude
```

**Try the command:**
```
> /quality-check src/app.js
```

**The agent activates automatically when you say:**
```
> Can you help me refactor this messy function?
```

---

## Step 5: Validate Plugin Structure

Run the deployment script again:
```bash
./scripts/deploy-claude-code.sh
```

**Select Option 5:** Validate plugin structure

Output:
```
Validating: code-quality
✅ Plugin structure valid
```

---

## Step 6: Add to Marketplace

### Manual Method (Recommended)

Edit `.claude-plugin/marketplace.json`:

```json
{
  "plugins": [
    {
      "name": "code-quality",
      "description": "Automated code quality checks and suggestions",
      "category": "development",
      "source": "./plugins/code-quality",
      "version": "1.0.0",
      "author": "Your Name",
      "license": "MIT"
    }
  ]
}
```

### Script-Assisted Method

```bash
./scripts/deploy-claude-code.sh
# Select Option 2: Add plugin to marketplace
```

Follow the prompts and it will show you what to add.

---

## Step 7: Create Documentation

```bash
./scripts/deploy-claude-code.sh
# Select Option 12: Generate plugin documentation
```

This creates `PLUGINS.md` with documentation for all plugins.

---

## Step 8: Submit to Repository

```bash
# Create a new branch
git checkout -b add-code-quality-plugin

# Add your changes
git add plugins/code-quality .claude-plugin/marketplace.json

# Commit
git commit -m "feat: Add code-quality plugin for automated code analysis"

# Push
git push origin add-code-quality-plugin

# Create PR on GitHub
```

---

## Real-World Usage Examples

### Example 1: Quick Quality Check

```bash
cd my-project
claude
> /quality-check
```

**Output:**
```
📊 Code Quality Report

HIGH PRIORITY:
  src/utils/parser.js:45 - Function too complex (complexity: 12)
  src/api/routes.js:89 - Missing error handling

MEDIUM PRIORITY:
  src/helpers/format.js:23 - Magic number 3.14159 should be a constant
  src/components/Form.js:67 - Duplicate code block (also in Form2.js:45)

LOW PRIORITY:
  src/index.js:12 - Consider using const instead of let

✅ 23 files checked
⚠️  5 issues found
```

### Example 2: Interactive Refactoring

```bash
claude
> This function is getting too long. Can you help me refactor it?
```

**Agent Response:**
```
I'll help you refactor this function. I see it's doing multiple things:

1. Validation (lines 12-34)
2. Data transformation (lines 35-56)
3. API calls (lines 57-89)
4. Error handling (lines 90-102)

Let me break this into smaller, focused functions:

BEFORE (103 lines):
[shows current code]

AFTER (4 functions, ~25 lines each):
[shows refactored code with explanations]

Would you like me to apply these changes?
```

### Example 3: Project-Wide Analysis

```bash
claude
> Analyze the entire codebase for quality issues
```

**Agent Response:**
```
🔍 Analyzing 47 files...

Top Issues:
1. Duplicate code in auth/ directory (3 files)
2. Missing error handling in 12 API endpoints
3. Complex functions in utils/ (avg complexity: 8.2)

Detailed Report:
- Generated: quality-report.md
- Actionable items: 34
- Estimated time to fix: 4-6 hours

Shall I create a prioritized task list?
```

---

## Advanced Features You Could Add

### 1. Configuration File

Create `plugins/code-quality/config.yaml`:

```yaml
rules:
  max_function_length: 50
  max_complexity: 10
  max_nesting: 3
  require_types: true
  require_tests: true

ignore_patterns:
  - "*.test.js"
  - "*.spec.js"
  - "node_modules/**"

severity_levels:
  missing_error_handling: high
  magic_numbers: medium
  naming_conventions: low
```

### 2. Integration with Tools

```markdown
## Tool Integration

This plugin can integrate with:
- ESLint for JavaScript/TypeScript
- Pylint for Python
- RuboCop for Ruby
- SonarQube for enterprise
```

### 3. Custom Rules

Allow users to define custom quality rules in `.claude/quality-rules.js`

---

## Benefits of This Approach

✅ **Interactive Development**
- Create plugins without manual setup
- Guided workflow
- Instant validation

✅ **Proper Structure**
- Follows Claude Code conventions
- Validated before submission
- Consistent naming

✅ **Easy Testing**
- Local testing before publishing
- No need for complex setup
- Fast iteration

✅ **Clear Documentation**
- Auto-generated docs
- Examples included
- User-friendly guides

---

## Next Steps

1. **Enhance Your Plugin**
   - Add more commands
   - Create specialized agents
   - Add configuration options

2. **Test Thoroughly**
   - Try different scenarios
   - Get feedback from users
   - Fix edge cases

3. **Share with Community**
   - Submit PR to marketplace
   - Write blog post
   - Demo on Discord

4. **Iterate and Improve**
   - Monitor usage
   - Gather feedback
   - Release updates

---

## Complete Plugin Structure

Final structure for `code-quality` plugin:

```
plugins/code-quality/
├── README.md                     # Plugin documentation
├── config.yaml                   # Configuration (optional)
├── commands/
│   ├── quality-check.md         # Quick quality scan
│   ├── complexity-report.md     # Detailed complexity analysis
│   └── refactor-suggest.md      # Refactoring suggestions
├── agents/
│   ├── refactor-advisor.md      # Interactive refactoring
│   ├── code-reviewer.md         # Code review agent
│   └── quality-coach.md         # Teaching best practices
└── examples/
    ├── before-after.md          # Refactoring examples
    └── best-practices.md        # Quality guidelines
```

---

## Resources

- **Script Location**: `scripts/deploy-claude-code.sh`
- **Documentation**: `DEPLOYMENT_README.md`
- **Quick Start**: `DEPLOYMENT_QUICKSTART.md`
- **Plugin Examples**: `plugins/` directory

---

## Troubleshooting

**Plugin not showing up?**
```bash
# Check symlink
ls -la ~/.claude/plugins/

# Re-link if needed
rm ~/.claude/plugins/code-quality
ln -s $(pwd)/plugins/code-quality ~/.claude/plugins/
```

**Commands not working?**
```bash
# Validate structure
./scripts/deploy-claude-code.sh
# Select Option 5
```

**Want to start over?**
```bash
# Remove plugin
rm -rf plugins/code-quality

# Create again
./scripts/deploy-claude-code.sh
# Select Option 1
```

---

**That's it! You've created a complete Claude Code plugin.** 🎉
