# API Reference - UE5 Navigation Plugin

Complete reference for the Navigation Plugin API (C++, HTTP, and Blueprint).

## Table of Contents

- [C++ API](#c-api)
- [HTTP API](#http-api)
- [Blueprint API](#blueprint-api)
- [Data Structures](#data-structures)
- [Error Codes](#error-codes)

---

## C++ API

### UNavigationServer

Main navigation server class providing all navigation functionality.

#### Server Management

##### `void StartHTTPServer(int32 Port = 8080)`

Start the HTTP server on the specified port.

**Parameters**:
- `Port` (int32): Port number (default: 8080)

**Example**:
```cpp
UNavigationServer* Server = NewObject<UNavigationServer>();
Server->StartHTTPServer(8080);
```

---

##### `void StopHTTPServer()`

Stop the HTTP server.

**Example**:
```cpp
Server->StopHTTPServer();
```

---

##### `bool IsServerRunning() const`

Check if the server is currently running.

**Returns**: `true` if running, `false` otherwise

**Example**:
```cpp
if (Server->IsServerRunning())
{
    UE_LOG(LogTemp, Log, TEXT("Server is active"));
}
```

---

#### Asset Navigation

##### `FNavigationResponse FocusAsset(const FString& AssetName)`

Focus on an asset in the Content Browser.

**Parameters**:
- `AssetName` (FString): Name of the asset to focus on

**Returns**: `FNavigationResponse` with success status

**Example**:
```cpp
FNavigationResponse Response = Server->FocusAsset(TEXT("BP_PlayerCharacter"));
if (Response.Success)
{
    UE_LOG(LogTemp, Log, TEXT("%s"), *Response.Message);
}
```

---

##### `FNavigationResponse OpenAsset(const FString& AssetPath)`

Open an asset in the appropriate editor.

**Parameters**:
- `AssetPath` (FString): Full asset path (e.g., `/Game/Blueprints/BP_Character`)

**Returns**: `FNavigationResponse` with success status

**Example**:
```cpp
FNavigationResponse Response = Server->OpenAsset(TEXT("/Game/Blueprints/BP_Character"));
```

---

##### `FNavigationResponse SearchAssets(const FString& SearchTerm)`

Search for assets by name.

**Parameters**:
- `SearchTerm` (FString): Search query

**Returns**: `FNavigationResponse` with matching assets in `AdditionalData`

**Example**:
```cpp
FNavigationResponse Response = Server->SearchAssets(TEXT("Player"));
for (const auto& Pair : Response.AdditionalData)
{
    UE_LOG(LogTemp, Log, TEXT("Found: %s"), *Pair.Value);
}
```

---

#### Viewport Control

##### `FNavigationResponse NavigateToLocation(const FVector& Location)`

Navigate the viewport camera to a specific location.

**Parameters**:
- `Location` (FVector): Target location

**Returns**: `FNavigationResponse` with success status

**Example**:
```cpp
FVector Target(0.0f, 0.0f, 500.0f);
FNavigationResponse Response = Server->NavigateToLocation(Target);
```

---

##### `FNavigationResponse SetViewportCamera(const FVector& Location, const FRotator& Rotation)`

Set viewport camera position and rotation.

**Parameters**:
- `Location` (FVector): Camera location
- `Rotation` (FRotator): Camera rotation

**Returns**: `FNavigationResponse` with success status

**Example**:
```cpp
FVector CamLoc(1000.0f, 0.0f, 500.0f);
FRotator CamRot(0.0f, 90.0f, 0.0f);
Server->SetViewportCamera(CamLoc, CamRot);
```

---

##### `FNavigationResponse FocusOnActor(const FString& ActorName)`

Focus the viewport on a specific actor.

**Parameters**:
- `ActorName` (FString): Name of the actor

**Returns**: `FNavigationResponse` with success status

**Example**:
```cpp
FNavigationResponse Response = Server->FocusOnActor(TEXT("PlayerStart"));
```

---

#### Blueprint Navigation

##### `FNavigationResponse FindBlueprintNode(const FString& BlueprintPath, const FString& NodeName)`

Find and navigate to a node in a Blueprint.

**Parameters**:
- `BlueprintPath` (FString): Full path to Blueprint
- `NodeName` (FString): Name of the node to find

**Returns**: `FNavigationResponse` with success status

**Example**:
```cpp
Server->FindBlueprintNode(
    TEXT("/Game/Blueprints/BP_Character"),
    TEXT("BeginPlay")
);
```

---

##### `FNavigationResponse HighlightBlueprintNode(const FString& BlueprintPath, const FString& NodeID)`

Highlight a specific node in a Blueprint graph.

**Parameters**:
- `BlueprintPath` (FString): Full path to Blueprint
- `NodeID` (FString): Node identifier

**Returns**: `FNavigationResponse` with success status

---

#### Code Navigation

##### `FNavigationResponse OpenSourceFile(const FString& FilePath, int32 LineNumber = -1)`

Open a source code file in the IDE.

**Parameters**:
- `FilePath` (FString): Full path to source file
- `LineNumber` (int32): Optional line number to jump to

**Returns**: `FNavigationResponse` with success status

**Example**:
```cpp
Server->OpenSourceFile(TEXT("C:/MyProject/Source/MyClass.cpp"), 42);
```

---

##### `FNavigationResponse FindSymbol(const FString& SymbolName)`

Search for a symbol (class, function, variable) in the codebase.

**Parameters**:
- `SymbolName` (FString): Symbol to search for

**Returns**: `FNavigationResponse` with search results

---

#### Editor Windows

##### `FNavigationResponse OpenEditorWindow(const FString& WindowType)`

Open a specific editor window.

**Parameters**:
- `WindowType` (FString): Window type (`"ContentBrowser"`, `"OutputLog"`, `"Viewport"`)

**Returns**: `FNavigationResponse` with success status

**Example**:
```cpp
Server->OpenEditorWindow(TEXT("ContentBrowser"));
```

---

##### `FNavigationResponse SwitchLevel(const FString& LevelName)`

Switch to a different level.

**Parameters**:
- `LevelName` (FString): Name of the level

**Returns**: `FNavigationResponse` with success status

**Example**:
```cpp
Server->SwitchLevel(TEXT("MainMenu"));
```

---

#### Project Structure

##### `FNavigationResponse GetProjectStructure()`

Get the project's directory structure.

**Returns**: `FNavigationResponse` with paths in `AdditionalData`

**Example**:
```cpp
FNavigationResponse Response = Server->GetProjectStructure();
```

---

##### `FNavigationResponse GetAssetHierarchy(const FString& RootPath)`

Get asset hierarchy for a specific path.

**Parameters**:
- `RootPath` (FString): Root path to scan

**Returns**: `FNavigationResponse` with assets in `AdditionalData`

**Example**:
```cpp
Server->GetAssetHierarchy(TEXT("/Game/Blueprints"));
```

---

#### Session Management

##### `FNavigationResponse SaveNavigationSession(const FString& SessionName)`

Save current navigation session.

**Parameters**:
- `SessionName` (FString): Name for the session

**Returns**: `FNavigationResponse` with success status

**Example**:
```cpp
Server->SaveNavigationSession(TEXT("BugFix_123"));
```

---

##### `FNavigationResponse LoadNavigationSession(const FString& SessionName)`

Load a previously saved navigation session.

**Parameters**:
- `SessionName` (FString): Name of the session to load

**Returns**: `FNavigationResponse` with success status

**Example**:
```cpp
Server->LoadNavigationSession(TEXT("BugFix_123"));
```

---

#### Breadcrumbs

##### `void AddBreadcrumb(const FString& Location, const FString& Description)`

Add a breadcrumb to navigation history.

**Parameters**:
- `Location` (FString): Location identifier
- `Description` (FString): Description of the action

**Example**:
```cpp
Server->AddBreadcrumb(TEXT("/Game/Maps/Level1"), TEXT("Explored level"));
```

---

##### `TArray<FString> GetBreadcrumbHistory()`

Get the breadcrumb history.

**Returns**: Array of breadcrumb strings

**Example**:
```cpp
TArray<FString> History = Server->GetBreadcrumbHistory();
for (const FString& Crumb : History)
{
    UE_LOG(LogTemp, Log, TEXT("%s"), *Crumb);
}
```

---

##### `FNavigationResponse NavigateToBreadcrumb(int32 Index)`

Navigate back to a specific breadcrumb.

**Parameters**:
- `Index` (int32): Breadcrumb index

**Returns**: `FNavigationResponse` with success status

**Example**:
```cpp
// Go back to previous location
Server->NavigateToBreadcrumb(History.Num() - 2);
```

---

## HTTP API

### Base URL

```
http://localhost:8080/api/navigate
```

### Request Format

All requests use POST method with JSON body.

**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "command": "CommandName",
  "assetName": "optional",
  "location": {"x": 0, "y": 0, "z": 0},
  "editorType": "optional",
  "timestamp": "optional"
}
```

### Response Format

**Success Response**:
```json
{
  "success": true,
  "message": "Operation successful",
  "error": "",
  "additionalData": {},
  "progress": 1.0
}
```

**Error Response**:
```json
{
  "success": false,
  "message": "",
  "error": "Error description",
  "additionalData": {},
  "progress": 0.0
}
```

---

### Available Commands

#### FocusAsset

Focus on an asset in Content Browser.

**Request**:
```json
{
  "command": "FocusAsset",
  "assetName": "BP_PlayerCharacter"
}
```

**cURL**:
```bash
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{"command":"FocusAsset","assetName":"BP_PlayerCharacter"}'
```

---

#### OpenAsset

Open an asset in its editor.

**Request**:
```json
{
  "command": "OpenAsset",
  "assetName": "/Game/Blueprints/BP_Character"
}
```

**cURL**:
```bash
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{"command":"OpenAsset","assetName":"/Game/Blueprints/BP_Character"}'
```

---

#### Search

Search for assets by name.

**Request**:
```json
{
  "command": "Search",
  "assetName": "Player"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Found 5 assets matching 'Player'",
  "additionalData": {
    "Result_0": "/Game/Blueprints/BP_Player",
    "Result_1": "/Game/Characters/Player_Character"
  }
}
```

**cURL**:
```bash
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{"command":"Search","assetName":"Player"}'
```

---

#### Navigate

Navigate viewport to a location.

**Request**:
```json
{
  "command": "Navigate",
  "location": {
    "x": 0,
    "y": 0,
    "z": 500
  }
}
```

**cURL**:
```bash
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{"command":"Navigate","location":{"x":0,"y":0,"z":500}}'
```

---

#### Blueprint

Find node in a Blueprint.

**Request**:
```json
{
  "command": "Blueprint",
  "assetName": "/Game/Blueprints/BP_Character",
  "editorType": "BeginPlay"
}
```

**cURL**:
```bash
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{"command":"Blueprint","assetName":"/Game/Blueprints/BP_Character","editorType":"BeginPlay"}'
```

---

#### FocusActor

Focus viewport on an actor.

**Request**:
```json
{
  "command": "FocusActor",
  "assetName": "PlayerStart"
}
```

---

## Blueprint API

All C++ functions are exposed to Blueprints via `UFUNCTION(BlueprintCallable)`.

### Getting the Navigation Server

```
Get Navigation Server (from module)
↓
Start HTTP Server (port: 8080)
```

### Common Blueprint Patterns

#### Start Server on Editor Start

```
Event Begin Play
↓
Get Navigation Server
↓
Start HTTP Server (Port: 8080)
```

#### Focus Asset by Name

```
Custom Event
↓
Get Navigation Server
↓
Focus Asset (AssetName: "BP_Character")
↓
Branch (Success?)
  ├─ True → Print Message (Success!)
  └─ False → Print Error
```

#### Navigate to Location

```
Custom Event
↓
Get Navigation Server
↓
Make Vector (X:0, Y:0, Z:500)
↓
Navigate to Location
↓
Print Response Message
```

---

## Data Structures

### FNavigationCommand

Command structure for navigation operations.

```cpp
USTRUCT(BlueprintType)
struct FNavigationCommand
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    FString Command;          // Command name

    UPROPERTY(BlueprintReadWrite)
    FString AssetName;        // Asset name or path

    UPROPERTY(BlueprintReadWrite)
    FVector Location;         // 3D location

    UPROPERTY(BlueprintReadWrite)
    FString EditorType;       // Editor type or node name

    UPROPERTY(BlueprintReadWrite)
    FString Timestamp;        // ISO 8601 timestamp
};
```

---

### FNavigationResponse

Response structure from navigation operations.

```cpp
USTRUCT(BlueprintType)
struct FNavigationResponse
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadWrite)
    bool Success = false;     // Operation success

    UPROPERTY(BlueprintReadWrite)
    FString Message;          // Success message

    UPROPERTY(BlueprintReadWrite)
    FString Error;            // Error message

    UPROPERTY(BlueprintReadWrite)
    TMap<FString, FString> AdditionalData;  // Extra data

    UPROPERTY(BlueprintReadWrite)
    float Progress = 0.0f;    // Progress (0.0 - 1.0)
};
```

---

## Error Codes

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success - Operation completed |
| 400 | Bad Request - Invalid JSON or missing required fields |
| 404 | Not Found - Asset, actor, or resource not found |
| 500 | Internal Server Error - Server-side error |

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Asset not found: X" | Asset doesn't exist or wrong path | Use full asset path |
| "No active viewport found" | Viewport not available | Open Level Editor viewport |
| "Command cannot be empty" | Missing command field | Include "command" in request |
| "Invalid JSON" | Malformed JSON | Validate JSON format |
| "Server not running" | HTTP server not started | Call StartHTTPServer() |

---

## Quick Reference

### Most Common Operations

**Start Server**:
```cpp
Server->StartHTTPServer(8080);
```

**Focus Asset**:
```bash
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{"command":"FocusAsset","assetName":"BP_Character"}'
```

**Navigate Viewport**:
```bash
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{"command":"Navigate","location":{"x":0,"y":0,"z":500}}'
```

**Search Assets**:
```bash
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{"command":"Search","assetName":"Player"}'
```

---

## See Also

- [Quick Start Guide](QUICK_START.md) - Get started quickly
- [Usage Examples](USAGE_EXAMPLES.md) - Detailed examples
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues
- [README](README.md) - Overview and documentation
