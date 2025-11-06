---
description: Compare AI tools side-by-side with benchmarks and scoring
argument-hint: "<tool1> [tool2] [tool3] ..."
allowed-tools:
  - Task:*
  - Read:**/*
  - Grep:**/*
  - WebFetch:*
---

# AI Tool Comparison Command

Compare AI tools side-by-side with structured analysis, quantitative benchmarks, and weighted scoring to make informed decisions.

## Usage

```bash
/compare <tool1> [tool2] [tool3] ...
```

## Examples

```bash
# Compare specific tools
/compare llama-3.1-405b gemini-api anthropic-claude
/compare codeium windsurf
/compare flux1-schnell flux1-dev
/compare n8n zapier

# Compare by category
/compare language-models
/compare code-assistance tools
/compare image generation models
/compare workflow automation platforms

# Alternative comparisons
/compare open-source alternatives to GPT-4
/compare free code completion tools
/compare self-hosted LLMs
```

## How It Works

This command launches the **tool-comparison** agent which:

1. **Loads Tool Data**
   - Retrieves comprehensive information for each tool
   - Gathers benchmarks and performance metrics
   - Collects pricing and licensing details
   - Checks compliance certifications

2. **Applies Category-Specific Criteria**
   - Language Models: Parameters, context length, benchmarks, cost
   - Image Generation: Quality, speed, licensing
   - Code Assistance: Language support, accuracy, integration
   - API Services: Capabilities, pricing, reliability

3. **Calculates Weighted Scores**
   - Multi-criteria decision analysis
   - Category-appropriate weighting
   - Use case-specific scoring
   - Total Cost of Ownership (TCO) calculations

4. **Presents Structured Comparison**
   - Side-by-side feature matrix
   - Performance benchmarks
   - Cost analysis
   - Clear recommendations for different use cases

## Comparison Criteria by Category

### Language Models (LLMs)
**Weighted Scoring**:
- Model Characteristics (30%): Parameters, context window, languages
- Performance (25%): Benchmarks, latency, throughput, accuracy
- Cost & Accessibility (25%): Pricing, free tier, self-hosting, license
- Integration (20%): API, SDKs, cloud providers, fine-tuning

**Benchmarks**:
- MMLU (general knowledge)
- HumanEval (code generation)
- MATH (mathematical reasoning)
- TruthfulQA (factual accuracy)

### Image Generation
**Weighted Scoring**:
- Quality (35%): Resolution, style, text rendering, realism
- Speed (25%): Generation time, batch processing, API latency
- Licensing (25%): Commercial use, attribution, modifications
- Integration (15%): API, UI compatibility, custom models

**Benchmarks**:
- FID Score (image quality)
- CLIP Score (text-image alignment)
- Generation speed (seconds per image)

### Code Assistance
**Weighted Scoring**:
- Code Intelligence (35%): Language support, context awareness, refactoring
- User Experience (25%): IDE integration, latency, accuracy
- Cost (20%): Pricing model, usage limits, free tier
- Privacy & Security (20%): Data retention, confidentiality, compliance

**Benchmarks**:
- Acceptance rate (% of suggestions accepted)
- Edit distance (accuracy of suggestions)
- Multi-line accuracy

### API Services
**Weighted Scoring**:
- Capabilities (30%): Model variety, features, advanced capabilities
- Pricing (30%): Cost per unit, free tier, volume discounts
- Reliability (25%): Uptime SLA, rate limits, error handling
- Integration (15%): SDK quality, documentation, webhooks

## Output Formats

### Quick Comparison Table
```
📊 Language Models Comparison

| Feature              | Llama 3.1 405B  | Gemini API      | Claude 3.5      |
|---------------------|-----------------|-----------------|-----------------|
| **Pricing**         |                 |                 |                 |
| Model               | Open-source     | Freemium        | Paid            |
| Free Tier           | ✓ Self-hosted   | ✓ 1M tokens/day | ✗               |
| Cost                | Free (hosting)  | $0.075/1M       | $3.00/1M        |
|                     |                 |                 |                 |
| **Performance**     |                 |                 |                 |
| Context Length      | 128K tokens     | 2M tokens       | 200K tokens     |
| Parameters          | 405B            | Unknown         | Unknown         |
| MMLU Score          | ~85%            | ~90%            | ~89%            |
|                     |                 |                 |                 |
| **Integration**     |                 |                 |                 |
| API Available       | ✓               | ✓               | ✓               |
| Self-Hostable       | ✓               | ✗               | ✗               |
| SDKs                | Multiple        | Official        | Official        |
|                     |                 |                 |                 |
| **Compliance**      |                 |                 |                 |
| SOC2                | N/A             | ✓               | ✓               |
| GDPR                | ✓               | ✓               | ✓               |
| HIPAA               | ✗               | ✓               | ✓               |
|                     |                 |                 |                 |
| **Overall Rating**  | ⭐ 4.8/5        | ⭐ 4.7/5        | ⭐ 4.9/5        |
| **Popularity**      | 95%             | 89%             | 92%             |

**Recommendation**:
• Best for self-hosted/open-source: Llama 3.1 405B
• Best for free tier/generous limits: Gemini API
• Best for quality/safety: Claude 3.5
```

### Detailed Comparison Report
```
🔍 Detailed Comparison: Codeium vs Windsurf

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. PRICING ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Codeium: Freemium
• Individual: Free (unlimited)
• Teams: $12/user/month
• Enterprise: Custom
• TCO (5 developers): $60/month (Teams tier)

Windsurf: Freemium
• Free tier: Available
• Paid tiers: TBD
• TCO (5 developers): Estimated $50-100/month

💰 Winner: Codeium - Better free tier value

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. FEATURE COMPARISON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature Category          | Codeium | Windsurf
─────────────────────────────────────────────
Code Completion           |    ✓    |    ✓
Multi-file Understanding  |    ○    |    ✓
Agentic Coding           |    ✗    |    ✓
70+ Languages            |    ✓    |    ○
IDE Integration          |    ✓    |    ○
Refactoring              |    ✓    |    ✓

Legend: ✓ Full | ○ Partial | ✗ Not available

🎯 Winner: Windsurf - More advanced AI features

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. WEIGHTED OVERALL SCORE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Criteria (Weight)         | Codeium | Windsurf
──────────────────────────────────────────
Code Intelligence (35%)   |   8.5   |   9.2
User Experience (25%)     |   9.0   |   8.5
Cost (20%)               |   10.0  |   8.0
Privacy & Security (20%)  |   8.5   |   8.5
──────────────────────────────────────────
TOTAL SCORE              |   8.9   |   8.7

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. FINAL RECOMMENDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🥇 Best Overall: Codeium (by small margin)
Codeium edges out slightly due to its generous free tier
and broader IDE support, despite Windsurf's more advanced
AI-native features.

🎯 Best for Specific Use Cases:
• Individual developers: Codeium - Unlimited free tier
• Complex codebases: Windsurf - Superior multi-file understanding
• Budget-conscious teams: Codeium - Lower cost per developer
• Cutting-edge AI: Windsurf - Agentic coding capabilities

⚠️  Important Considerations:
• Windsurf is newer and evolving rapidly
• Codeium has larger proven user base
```

### Visual Score Comparison
```
📈 Comparative Scoring Analysis

Codeium vs Windsurf

Code Intelligence:
Codeium:  ████████████████░░░░ 85%
Windsurf: ████████████████████ 92%

User Experience:
Codeium:  ████████████████████ 90%
Windsurf: ████████████████░░░░ 85%

Cost Efficiency:
Codeium:  ████████████████████ 100%
Windsurf: ████████████████░░░░ 80%

Privacy & Security:
Codeium:  ████████████████░░░░ 85%
Windsurf: ████████████████░░░░ 85%

Overall Score (Weighted):
Codeium:  ████████████████████ 89%  ⭐⭐⭐⭐
Windsurf: ████████████████████ 87%  ⭐⭐⭐⭐

💡 Insight: Very close competition - choose based on
whether you value cost (Codeium) or advanced AI (Windsurf)
```

## Comparison Strategies

### Head-to-Head (2 tools)
Direct alternative comparison with clear winner for each criterion and overall recommendation based on use case.

### Category Leaders (3-5 tools)
Market leaders plus challengers with weighted scoring system, clear category winner, and best alternatives for specific needs.

### Budget-Conscious
Focus on pricing and TCO, include all free/open-source options, calculate break-even points.

### Enterprise Evaluation
Weight compliance and security highly, include support and SLA analysis, consider integration costs and vendor stability.

### Technical Deep Dive
Focus on technical capabilities, include architecture analysis, test edge cases and limits, provide integration examples.

## Data Quality

### Verification
- Cross-reference multiple sources
- Note data freshness (lastVerified field)
- Highlight when data may be outdated
- Provide source attribution

### Objectivity
- Use quantitative data where available
- Present trade-offs, not just strengths
- Include pricing for all tiers
- Disclose limitations or gaps in data
- Avoid vendor bias

## Common Comparisons

### Most Popular
- Llama 3.1 vs GPT-4 vs Claude
- Codeium vs GitHub Copilot vs Windsurf
- FLUX.1 vs Stable Diffusion vs Midjourney
- n8n vs Zapier vs Make
- Google Gemini vs Anthropic Claude vs OpenAI

### Category Leaders
- Best LLM for self-hosting
- Best free code completion
- Best commercial image generation
- Best workflow automation
- Best API services

---

## Implementation

**Agent Used**: tool-comparison (Sonnet model)
**Tools**: Read (database), Grep (search), WebFetch (live data)
**Methodology**: Category-specific weighted scoring with multi-criteria analysis
**Database**: `/plugins/ai-playground/data/ai-tools-database.json`
