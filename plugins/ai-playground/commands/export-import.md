---
description: Export and import tool collections, workflows, and preferences
argument-hint: "[export|import] [format] [filename]"
allowed-tools:
  - Read:**/*
  - Write:**/*
  - Bash:*
---

# Export/Import Tool Collections

Export and import your AI tool collections, workflows, preferences, and analytics data in multiple formats for backup, sharing, and portability.

## Usage

```bash
# Export commands
/export-import export json my-tools.json
/export-import export csv my-tools.csv
/export-import export yaml my-tools.yaml

# Import commands
/export-import import json my-tools.json
/export-import import csv my-tools.csv

# Export specific data
/export-import export saved-tools json
/export-import export workflows json
/export-import export preferences json
/export-import export analytics json
```

## Supported Formats

### JSON (Recommended)
- **Full fidelity**: All data structures preserved
- **Human-readable**: Easy to inspect and edit
- **Universal**: Compatible with most tools
- **Nested structures**: Supports complex data

### CSV
- **Spreadsheet compatible**: Opens in Excel, Google Sheets
- **Simple structure**: Flat data representation
- **Bulk editing**: Easy to modify in spreadsheet tools
- **Limited nesting**: Complex structures flattened

### YAML
- **Configuration files**: Good for version control
- **Human-friendly**: More readable than JSON
- **Comments supported**: Document your data
- **Hierarchical**: Clean nested structures

### XML
- **Enterprise systems**: Compatible with legacy systems
- **Schema validation**: Structured with XSD
- **Industry standard**: GDPR data portability format
- **Verbose**: Larger file sizes

## What Can Be Exported

### 1. Saved Tools Collection
```json
{
  "export": {
    "type": "saved-tools",
    "version": "1.0.0",
    "exported": "2025-11-06T10:30:00Z",
    "tools": [
      {
        "toolId": "codeium",
        "name": "Codeium",
        "category": "code-assistance",
        "savedAt": "2025-10-15T14:20:00Z",
        "notes": "Using this for all code completion",
        "tags": ["primary", "coding"],
        "rating": 5
      }
    ],
    "metadata": {
      "toolCount": 12,
      "categories": ["code-assistance", "language-models"],
      "owner": "user-123"
    }
  }
}
```

### 2. Workflows
```json
{
  "export": {
    "type": "workflows",
    "version": "1.0.0",
    "workflows": [
      {
        "id": "workflow-001",
        "name": "Content Creation Pipeline",
        "description": "Generate blog posts with AI",
        "nodes": [...],
        "edges": [...],
        "created": "2025-10-20T09:00:00Z",
        "modified": "2025-11-01T15:30:00Z"
      }
    ]
  }
}
```

### 3. User Preferences
```json
{
  "export": {
    "type": "preferences",
    "version": "1.0.0",
    "preferences": {
      "categories": ["code-assistance", "language-models"],
      "pricingPreference": ["free", "open-source"],
      "complianceRequired": ["GDPR", "SOC2"],
      "technicalLevel": "intermediate",
      "notifications": {
        "newTools": true,
        "priceChanges": true,
        "securityUpdates": true
      },
      "display": {
        "theme": "dark",
        "compactMode": false,
        "itemsPerPage": 25
      }
    }
  }
}
```

### 4. Analytics Data
```json
{
  "export": {
    "type": "analytics",
    "version": "1.0.0",
    "period": {
      "start": "2025-10-01",
      "end": "2025-10-31"
    },
    "summary": {
      "toolsViewed": 47,
      "toolsAdopted": 8,
      "searchesPerformed": 23,
      "comparisons": 12,
      "workflowsCreated": 3
    },
    "roiData": {
      "totalTimeSaved": 85.5,
      "totalCostSavings": 6412.50,
      "averageROI": 547
    }
  }
}
```

### 5. Complete Backup
```json
{
  "export": {
    "type": "complete-backup",
    "version": "1.0.0",
    "exported": "2025-11-06T10:30:00Z",
    "data": {
      "savedTools": [...],
      "workflows": [...],
      "preferences": {...},
      "analytics": {...},
      "searchHistory": [...],
      "comparisonHistory": [...]
    },
    "metadata": {
      "userId": "user-123",
      "platform": "claude-code",
      "totalItems": 156
    }
  }
}
```

## Export Examples

### Export Saved Tools (JSON)
```bash
/export-import export saved-tools json
```

Output: `ai-playground-saved-tools-2025-11-06.json`
```json
{
  "export": {
    "type": "saved-tools",
    "tools": [
      {
        "toolId": "codeium",
        "name": "Codeium",
        "category": "code-assistance",
        "vendor": "Codeium",
        "savedAt": "2025-10-15",
        "myRating": 5,
        "myNotes": "Excellent free tier, using daily",
        "myTags": ["coding", "primary", "free"]
      },
      {
        "toolId": "llama-3.1-70b",
        "name": "Meta Llama 3.1 70B",
        "category": "language-models",
        "vendor": "Meta",
        "savedAt": "2025-10-18",
        "myRating": 4.5,
        "myNotes": "Great for self-hosted deployment",
        "myTags": ["llm", "self-hosted", "open-source"]
      }
    ]
  }
}
```

### Export Saved Tools (CSV)
```bash
/export-import export saved-tools csv
```

Output: `ai-playground-saved-tools-2025-11-06.csv`
```csv
toolId,name,category,vendor,savedAt,myRating,myNotes,myTags
codeium,Codeium,code-assistance,Codeium,2025-10-15,5,"Excellent free tier, using daily","coding|primary|free"
llama-3.1-70b,Meta Llama 3.1 70B,language-models,Meta,2025-10-18,4.5,"Great for self-hosted deployment","llm|self-hosted|open-source"
flux1-schnell,FLUX.1 Schnell,image-generation,Black Forest Labs,2025-10-22,4.8,"Best open-source image model","image|commercial|fast"
```

### Export Workflows (YAML)
```bash
/export-import export workflows yaml
```

Output: `ai-playground-workflows-2025-11-06.yaml`
```yaml
export:
  type: workflows
  version: 1.0.0
  workflows:
    - id: workflow-001
      name: Content Creation Pipeline
      description: Generate blog posts with text and images
      created: 2025-10-20T09:00:00Z
      nodes:
        - id: node-1
          name: Generate Outline
          type: ai-tool
          tool: anthropic-claude
          config:
            model: claude-3-5-sonnet
            temperature: 0.7
        - id: node-2
          name: Generate Images
          type: ai-tool
          tool: flux1-schnell
      edges:
        - from: node-1
          to: node-2
```

## Import Examples

### Import from JSON
```bash
/export-import import json my-backup.json
```

Process:
1. Validates JSON structure
2. Checks version compatibility
3. Identifies data type (saved-tools, workflows, etc.)
4. Merges or replaces existing data (user choice)
5. Reports import results

Output:
```
✅ Import Successful

Imported: my-backup.json
Type: saved-tools
Items: 12 tools

Summary:
• New tools added: 8
• Existing tools updated: 4
• Duplicates skipped: 0
• Errors: 0

Imported Tools:
1. Codeium (code-assistance)
2. Llama 3.1 70B (language-models)
3. FLUX.1 Schnell (image-generation)
[...9 more]

Next Steps:
• View imported tools: /discover saved-tools
• Compare tools: /compare codeium windsurf
```

### Import from CSV
```bash
/export-import import csv external-tools.csv
```

Process:
1. Parses CSV format
2. Maps columns to data structure
3. Validates tool IDs (checks against database)
4. Imports valid rows
5. Reports errors for invalid rows

## Data Portability Features

### GDPR Compliance
Export all personal data in machine-readable format:
```bash
/export-import export complete-backup json
```

Includes:
- All saved tools and collections
- All workflows created
- All preferences and settings
- Usage analytics (anonymized)
- Search history
- Comparison history

### Migration Between Systems
Export from one system, import to another:
```bash
# System A (export)
/export-import export complete-backup json backup.json

# System B (import)
/export-import import json backup.json
```

### Version Control Integration
Export workflows to YAML for git tracking:
```bash
/export-import export workflows yaml workflows.yaml
git add workflows.yaml
git commit -m "Update workflows"
```

### Team Sharing
Export curated tool collections for team members:
```bash
/export-import export saved-tools json team-recommended-tools.json
# Share file with team
# Team members import:
/export-import import json team-recommended-tools.json
```

## Advanced Features

### Selective Export
```bash
# Export only specific categories
/export-import export saved-tools json --category=code-assistance

# Export tools with specific tags
/export-import export saved-tools json --tags=production,critical

# Export date range
/export-import export analytics json --from=2025-10-01 --to=2025-10-31
```

### Merge Strategies
When importing, choose merge strategy:

1. **Add Only**: Only add new items, skip existing
2. **Update Only**: Only update existing items
3. **Replace**: Replace all data
4. **Smart Merge**: Update existing, add new

```bash
/export-import import json backup.json --strategy=smart-merge
```

### Format Conversion
Convert between formats:
```bash
# Export as JSON, import as CSV
/export-import export saved-tools json
/export-import convert my-tools.json csv
# Result: my-tools.csv
```

### Validation
Validate export files without importing:
```bash
/export-import validate my-backup.json
```

Output:
```
✅ Validation Successful

File: my-backup.json
Format: JSON
Type: complete-backup
Version: 1.0.0

Structure:
• Saved tools: 12 items ✓
• Workflows: 3 items ✓
• Preferences: Valid ✓
• Analytics: Valid ✓

Compatibility:
• Current version: ✓ Compatible
• Tool IDs: ✓ All valid
• Schema: ✓ Valid

Ready to import: Yes
```

## Security & Privacy

### Data Sanitization
Before export:
- API keys removed
- Passwords removed
- Personal identifiers anonymized (optional)
- Sensitive notes redacted (optional)

### Encryption
Encrypt sensitive exports:
```bash
/export-import export complete-backup json --encrypt
# Prompts for password
# Creates: backup.json.encrypted
```

Decrypt on import:
```bash
/export-import import json backup.json.encrypted --decrypt
# Prompts for password
```

### Audit Trail
All export/import operations logged:
- Timestamp
- User
- Operation type
- File name
- Items count
- Success/failure

## Best Practices

### Regular Backups
Schedule regular exports:
```bash
# Weekly backup
/export-import export complete-backup json weekly-backup-$(date +%Y-%m-%d).json
```

### Version Control
Keep workflow definitions in git:
```bash
/export-import export workflows yaml
git add *.yaml
git commit -m "Update workflows"
```

### Team Synchronization
Share curated collections:
1. Export recommended tools
2. Share file via git/cloud
3. Team imports and reviews
4. Continuous updates

### Migration Checklist
When migrating systems:
1. ✓ Export complete backup
2. ✓ Validate export file
3. ✓ Test import on new system
4. ✓ Verify all data imported
5. ✓ Check functionality
6. ✓ Keep backup until confirmed

---

## Implementation

**Tools Used**: Read (source data), Write (export files), Bash (file operations)
**Formats**: JSON, CSV, YAML, XML
**Features**: GDPR compliance, encryption, validation, merge strategies
**Location**: Exports saved to `./exports/` directory
