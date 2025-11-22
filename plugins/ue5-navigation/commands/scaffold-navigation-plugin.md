---
description: Scaffold a complete UE5 Navigation Plugin with all necessary files
---

# Scaffold UE5 Navigation Plugin

Create a complete Unreal Engine 5 Navigation Plugin with HTTP server integration. This command will:

1. Create the plugin directory structure in the user's project
2. Generate all necessary C++ source files (NavigationServer.h, NavigationServer.cpp)
3. Create the Build.cs configuration file
4. Generate the .uplugin descriptor file
5. Set up the module structure

## Directory Structure to Create

```
Plugins/NavigationPlugin/
├── Source/
│   ├── NavigationPlugin/
│   │   ├── Public/
│   │   │   └── NavigationServer.h
│   │   ├── Private/
│   │   │   └── NavigationServer.cpp
│   │   └── NavigationPlugin.Build.cs
├── Config/
│   └── FilterPlugin.ini
└── NavigationPlugin.uplugin
```

## Files to Generate

Use the templates from the ue5-navigation plugin's `templates/` directory:
- `Source/NavigationServer.h` → Copy to `Public/NavigationServer.h`
- `Source/NavigationServer.cpp` → Copy to `Private/NavigationServer.cpp`
- `Source/NavigationPlugin.Build.cs` → Copy to root of module
- `NavigationPlugin.uplugin` → Copy to plugin root

## Instructions

1. Ask the user for their UE5 project path
2. Verify the path exists and contains a .uproject file
3. Create the `Plugins/NavigationPlugin/` directory structure
4. Copy all template files to their appropriate locations
5. Update any placeholder values (API macros, module names) if needed
6. Generate a FilterPlugin.ini if requested
7. Provide instructions for:
   - Regenerating project files
   - Building the plugin
   - Enabling the plugin in the project
   - Starting the HTTP server

## Post-Setup Instructions

After scaffolding, inform the user:

```
✅ UE5 Navigation Plugin scaffolded successfully!

Next steps:
1. Right-click your .uproject file and select "Generate Visual Studio project files"
2. Open your project in Visual Studio
3. Build the solution (Ctrl+Shift+B)
4. Launch Unreal Editor
5. Enable the plugin: Edit → Plugins → Search "Navigation Plugin" → Enable
6. Restart the editor
7. Start the HTTP server from the Tools menu or via Blueprint

The Navigation Server will be available at http://localhost:8080/api/navigate
```
