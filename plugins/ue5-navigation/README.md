# UE5 Navigation Plugin for Claude Code

A comprehensive Claude Code plugin for developing Unreal Engine 5 navigation systems with HTTP server integration, asset management, and AI-powered navigation features.

## Overview

This plugin provides tools and agents to help you build sophisticated navigation systems for Unreal Engine 5 projects. It includes:

- **Complete UE5 Plugin Templates**: Ready-to-use C++ code for navigation server implementation
- **HTTP API Integration**: RESTful API for external navigation control
- **Asset Navigation**: Navigate to and manage UE5 assets programmatically
- **Viewport Control**: Control editor viewports and cameras via API
- **Blueprint Integration**: Navigate blueprint graphs and nodes
- **Specialized Agents**: AI agents for architecture review, code review, and documentation

## Features

### 🚀 Quick Scaffolding
Instantly scaffold a complete UE5 Navigation Plugin with all necessary files:
- NavigationServer.h and .cpp with full implementation
- Build.cs configuration
- .uplugin descriptor
- Proper module structure

### 🌐 HTTP Server Integration
Built-in HTTP server for remote navigation control:
- RESTful API endpoints
- JSON request/response format
- Asset navigation commands
- Viewport control
- Blueprint navigation

### 🎯 Asset Management
Comprehensive asset navigation features:
- Focus on assets in Content Browser
- Open assets in appropriate editors
- Search and filter assets
- Navigate asset hierarchies
- Session management

### 📐 Blueprint Navigation
Navigate and control Blueprint graphs:
- Find and highlight nodes
- Navigate to function calls
- Track variable usage
- Blueprint call stack navigation

### 🤖 Specialized AI Agents

#### UE5 Architect
Expert agent for architecture and design decisions:
- Plugin structure review
- API design recommendations
- Performance optimization
- Integration guidance

#### Navigation Code Reviewer
Thorough code review focusing on:
- UE5 coding standards
- Memory management
- Thread safety
- Error handling
- Security

#### API Documentation Generator
Comprehensive documentation generation:
- C++ API reference
- HTTP API specifications
- Blueprint node documentation
- Integration guides

## Installation

### Prerequisites
- Claude Code CLI installed
- Unreal Engine 5.x installed
- Visual Studio 2022 (or compatible C++ compiler)
- Basic understanding of UE5 plugin development

### Install the Plugin

1. Clone or install this plugin to your Claude Code plugins directory:
```bash
cd ~/.claude/plugins  # or your Claude Code plugins directory
git clone <repository-url> ue5-navigation
```

2. Restart Claude Code or reload plugins

3. Verify installation:
```bash
claude --plugins
```

You should see `ue5-navigation` in the list.

## Usage

### Quick Start

1. **Scaffold a New UE5 Navigation Plugin**

In your UE5 project directory, run:
```bash
/scaffold-navigation-plugin
```

Claude will:
- Ask for your UE5 project path
- Create the plugin directory structure
- Copy all template files
- Provide setup instructions

2. **Build and Enable the Plugin**

Follow the post-setup instructions:
```bash
# Generate project files
Right-click YourProject.uproject → "Generate Visual Studio project files"

# Build in Visual Studio
Open solution → Build (Ctrl+Shift+B)

# Enable plugin in UE5
Edit → Plugins → Search "Navigation Plugin" → Enable → Restart
```

3. **Start the Navigation Server**

In the UE5 Editor:
- Open any Blueprint or C++ class
- Call `Start HTTP Server` on a NavigationServer instance
- Server starts on `http://localhost:8080`

4. **Test the API**

```bash
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{"command":"FocusAsset","assetName":"BP_PlayerCharacter"}'
```

### Available Commands

#### `/scaffold-navigation-plugin`
Generate a complete UE5 Navigation Plugin in your project.

**Example**:
```
User: /scaffold-navigation-plugin
Claude: I'll help you scaffold a UE5 Navigation Plugin. What's your UE5 project path?
User: C:/Projects/MyGame/MyGame.uproject
Claude: [Creates plugin structure and provides setup instructions]
```

#### `/add-navigation-feature`
Add a new navigation feature to an existing plugin.

**Example**:
```
User: /add-navigation-feature
Claude: What type of navigation feature would you like to add?
User: Custom DataTable navigation with preview
Claude: [Implements custom feature with code examples]
```

#### `/test-navigation-api`
Generate test scripts and examples for the Navigation API.

**Example**:
```
User: /test-navigation-api
Claude: What test format would you prefer? (cURL/Python/Postman/JavaScript)
User: Python
Claude: [Generates comprehensive Python test suite]
```

### Using Specialized Agents

Agents are specialized AI assistants for specific tasks.

#### Architecture Review

Ask the UE5 Architect agent to review your design:
```
User: @ue5-architect please review my navigation plugin architecture
```

The agent will:
- Analyze your plugin structure
- Identify design issues
- Recommend improvements
- Provide code examples

#### Code Review

Request a thorough code review:
```
User: @navigation-code-reviewer please review NavigationServer.cpp
```

The agent will:
- Check UE5 coding standards
- Identify memory issues
- Check thread safety
- Suggest optimizations

#### Generate Documentation

Generate comprehensive API documentation:
```
User: @api-documentation-generator create HTTP API documentation
```

The agent will:
- Generate complete API reference
- Include examples in multiple languages
- Create integration guides
- Add troubleshooting tips

## API Reference

### HTTP Endpoints

#### POST /api/navigate

Main navigation endpoint for all commands.

**Focus Asset Example**:
```json
{
  "command": "FocusAsset",
  "assetName": "BP_PlayerCharacter"
}
```

**Navigate to Location Example**:
```json
{
  "command": "Navigate",
  "location": {
    "x": 0,
    "y": 0,
    "z": 100
  }
}
```

**Response Format**:
```json
{
  "success": true,
  "message": "Focused on asset: BP_PlayerCharacter",
  "error": "",
  "additionalData": {},
  "progress": 1.0
}
```

### C++ API

#### UNavigationServer

Main navigation server class.

**Key Methods**:
- `StartHTTPServer(int32 Port)` - Start the HTTP server
- `StopHTTPServer()` - Stop the HTTP server
- `FocusAsset(const FString& AssetName)` - Focus on an asset
- `OpenAsset(const FString& AssetPath)` - Open an asset
- `NavigateToLocation(const FVector& Location)` - Navigate viewport
- `FocusOnActor(const FString& ActorName)` - Focus on actor

**Example Usage**:
```cpp
UNavigationServer* Server = NewObject<UNavigationServer>();
Server->StartHTTPServer(8080);

FNavigationResponse Response = Server->FocusAsset(TEXT("BP_PlayerCharacter"));
if (Response.Success)
{
    UE_LOG(LogTemp, Log, TEXT("%s"), *Response.Message);
}
```

## Templates Included

The plugin includes complete, production-ready templates:

### NavigationServer.h
- Complete header with all navigation functions
- Proper UE5 macros and reflection
- Blueprint-compatible functions
- Comprehensive API surface

### NavigationServer.cpp
- Full implementation of all navigation features
- HTTP server setup and routing
- Asset registry integration
- Content browser integration
- Viewport control
- Blueprint navigation
- Session management
- Breadcrumb system

### NavigationPlugin.Build.cs
- Complete module dependencies
- Proper include paths
- All required UE5 modules

### NavigationPlugin.uplugin
- Plugin descriptor
- Module configuration
- HTTPServer plugin dependency

## Architecture

```
UE5 Navigation Plugin
├── HTTP Server (Port 8080)
│   ├── Route: /api/navigate
│   └── JSON Request/Response
├── Command Processing
│   ├── Asset Navigation
│   ├── Viewport Control
│   ├── Blueprint Navigation
│   └── Code Navigation
├── UE5 Integration
│   ├── Asset Registry
│   ├── Content Browser
│   ├── Level Editor
│   └── Blueprint Editor
└── Session Management
    ├── Breadcrumb System
    └── Navigation History
```

## Best Practices

1. **Error Handling**: Always check response success status
2. **Asset Paths**: Use full asset paths (e.g., `/Game/Blueprints/BP_Player`)
3. **Thread Safety**: HTTP server runs on separate thread, use proper synchronization
4. **Performance**: Cache asset lookups when possible
5. **Security**: Validate all incoming requests
6. **Logging**: Enable verbose logging for debugging

## Troubleshooting

### HTTP Server Won't Start
- Check if port 8080 is already in use
- Ensure HTTPServer plugin is enabled
- Check UE5 logs for error messages

### Asset Not Found
- Verify asset exists in Content Browser
- Use full asset path, not just name
- Check asset is loaded (not in background)

### Viewport Not Responding
- Ensure Level Editor viewport is active
- Check viewport is not in Play mode
- Verify viewport client is valid

### Performance Issues
- Reduce search scope when possible
- Use asset registry filters
- Cache frequently accessed assets
- Consider async operations for heavy tasks

## Examples

### Python Integration

```python
import requests

class UE5Navigator:
    def __init__(self, base_url="http://localhost:8080"):
        self.url = f"{base_url}/api/navigate"

    def focus_asset(self, asset_name):
        return requests.post(self.url, json={
            "command": "FocusAsset",
            "assetName": asset_name
        }).json()

    def navigate_to(self, x, y, z):
        return requests.post(self.url, json={
            "command": "Navigate",
            "location": {"x": x, "y": y, "z": z}
        }).json()

# Usage
nav = UE5Navigator()
nav.focus_asset("BP_PlayerCharacter")
nav.navigate_to(0, 0, 100)
```

### JavaScript/Node.js Integration

```javascript
const axios = require('axios');

class UE5Navigator {
    constructor(baseUrl = 'http://localhost:8080') {
        this.url = `${baseUrl}/api/navigate`;
    }

    async focusAsset(assetName) {
        const response = await axios.post(this.url, {
            command: 'FocusAsset',
            assetName: assetName
        });
        return response.data;
    }

    async navigateTo(x, y, z) {
        const response = await axios.post(this.url, {
            command: 'Navigate',
            location: { x, y, z }
        });
        return response.data;
    }
}

// Usage
const nav = new UE5Navigator();
await nav.focusAsset('BP_PlayerCharacter');
await nav.navigateTo(0, 0, 100);
```

## Contributing

Contributions are welcome! Please:

1. Follow UE5 coding standards
2. Add tests for new features
3. Update documentation
4. Submit pull requests

## License

MIT License - See LICENSE file for details

## Support

- GitHub Issues: [Report bugs or request features]
- Documentation: [Link to full documentation]
- UE5 Forums: [Community support]

## Changelog

### Version 1.0.0
- Initial release
- Complete navigation server implementation
- HTTP API integration
- Asset navigation features
- Viewport control
- Blueprint navigation
- Session management
- Specialized AI agents

## Acknowledgments

Built with Claude Code and powered by Anthropic's Claude AI.

Special thanks to the Unreal Engine community for inspiration and support.
