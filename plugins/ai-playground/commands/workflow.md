---
description: Build and orchestrate multi-tool AI workflows
argument-hint: "[workflow name or description]"
allowed-tools:
  - Task:*
  - Read:**/*
  - Write:**/*
  - Grep:**/*
  - WebFetch:*
---

# Workflow Automation Builder Command

Build and orchestrate sophisticated multi-tool AI workflows using visual node-based architecture inspired by n8n and Zapier.

## Usage

```bash
/workflow [description or template name]
```

## Examples

```bash
# Create custom workflow
/workflow content creation pipeline
/workflow automated code review system
/workflow customer support automation
/workflow social media content generator

# Use pre-built templates
/workflow template:content-creation
/workflow template:code-review
/workflow template:data-processing
/workflow template:support-automation
/workflow template:social-media

# Explore workflow patterns
/workflow show patterns
/workflow show templates
```

## How It Works

This command launches the **workflow-builder** agent which:

1. **Understands Your Requirements**
   - Analyzes your workflow description
   - Identifies required capabilities
   - Maps to appropriate AI tools
   - Determines workflow pattern

2. **Designs Workflow Architecture**
   - Selects optimal workflow pattern (linear, fan-out, conditional, etc.)
   - Chooses appropriate tools for each step
   - Plans data transformations
   - Designs error handling strategy

3. **Creates Workflow Definition**
   - Generates JSON/YAML workflow specification
   - Defines triggers and event handlers
   - Configures tool integrations
   - Sets up monitoring and logging

4. **Provides Implementation Guidance**
   - Step-by-step setup instructions
   - Integration code examples
   - Testing procedures
   - Deployment recommendations

## Workflow Architecture Patterns

### 1. Linear Pipeline
Sequential execution where output of one tool feeds next tool.

```
[Trigger] → [Tool 1] → [Transform] → [Tool 2] → [Output]
```

**Best for**: Simple sequential processes, content creation, data transformation

### 2. Fan-Out / Fan-In
Parallel processing that converges to single output.

```
         ┌─→ [Tool 1] ─┐
[Trigger]├─→ [Tool 2] ─┤→ [Aggregator] → [Output]
         └─→ [Tool 3] ─┘
```

**Best for**: Multi-model analysis, consensus building, redundancy

### 3. Conditional Branching
Dynamic routing based on conditions or outputs.

```
              ┌─→ [Path A] → [Output A]
[Trigger] → [Decision] ┼─→ [Path B] → [Output B]
              └─→ [Path C] → [Output C]
```

**Best for**: Content moderation, smart routing, adaptive workflows

### 4. Loop with Accumulation
Iterative processing until condition met.

```
[Trigger] → [Loop] → [Process] → [Check] ─┬─→ [Output]
               ↑                           │
               └───────── NO ←─────────────┘
```

**Best for**: Iterative refinement, quality improvement, batch processing

### 5. Event-Driven Reactive
Multiple triggers feeding same workflow.

```
[Trigger A] ─┐
[Trigger B] ─┼─→ [Workflow] → [Output]
[Trigger C] ─┘
```

**Best for**: Multi-source aggregation, reactive systems, monitoring

## Pre-built Workflow Templates

### Template 1: Content Creation Pipeline
```yaml
Name: AI Content Creation Pipeline
Trigger: User input (topic + keywords)
Duration: 5-10 minutes
Cost: $0.50-$2.00

Steps:
1. Content Outline (Claude API)
   - Generate structured outline
   - Extract main sections

2. Section Writing (Claude API - Loop)
   - Write each section
   - Identify image opportunities

3. Image Generation (FLUX.1)
   - Generate relevant images
   - Optimize and format

4. Assembly
   - Combine text + images
   - Format as HTML/Markdown

Tools: Claude API, FLUX.1 Schnell
```

### Template 2: Automated Code Review
```yaml
Name: Multi-Agent Code Review Workflow
Trigger: GitHub PR created
Duration: 2-5 minutes
Cost: $0.10-$0.50

Steps:
1. Fetch PR (GitHub API)
   - Get diff and changed files

2. Parallel Analysis:
   a. Code Quality (Claude)
   b. Security Scan (Custom)
   c. Test Coverage (Qodo)

3. Aggregate Results
   - Combine analyses
   - Prioritize issues

4. Post Review (GitHub API)
   - Create comments
   - Update PR status

Tools: GitHub API, Claude, Qodo
```

### Template 3: Data Processing Pipeline
```yaml
Name: Multi-Source Data Analysis
Trigger: Daily schedule (9 AM)
Duration: 10-20 minutes
Cost: $1-$3

Steps:
1. Data Collection (Parallel):
   - Fetch API data
   - Scrape web data
   - Query database

2. Data Normalization
   - Convert to common format
   - Clean and validate

3. AI Analysis (Llama 3.1)
   - Identify patterns
   - Generate insights

4. Visualization
   - Generate charts
   - Create dashboard

5. Report Generation (Claude)
   - Write executive summary

6. Distribution (Email/Slack)

Tools: Llama 3.1, Claude, Custom tools
```

### Template 4: Customer Support Automation
```yaml
Name: Intelligent Support Ticket Handler
Trigger: New ticket (Email/Form)
Duration: 30s - 2 minutes
Cost: $0.05-$0.20

Steps:
1. Parse Ticket
   - Extract content
   - Parse user info

2. Categorization (Claude)
   - Classify issue type
   - Assess urgency

3. Conditional Routing:
   a. Simple → Auto-respond
   b. Complex → Route to agent
   c. Technical → Run diagnostics

4. KB Update (if new issue type)

Tools: Claude, Email/Ticketing APIs
```

### Template 5: Social Media Content Generator
```yaml
Name: Multi-Platform Social Creator
Trigger: Content brief input
Duration: 5-15 minutes
Cost: $1-$4

Steps:
1. Research (Parallel):
   a. Web search (trends)
   b. Image search (references)

2. Content Generation (Claude)
   - Long-form content
   - Extract key quotes
   - Generate hashtags

3. Platform Adaptation (Loop)
   For Twitter, LinkedIn, Instagram:
   - Adapt content
   - Optimize format

4. Visual Creation (FLUX.1)
   - Generate images
   - Create quote cards

5. Scheduling (Buffer/Hootsuite)

Tools: Claude, FLUX.1, Social APIs
```

## What You'll Get

### Workflow Design
```
📋 Workflow: Content Creation Pipeline

Trigger: Manual (user input)
   ↓
┌──────────────────────────────┐
│ 1. Generate Outline          │
│ Tool: Claude API             │
│ Duration: ~30s               │
│ Cost: $0.10                  │
└──────────────────────────────┘
   ↓
┌──────────────────────────────┐
│ 2. Write Sections (Loop)     │
│ Tool: Claude API             │
│ Duration: ~3min              │
│ Cost: $0.50                  │
└──────────────────────────────┘
   ↓
┌──────────────────────────────┐
│ 3. Generate Images           │
│ Tool: FLUX.1 Schnell         │
│ Duration: ~2min              │
│ Cost: Free                   │
└──────────────────────────────┘
   ↓
Complete Article

Total Duration: ~6min
Total Cost: $0.60
```

### Workflow Definition (JSON)
```json
{
  "workflow": {
    "id": "content-pipeline-001",
    "name": "Content Creation Pipeline",
    "version": "1.0.0",

    "triggers": [{
      "id": "trigger-1",
      "type": "manual",
      "config": {}
    }],

    "nodes": [
      {
        "id": "node-1",
        "name": "Generate Outline",
        "type": "ai-tool",
        "tool": "anthropic-claude",
        "config": {
          "model": "claude-3-5-sonnet",
          "temperature": 0.7
        },
        "inputs": {
          "prompt": "{{ trigger.payload.topic }}"
        }
      }
      // ... more nodes
    ],

    "edges": [
      {"from": "trigger-1", "to": "node-1"},
      {"from": "node-1", "to": "node-2"}
      // ... more edges
    ],

    "errorHandling": {
      "strategy": "retry",
      "maxAttempts": 3
    }
  }
}
```

### Implementation Guide
```
🔧 Implementation Guide: Content Creation Pipeline

Prerequisites:
□ Claude API key
□ FLUX.1 API access
□ Workflow runtime (n8n or custom)

Step 1: Set up Tool Integrations
──────────────────────────────────
1. Configure Claude API:
   - Sign up at https://anthropic.com
   - Get API key
   - Set environment variable: ANTHROPIC_API_KEY

2. Configure FLUX.1:
   - Self-host or use hosted API
   - Set endpoint: FLUX_API_ENDPOINT

Step 2: Deploy Workflow
──────────────────────────────────
Option A: Using n8n
1. Import workflow JSON
2. Configure credentials
3. Test workflow
4. Activate

Option B: Custom Runtime
1. Use workflow orchestrator library
2. Implement node execution logic
3. Add error handling
4. Deploy to server

Step 3: Test Workflow
──────────────────────────────────
Test Input:
{
  "topic": "AI in Healthcare 2025",
  "keywords": ["medical AI", "diagnostics"]
}

Expected Output:
- Article outline (30s)
- Full article (3min)
- Generated images (2min)
- Formatted content (instant)

Step 4: Monitor and Optimize
──────────────────────────────────
Metrics to track:
• Success rate (target: >95%)
• Average duration (target: <8min)
• Cost per execution (target: <$1)
• Error types and frequency

Troubleshooting:
• Issue: API timeout
  Fix: Increase timeout or retry count

• Issue: High costs
  Fix: Optimize prompts, reduce tokens
```

## Workflow Building Process

When you describe your workflow, the agent will:

1. **Gather Requirements**
   - What is the workflow's goal?
   - What triggers it?
   - What are the inputs/outputs?
   - Time constraints?
   - Budget per execution?
   - Compliance requirements?

2. **Select Tools**
   - Match capabilities to requirements
   - Consider cost, latency, reliability
   - Plan fallback alternatives

3. **Design Data Flow**
   - Map data transformations
   - Define intermediate storage
   - Plan error handling

4. **Generate Implementation**
   - Create workflow definition
   - Provide setup instructions
   - Include testing procedures

## Integration Patterns

### API Integration
- RESTful API calls with authentication
- Retry logic with exponential backoff
- Error handling and fallbacks
- Rate limiting and quota management

### Event-Driven
- Webhook triggers
- Message queue integration
- Real-time event processing
- Event filtering and routing

### Data Transformation
- Format conversion (JSON, XML, CSV)
- Field mapping and extraction
- Data validation and cleaning
- Aggregation and enrichment

## Monitoring and Analytics

Track workflow performance:
- **Execution count**: Total runs
- **Success rate**: % successful executions
- **Average duration**: Time per execution
- **Average cost**: $ per execution
- **Error rate**: % failed executions
- **Tool-specific metrics**: Per-tool performance

## Best Practices

1. **Start Simple**: Begin with linear workflows, add complexity gradually
2. **Plan for Failures**: Always include error handling and retries
3. **Monitor Costs**: Track API usage and optimize prompts
4. **Test Thoroughly**: Test with various inputs before production
5. **Document Well**: Maintain clear documentation of workflow logic
6. **Version Control**: Keep workflow definitions in version control
7. **Security**: Secure API keys, validate inputs, sanitize outputs

---

## Implementation

**Agent Used**: workflow-builder (Sonnet model)
**Tools**: Read, Write (workflow definitions), WebFetch (tool APIs)
**Patterns**: Linear, Fan-out/in, Conditional, Loop, Event-driven
**Templates**: 5+ pre-built workflow templates
**Integration**: n8n, Zapier, custom runtimes
