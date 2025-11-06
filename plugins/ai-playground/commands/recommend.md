---
description: Get personalized AI tool recommendations based on your needs and preferences
argument-hint: "[optional: use case or preferences]"
allowed-tools:
  - Task:*
  - Read:**/*
  - Write:**/*
  - Grep:**/*
---

# AI Tool Recommendations Command

Get personalized AI tool recommendations using advanced recommendation algorithms inspired by Google's three-stage recommendation architecture.

## Usage

```bash
/recommend [optional: context or preferences]
```

## Examples

```bash
# General recommendations
/recommend

# Context-specific recommendations
/recommend for building a chatbot
/recommend for e-commerce automation
/recommend for content creation pipeline

# Preference-based recommendations
/recommend free and open-source only
/recommend with GDPR compliance required
/recommend self-hosted solutions
```

## How It Works

This command launches the **recommendation-engine** agent which uses a sophisticated three-stage process:

### Stage 1: Candidate Generation
- Analyzes your query and preferences
- Uses collaborative filtering to find similar user patterns
- Identifies tools frequently used together
- Generates 50-100 candidate tools

### Stage 2: Precise Scoring
Scores each candidate tool using weighted criteria:

- **Relevance (40%)**: Category match, capability alignment, use case fit
- **Quality (25%)**: Tool rating, community size, recency, vendor reputation
- **Accessibility (20%)**: Pricing match, license compatibility, integration ease
- **Performance (15%)**: Benchmarks, speed, reliability, scalability

### Stage 3: Re-ranking
Optimizes final recommendations for:
- **Diversity**: Multiple categories, vendor variety
- **Freshness**: Recently released (2024-2025) tools
- **Personalization**: Your specific requirements and preferences
- **Exploration**: 80% safe recommendations + 20% discovery

## Recommendation Modes

### Cold Start (First Time)
When you're new, we'll ask quick preference questions:
- What do you want to build? (use case)
- What's your budget? (pricing)
- Any compliance requirements? (GDPR, HIPAA, etc.)
- Self-hosted or cloud? (deployment)
- Experience level? (beginner, intermediate, expert)

### Personalized (Return User)
For existing users with history:
- Analyzes your past tool views and interactions
- Learns from your search patterns
- Adapts to your preferences over time
- Provides increasingly relevant recommendations

### Context-Aware (Specific Need)
When you have a specific current need:
- Prioritizes current context (70%) over history (30%)
- Provides focused recommendations for immediate need
- Includes "You might also like" based on profile

### Workflow-Based
For multi-tool workflow needs:
- Recommends tool combinations that work well together
- Shows integration patterns
- Provides end-to-end setup guidance

## What You'll Get

### Quick Recommendations (5 tools)
```
🎯 Recommended for You

1. **Codeium** ⭐ 4.7/5
   Unlimited AI code completion with 70+ languages
   Matches: Your interest in code-assistance and free tools

2. **Meta Llama 3.1 70B** ⭐ 4.7/5
   Open-source LLM balancing performance and efficiency
   Matches: Your preference for open-source and self-hosted

[...3 more recommendations]

💡 Based on your interest in code-assistance and open-source tools.
```

### Detailed Recommendations (3 tools)
```
🎯 Top Picks for Your Workflow

┌─ Codeium ─────────────────────────────┐
│ Why recommended:                      │
│ • Matches your code completion needs  │
│ • Free tier fits your budget          │
│ • Popular among similar users         │
│                                       │
│ Key Features:                         │
│ • Unlimited completions               │
│ • 70+ languages                       │
│ • Multi-file context                  │
│                                       │
│ Get Started: https://codeium.com/     │
└───────────────────────────────────────┘

Confidence: 87% match based on your profile
```

### Workflow Recommendations
```
🔧 Complete Workflow Setup

For your "content creation" project:

Phase 1: Text Generation
→ Claude API - Highest quality text generation

Phase 2: Image Creation
→ FLUX.1 Schnell - Commercial-free, fast generation

Phase 3: Automation
→ n8n - Open-source workflow automation

Integration Path:
Claude API → n8n → FLUX.1 API

Estimated Setup Time: 2 hours
Total Cost: Free tier available for all
```

## Personalization Features

### Learning from Your Behavior
The recommendation engine automatically tracks:
- Tools you view (duration indicates interest)
- Tools you compare (understanding trade-offs)
- Tools you save/bookmark (strong positive signal)
- Documentation clicks (high adoption intent)
- Return visits (sustained interest)

### Explicit Feedback
You can provide feedback:
- Thumbs up/down on recommendations
- "Not interested" signals
- "Show more like this" requests
- Adoption confirmations
- Reviews and ratings

### Preference Inference
The system learns your preferences:
- Frequent open-source views → prefer open-source
- Always checks self-hosting → deployment preference
- Compares pricing → budget-conscious
- Views enterprise tools → business use case
- Checks compliance badges → regulated industry

## Advanced Features

### Social Recommendations
- "Tools trending in your industry"
- "What similar companies are adopting"
- "Popular among users who viewed [X]"

### Serendipity Injection
- 1-2 "wildcard" recommendations
- Tools outside normal categories
- Emerging tools with high potential
- Cross-domain innovations

### Temporal Recommendations
- Different tools for exploration vs work
- Enterprise tools (weekday) vs hobby projects (weekend)
- Seasonal recommendations

## Performance Metrics

The recommendation engine is optimized for:

- **Engagement Rate**: >40% of recommendations clicked
- **Adoption Rate**: >15% of recommendations actually adopted
- **Diversity Score**: >3 categories in top 10 recommendations
- **Novelty Score**: 15-25% recommendations outside typical categories
- **User Satisfaction**: >4.0/5.0 average rating

## Privacy

Your preference data:
- Stored locally in your user profile
- Used only for improving your recommendations
- Never shared with third parties
- Can be cleared anytime

---

## Implementation

**Agent Used**: recommendation-engine (Sonnet model)
**Tools**: Read (database), Write (profiles), Grep (search)
**Algorithm**: Three-stage (Candidate Generation → Scoring → Re-ranking)
**Data Storage**: `/plugins/ai-playground/data/user-profiles/`
