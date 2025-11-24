# Quick Start Guide - UE5 Navigation Plugin

Get up and running with the UE5 Navigation Plugin in 5 minutes.

## Prerequisites

- ✅ Claude Code CLI installed
- ✅ Unreal Engine 5.1+ installed
- ✅ Visual Studio 2022 (or compatible C++ compiler)
- ✅ Existing UE5 project (or create a new one)

## Step 1: Install the Plugin

The plugin is already available in Claude Code if you're on the correct branch.

```bash
# Verify the plugin is available
ls plugins/ue5-navigation
```

## Step 2: Scaffold Your First Navigation Plugin

1. Open Claude Code in your UE5 project directory
2. Run the scaffold command:

```
/scaffold-navigation-plugin
```

3. Provide your UE5 project path when prompted:
```
C:/Projects/MyGame/MyGame.uproject
```

The command will create:
```
YourProject/
└── Plugins/
    └── NavigationPlugin/
        ├── Source/
        │   └── NavigationPlugin/
        │       ├── Public/
        │       │   └── NavigationServer.h
        │       ├── Private/
        │       │   ├── NavigationServer.cpp
        │       │   └── NavigationPluginModule.cpp
        │       └── NavigationPlugin.Build.cs
        ├── Config/
        │   └── FilterPlugin.ini
        └── NavigationPlugin.uplugin
```

## Step 3: Build the Plugin

### Option A: Visual Studio

1. Close Unreal Editor if it's open
2. Right-click your `.uproject` file
3. Select "Generate Visual Studio project files"
4. Open the generated `.sln` file
5. Build the solution (Ctrl+Shift+B)

### Option B: Command Line

```bash
# Windows
"C:/Program Files/Epic Games/UE_5.1/Engine/Build/BatchFiles/Build.bat" ^
    Development Win64 -Project="C:/Projects/MyGame/MyGame.uproject" ^
    -TargetType=Editor

# Mac
/Users/Shared/Epic\ Games/UE_5.1/Engine/Build/BatchFiles/Mac/Build.sh ^
    Development Mac -Project="/Users/YourName/MyGame/MyGame.uproject" ^
    -TargetType=Editor

# Linux
~/UnrealEngine/Engine/Build/BatchFiles/Linux/Build.sh ^
    Development Linux -Project="~/MyGame/MyGame.uproject" ^
    -TargetType=Editor
```

## Step 4: Enable the Plugin

1. Launch Unreal Editor
2. Go to **Edit → Plugins**
3. Search for "Navigation Plugin"
4. Check the **Enabled** checkbox
5. Click **Restart Now**

## Step 5: Start the HTTP Server

### Option A: Editor Menu

1. Go to **Tools → Start Navigation Server**
2. The server starts on `http://localhost:8080`
3. You'll see a notification: "Navigation Server started on port 8080"

### Option B: Blueprint

1. Open any Blueprint
2. Add a **Start HTTP Server** node
3. Connect to **Begin Play** or any event
4. Set Port to `8080`
5. Compile and run

### Option C: C++

```cpp
#include "NavigationPluginModule.h"

void StartNavigationServer()
{
    FNavigationPluginModule& Module = FModuleManager::LoadModuleChecked<FNavigationPluginModule>("NavigationPlugin");
    UNavigationServer* Server = Module.GetNavigationServer();
    if (Server)
    {
        Server->StartHTTPServer(8080);
    }
}
```

## Step 6: Test the API

### Quick Test with cURL

```bash
# Test 1: Focus on an asset
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{"command":"FocusAsset","assetName":"BP_ThirdPersonCharacter"}'

# Test 2: Search for assets
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{"command":"Search","assetName":"Character"}'

# Test 3: Navigate viewport
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{"command":"Navigate","location":{"x":0,"y":0,"z":500}}'
```

### Expected Response

```json
{
  "success": true,
  "message": "Focused on asset: BP_ThirdPersonCharacter",
  "error": "",
  "additionalData": {},
  "progress": 1.0
}
```

## Step 7: Create Your First Automation Script

### Python Example

Create `navigate_test.py`:

```python
import requests

BASE_URL = "http://localhost:8080/api/navigate"

def focus_asset(name):
    response = requests.post(BASE_URL, json={
        "command": "FocusAsset",
        "assetName": name
    })
    return response.json()

# Test it
result = focus_asset("BP_ThirdPersonCharacter")
print(f"Success: {result['success']}")
print(f"Message: {result['message']}")
```

Run it:
```bash
python navigate_test.py
```

## Next Steps

### 🎨 Explore Features

- **Asset Navigation**: Focus, open, and search assets
- **Viewport Control**: Control camera position and focus on actors
- **Blueprint Navigation**: Find and highlight Blueprint nodes
- **Session Management**: Save and load navigation sessions

### 📚 Learn More

- Read the [full README](README.md) for comprehensive documentation
- Check [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for advanced examples
- Use `/add-navigation-feature` to extend functionality

### 🔧 Customize

Add custom navigation features:
```
/add-navigation-feature
```

Example customizations:
- Custom asset type support (DataTables, Materials, etc.)
- Advanced camera movements
- Custom HTTP endpoints
- Integration with external tools

### 🧪 Generate Tests

Create comprehensive test suites:
```
/test-navigation-api
```

Choose format:
- cURL scripts
- Python test suite
- Postman collection
- JavaScript/Node.js

## Troubleshooting

### Server Won't Start

**Problem**: "Failed to start Navigation Server"

**Solutions**:
1. Check if port 8080 is already in use:
   ```bash
   # Windows
   netstat -ano | findstr :8080

   # Mac/Linux
   lsof -i :8080
   ```
2. Try a different port: `Server->StartHTTPServer(8081)`
3. Ensure HTTPServer plugin is enabled in UE5

### Asset Not Found

**Problem**: "Asset not found: AssetName"

**Solutions**:
1. Use full asset path: `/Game/Blueprints/BP_Character`
2. Verify asset exists in Content Browser
3. Ensure asset is loaded (not in background)

### Connection Refused

**Problem**: `curl: (7) Failed to connect to localhost port 8080`

**Solutions**:
1. Verify server is running (check notification)
2. Check UE5 Output Log for errors
3. Ensure firewall allows port 8080
4. Restart the navigation server

### Build Errors

**Problem**: Compilation errors when building

**Solutions**:
1. Verify UE5 version compatibility (5.1+)
2. Check all module dependencies in Build.cs
3. Regenerate project files
4. Clean and rebuild:
   ```bash
   # Delete Intermediate and Binaries folders
   # Regenerate project files
   # Build again
   ```

## Common Workflows

### Workflow 1: Asset Review

```python
# Review all player-related assets
import requests

nav = "http://localhost:8080/api/navigate"

# Search
result = requests.post(nav, json={"command": "Search", "assetName": "Player"})
assets = result.json()["additionalData"]

# Open each one
for key, path in assets.items():
    requests.post(nav, json={"command": "OpenAsset", "assetName": path})
    time.sleep(2)  # Wait for editor
```

### Workflow 2: Viewport Tour

```python
# Automated level tour
locations = [
    (0, 0, 500, "Spawn"),
    (1000, 0, 500, "Checkpoint 1"),
    (2000, 1000, 500, "Boss Arena")
]

for x, y, z, name in locations:
    print(f"Visiting: {name}")
    requests.post(nav, json={
        "command": "Navigate",
        "location": {"x": x, "y": y, "z": z}
    })
    time.sleep(3)
```

### Workflow 3: Blueprint Analysis

```python
# Open all blueprints and find specific nodes
blueprints = [
    "/Game/Blueprints/BP_Character",
    "/Game/Blueprints/BP_Enemy",
    "/Game/Blueprints/BP_Weapon"
]

for bp in blueprints:
    # Open blueprint
    requests.post(nav, json={"command": "OpenAsset", "assetName": bp})

    # Find BeginPlay node
    requests.post(nav, json={
        "command": "Blueprint",
        "assetName": bp,
        "editorType": "BeginPlay"
    })
```

## Success! 🎉

You now have a fully functional UE5 Navigation Plugin with HTTP API integration!

### What You Can Do Now:

- ✅ Control UE5 editor remotely via HTTP
- ✅ Automate asset navigation
- ✅ Create custom workflows
- ✅ Integrate with external tools
- ✅ Build automation scripts

### Get Help:

- Review the full documentation
- Ask Claude Code AI agents for assistance
- Check troubleshooting section
- Extend with custom features

**Happy navigating! 🚀**
