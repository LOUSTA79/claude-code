---
description: Discover AI tools using semantic search and intelligent filtering
argument-hint: "[search query or category]"
allowed-tools:
  - Task:*
  - Read:**/*
  - Grep:**/*
---

# AI Tool Discovery Command

Discover the latest AI tools (2024-2025) using natural language search, semantic matching, and intelligent filtering.

## Usage

```bash
/discover [query]
```

## Examples

```bash
# Search by capability
/discover free code completion tools
/discover image generation with commercial license
/discover self-hosted LLM with GDPR compliance

# Search by use case
/discover tools for customer support automation
/discover best for content creation pipeline
/discover code testing and QA tools

# Search by category
/discover language-models
/discover browser-extensions
/discover workflow-automation

# Compare alternatives
/discover open-source alternatives to GPT-4
/discover zapier alternatives
```

## How It Works

This command launches the **tool-discovery** agent which:

1. **Understands Your Intent**
   - Analyzes your natural language query
   - Identifies key requirements (pricing, capabilities, compliance)
   - Maps to relevant tool categories

2. **Semantic Search**
   - Searches beyond keyword matching
   - Considers synonyms and related concepts
   - Matches use cases and capabilities

3. **Multi-dimensional Filtering**
   - Category filtering
   - Pricing models (free, freemium, paid, open-source)
   - Capabilities matching
   - Compliance requirements (SOC2, GDPR, HIPAA)
   - Integration options (APIs, self-hosting, IDEs)

4. **Intelligent Ranking**
   - Relevance to your query
   - Tool popularity and ratings
   - Community size and activity
   - Recency and maintenance status

5. **Rich Results**
   - Detailed tool information
   - Pricing and licensing details
   - Integration capabilities
   - Use cases and documentation links

## What You'll Get

### Quick List (Multiple Matches)
- Top 3-5 matching tools
- One-line descriptions
- Key differentiators
- Pricing information
- Ratings and popularity

### Detailed Analysis (Specific Tool)
- Comprehensive overview
- Full capability list
- Pricing breakdown
- Integration options
- Benchmarks and performance
- Security compliance
- Documentation links

### Comparison Matrix (Category Search)
- Side-by-side comparison
- Feature availability
- Pricing comparison
- Best use cases for each tool

## Categories Available

- **language-models**: LLMs like Llama 3.1, Gemini, Claude, Mistral
- **image-generation**: Image models like FLUX.1, Stable Diffusion
- **code-assistance**: Coding tools like Codeium, Windsurf, Qodo
- **browser-extensions**: Extensions like AI Blaze, Magical, HARPA AI
- **api-services**: API platforms like Google Gemini, Anthropic, Mistral
- **workflow-automation**: Automation tools like n8n, Zapier
- **testing-qa**: Testing tools for quality assurance

## Database Coverage

This command searches through **17+ AI tools** across **7 categories**, featuring:

- Latest 2024-2025 releases
- Open-source and proprietary tools
- Free and paid options
- Enterprise-grade platforms
- Emerging technologies

All tools include verified information about:
- Capabilities and features
- Pricing and licensing
- Benchmarks and performance
- Integration options
- Security compliance
- Documentation and support

---

## Implementation

**Agent Used**: tool-discovery (Sonnet model)
**Tools**: Read (database access), Grep (search), WebFetch (updates)
**Database**: `/plugins/ai-playground/data/ai-tools-database.json`
