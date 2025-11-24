# Troubleshooting Guide - UE5 Navigation Plugin

Common issues and their solutions when using the UE5 Navigation Plugin.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Build Errors](#build-errors)
3. [Server Issues](#server-issues)
4. [Navigation Errors](#navigation-errors)
5. [Performance Issues](#performance-issues)
6. [API Issues](#api-issues)

---

## Installation Issues

### Plugin Not Found After Scaffolding

**Symptoms**:
- Plugin doesn't appear in Plugins menu
- "Plugin not found" error

**Solutions**:

1. **Verify Plugin Location**:
   ```bash
   # Plugin should be at:
   YourProject/Plugins/NavigationPlugin/NavigationPlugin.uplugin
   ```

2. **Check .uplugin File**:
   - Ensure `NavigationPlugin.uplugin` exists
   - Verify JSON is valid (no syntax errors)
   - Check file permissions (read access)

3. **Regenerate Project Files**:
   ```bash
   # Windows: Right-click .uproject → "Generate Visual Studio project files"
   # Or delete .sln and regenerate
   ```

4. **Verify Plugin Structure**:
   ```
   Plugins/NavigationPlugin/
   ├── NavigationPlugin.uplugin ✓
   ├── Source/
   │   └── NavigationPlugin/
   │       ├── NavigationPlugin.Build.cs ✓
   │       ├── Public/
   │       │   └── NavigationServer.h ✓
   │       └── Private/
   │           └── NavigationServer.cpp ✓
   ```

### Plugin Won't Enable

**Symptoms**:
- Checkbox won't stay checked
- "Plugin failed to load" error

**Solutions**:

1. **Check UE5 Version**:
   - Plugin requires UE5.1 or later
   - Check `EngineVersion` in .uplugin

2. **Build the Plugin**:
   - Plugin must be compiled before enabling
   - Build solution in Visual Studio
   - Check Output Log for compile errors

3. **Check Dependencies**:
   - Ensure HTTPServer plugin is available
   - Verify all modules in Build.cs exist

4. **Review Output Log**:
   ```
   Window → Developer Tools → Output Log
   Filter: "NavigationPlugin"
   ```

---

## Build Errors

### "Cannot open include file: 'NavigationServer.h'"

**Cause**: Include path issue

**Solutions**:

1. **Verify File Location**:
   ```
   Source/NavigationPlugin/Public/NavigationServer.h
   ```

2. **Check Build.cs**:
   ```csharp
   PublicIncludePaths.AddRange(new string[] {
       // Should not need explicit paths if structure is correct
   });
   ```

3. **Use Angle Brackets**:
   ```cpp
   // Use this:
   #include "NavigationServer.h"

   // Not this:
   #include <NavigationServer.h>
   ```

### "Unresolved external symbol" Errors

**Cause**: Linking issue or missing module dependency

**Solutions**:

1. **Add Missing Modules to Build.cs**:
   ```csharp
   PublicDependencyModuleNames.AddRange(new string[]
   {
       "Core",
       "CoreUObject",
       "Engine",
       "HTTP",
       "HTTPServer",  // ← Ensure this is present
       "Json",
       "JsonUtilities",
   });
   ```

2. **Check API Export Macro**:
   ```cpp
   // In header file:
   class NAVIGATIONPLUGIN_API UNavigationServer : public UObject
   //     ^^^^^^^^^^^^^^^^^^^^^^ Must match module name
   ```

3. **Clean and Rebuild**:
   ```bash
   # Delete these folders:
   Plugins/NavigationPlugin/Intermediate/
   Plugins/NavigationPlugin/Binaries/

   # Regenerate and rebuild
   ```

### HTTPServer Module Not Found

**Cause**: HTTPServer plugin not enabled

**Solutions**:

1. **Enable HTTPServer Plugin**:
   ```
   Edit → Plugins → Search "HTTP" → Enable "HTTP Server"
   ```

2. **Verify in .uplugin**:
   ```json
   "Plugins": [
       {
           "Name": "HTTPServer",
           "Enabled": true
       }
   ]
   ```

3. **Check Engine Version**:
   - HTTPServer available in UE5.0+
   - Use alternative HTTP library if needed

---

## Server Issues

### HTTP Server Won't Start

**Symptoms**:
- "Failed to start Navigation Server" notification
- No response on port 8080

**Solutions**:

1. **Check Port Availability**:
   ```bash
   # Windows
   netstat -ano | findstr :8080

   # Mac/Linux
   lsof -i :8080

   # If in use, kill process or use different port
   ```

2. **Try Different Port**:
   ```cpp
   Server->StartHTTPServer(8081);  // Try 8081, 8082, etc.
   ```

3. **Check Firewall**:
   ```bash
   # Windows: Allow port in Windows Firewall
   # Add inbound rule for port 8080

   # Mac: System Preferences → Security → Firewall
   # Allow UnrealEditor

   # Linux: Configure iptables/ufw
   sudo ufw allow 8080
   ```

4. **Verify HTTPServer Module**:
   ```cpp
   // Check if module loads correctly
   if (FModuleManager::Get().IsModuleLoaded("HTTPServer"))
   {
       UE_LOG(LogTemp, Log, TEXT("HTTPServer module loaded"));
   }
   else
   {
       UE_LOG(LogTemp, Error, TEXT("HTTPServer module NOT loaded"));
   }
   ```

5. **Check Editor Mode**:
   - Server only works in Editor, not PIE (Play In Editor)
   - Must be in actual Editor environment

### Server Starts But No Response

**Symptoms**:
- Server appears to start successfully
- No response to HTTP requests
- Connection timeout or refused

**Solutions**:

1. **Verify Server is Running**:
   ```cpp
   if (Server->IsServerRunning())
   {
       UE_LOG(LogTemp, Log, TEXT("Server is running"));
   }
   ```

2. **Check Route Registration**:
   ```cpp
   // Ensure route is properly bound
   FHttpRouteHandle RouteHandle = HttpRouter->BindRoute(
       FHttpPath(TEXT("/api/navigate")),
       EHttpServerRequestVerbs::VERB_POST,
       [this](const FHttpServerRequest& Request, const FHttpResultCallback& OnComplete)
       {
           // Handler code
       }
   );
   ```

3. **Test with Simple Request**:
   ```bash
   # Test if server responds at all
   curl -v http://localhost:8080/api/navigate
   ```

4. **Check Content-Type**:
   ```bash
   # Must include Content-Type header
   curl -X POST http://localhost:8080/api/navigate \
     -H "Content-Type: application/json" \
     -d '{}'
   ```

### Server Crashes on Request

**Symptoms**:
- UE5 crashes when sending HTTP request
- Access violation or segmentation fault

**Solutions**:

1. **Check Null Pointers**:
   ```cpp
   // Always verify pointers
   if (NavigationServer && NavigationServer->IsValidLowLevel())
   {
       NavigationServer->ProcessCommand(Command);
   }
   ```

2. **Thread Safety**:
   ```cpp
   // HTTP requests come on worker thread
   // Use AsyncTask for UObject access
   AsyncTask(ENamedThreads::GameThread, [this, Command]()
   {
       // Safe to access UObjects here
       ProcessCommand(Command);
   });
   ```

3. **Review Stack Trace**:
   ```
   Window → Developer Tools → Output Log
   Look for crash callstack
   ```

---

## Navigation Errors

### "Asset not found: AssetName"

**Cause**: Asset doesn't exist or wrong path

**Solutions**:

1. **Use Full Asset Path**:
   ```cpp
   // ✓ Correct:
   Server->OpenAsset(TEXT("/Game/Blueprints/BP_Character"));

   // ✗ Wrong:
   Server->OpenAsset(TEXT("BP_Character"));
   ```

2. **Verify Asset Exists**:
   ```cpp
   // Check in editor:
   bool bExists = UEditorAssetLibrary::DoesAssetExist(AssetPath);
   ```

3. **Check Asset Registry**:
   ```cpp
   // Asset may not be in registry yet
   FAssetRegistryModule& AssetRegistry =
       FModuleManager::LoadModuleChecked<FAssetRegistryModule>("AssetRegistry");
   AssetRegistry.Get().SearchAllAssets(true);  // Force scan
   ```

4. **Check Asset Name Format**:
   ```cpp
   // Common formats:
   "/Game/Blueprints/BP_Character"              // ✓
   "/Game/Blueprints/BP_Character.BP_Character" // ✓ (with asset name)
   "BP_Character"                               // ✗ (ambiguous)
   "Content/Blueprints/BP_Character"            // ✗ (filesystem path)
   ```

### "No active viewport found"

**Cause**: Viewport control requires active Level Editor viewport

**Solutions**:

1. **Ensure Level Editor is Open**:
   ```cpp
   FLevelEditorModule& LevelEditor =
       FModuleManager::GetModuleChecked<FLevelEditorModule>("LevelEditor");
   TSharedPtr<IAssetViewport> Viewport = LevelEditor.GetFirstActiveViewport();

   if (!Viewport.IsValid())
   {
       // Open level editor first
   }
   ```

2. **Not in PIE Mode**:
   - Exit Play In Editor mode
   - Must be in regular editor mode

3. **Open a Level**:
   - Ensure a level is loaded
   - Create or open a level if none exists

### Blueprint Node Not Found

**Cause**: Node doesn't exist or blueprint not properly opened

**Solutions**:

1. **Open Blueprint First**:
   ```cpp
   // Open before searching
   Server->OpenAsset(BlueprintPath);
   // Wait for async load
   Server->FindBlueprintNode(BlueprintPath, NodeName);
   ```

2. **Check Node Name**:
   - Use exact function name (case-sensitive)
   - Common names: "BeginPlay", "Tick", "Event BeginPlay"

3. **Verify Blueprint Type**:
   ```cpp
   UObject* Asset = LoadAsset(Path);
   if (UBlueprint* BP = Cast<UBlueprint>(Asset))
   {
       // It's a blueprint
   }
   ```

---

## Performance Issues

### Slow Asset Search

**Symptoms**:
- Search takes multiple seconds
- Editor becomes unresponsive

**Solutions**:

1. **Use Asset Registry Filters**:
   ```cpp
   FARFilter Filter;
   Filter.ClassNames.Add(UBlueprint::StaticClass()->GetFName());
   Filter.bRecursiveClasses = true;

   TArray<FAssetData> AssetDataList;
   AssetRegistry.GetAssets(Filter, AssetDataList);
   ```

2. **Cache Results**:
   ```cpp
   // Cache frequently accessed assets
   TMap<FString, UObject*> AssetCache;

   UObject* GetCachedAsset(const FString& Name)
   {
       if (AssetCache.Contains(Name))
           return AssetCache[Name];

       UObject* Asset = FindAsset(Name);
       AssetCache.Add(Name, Asset);
       return Asset;
   }
   ```

3. **Limit Search Scope**:
   ```cpp
   // Search specific directories only
   Filter.PackagePaths.Add("/Game/Blueprints");
   ```

4. **Async Search**:
   ```cpp
   // Don't block game thread
   AsyncTask(ENamedThreads::AnyBackgroundThreadNormalTask, [this]()
   {
       // Perform search
       // Return results via callback
   });
   ```

### High Memory Usage

**Symptoms**:
- Editor memory usage increases
- Out of memory errors

**Solutions**:

1. **Clear Asset Cache Periodically**:
   ```cpp
   void ClearOldCacheEntries()
   {
       // Clear cache entries older than 5 minutes
       AssetCache.Empty();
   }
   ```

2. **Don't Keep UObjects Alive**:
   ```cpp
   // ✗ Don't do this:
   TArray<UObject*> AllLoadedAssets;  // Prevents GC

   // ✓ Do this:
   TArray<FSoftObjectPath> AssetPaths;  // Just paths
   ```

3. **Limit Breadcrumb History**:
   ```cpp
   // Already implemented:
   if (BreadcrumbHistory.Num() > 100)
   {
       BreadcrumbHistory.RemoveAt(0);
   }
   ```

---

## API Issues

### Invalid JSON Error

**Symptoms**:
- "Invalid JSON" error
- 400 Bad Request response

**Solutions**:

1. **Validate JSON Format**:
   ```bash
   # Use a JSON validator
   echo '{"command":"FocusAsset","assetName":"Test"}' | jq .
   ```

2. **Check Quotes**:
   ```json
   // ✓ Correct:
   {"command": "FocusAsset"}

   // ✗ Wrong:
   {command: "FocusAsset"}  // Missing quotes on key
   {'command': 'FocusAsset'}  // Single quotes
   ```

3. **Escape Special Characters**:
   ```json
   {
       "assetName": "BP_Character\"Special\""  // Escape quotes
   }
   ```

### CORS Errors (Web Browser)

**Symptoms**:
- "CORS policy" error in browser console
- Requests work in Postman but not browser

**Solutions**:

1. **Add CORS Headers**:
   ```cpp
   // In HTTP response
   Response->Headers.Add("Access-Control-Allow-Origin", "*");
   Response->Headers.Add("Access-Control-Allow-Methods", "POST, GET, OPTIONS");
   Response->Headers.Add("Access-Control-Allow-Headers", "Content-Type");
   ```

2. **Handle OPTIONS Requests**:
   ```cpp
   // Add OPTIONS handler for preflight
   HttpRouter->BindRoute(
       FHttpPath(TEXT("/api/navigate")),
       EHttpServerRequestVerbs::VERB_OPTIONS,
       [](const FHttpServerRequest& Request, const FHttpResultCallback& OnComplete)
       {
           TUniquePtr<FHttpServerResponse> Response =
               FHttpServerResponse::Create(TEXT(""), TEXT("text/plain"));
           Response->Code = EHttpServerResponseCodes::Ok;
           Response->Headers.Add("Access-Control-Allow-Origin", "*");
           OnComplete(MoveTemp(Response));
           return true;
       }
   );
   ```

### Timeout Errors

**Symptoms**:
- Request times out
- No response after long wait

**Solutions**:

1. **Increase Client Timeout**:
   ```python
   # Python
   response = requests.post(url, json=data, timeout=30)  # 30 seconds
   ```

2. **Check for Blocking Operations**:
   ```cpp
   // Don't block the HTTP handler
   // Use async operations for long-running tasks
   ```

3. **Add Progress Reporting**:
   ```cpp
   // Return progress updates
   Response.Progress = CurrentStep / TotalSteps;
   ```

---

## Getting More Help

### Enable Verbose Logging

```cpp
// Add to NavigationServer.cpp
#define NAVIGATION_LOG_VERBOSE 1

#if NAVIGATION_LOG_VERBOSE
    UE_LOG(LogTemp, VeryVerbose, TEXT("NavigationServer: %s"), *Message);
#endif
```

### Check Output Log

```
Window → Developer Tools → Output Log
Filter by: LogTemp, LogNavigation
```

### Use AI Agents

```
@navigation-code-reviewer Please review my NavigationServer implementation
@ue5-architect How can I improve the architecture?
```

### Community Resources

- UE5 Forums: https://forums.unrealengine.com
- UE5 Documentation: https://docs.unrealengine.com
- Claude Code Docs: https://docs.claude.com

---

## Still Having Issues?

If none of these solutions work:

1. **Collect Information**:
   - UE5 version
   - Plugin version
   - Error messages (full text)
   - Steps to reproduce
   - Output Log contents

2. **Create Minimal Reproduction**:
   - Fresh UE5 project
   - Just the plugin
   - Single test case

3. **Review Source Code**:
   - Check templates/Source/*.cpp
   - Verify your modifications
   - Compare with original

4. **Ask Claude Code**:
   ```
   I'm having an issue with the UE5 Navigation Plugin:
   [Describe the problem in detail]
   [Include error messages]
   [Include steps to reproduce]
   ```

The AI agents are designed to help troubleshoot and fix issues!
