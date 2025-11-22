# UE5 Navigation Plugin - Usage Examples

Complete examples for using the UE5 Navigation Plugin in various scenarios.

## Table of Contents

1. [Basic Setup](#basic-setup)
2. [Asset Navigation](#asset-navigation)
3. [Viewport Control](#viewport-control)
4. [Blueprint Navigation](#blueprint-navigation)
5. [Session Management](#session-management)
6. [External Integration](#external-integration)

## Basic Setup

### In-Editor Setup

```cpp
// In any Blueprint or C++ class
UNavigationServer* NavServer = NewObject<UNavigationServer>();
NavServer->StartHTTPServer(8080);
```

### Menu Access

1. Open Unreal Editor
2. Go to **Tools → Start Navigation Server**
3. Server starts on port 8080

## Asset Navigation

### Focus on Asset by Name

**C++**:
```cpp
UNavigationServer* Server = GetNavigationServer();
FNavigationResponse Response = Server->FocusAsset(TEXT("BP_PlayerCharacter"));

if (Response.Success)
{
    UE_LOG(LogTemp, Log, TEXT("Success: %s"), *Response.Message);
}
else
{
    UE_LOG(LogTemp, Error, TEXT("Error: %s"), *Response.Error);
}
```

**HTTP API**:
```bash
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{
    "command": "FocusAsset",
    "assetName": "BP_PlayerCharacter"
  }'
```

**Python**:
```python
import requests

response = requests.post(
    "http://localhost:8080/api/navigate",
    json={"command": "FocusAsset", "assetName": "BP_PlayerCharacter"}
)

result = response.json()
if result["success"]:
    print(f"Success: {result['message']}")
else:
    print(f"Error: {result['error']}")
```

### Open Asset in Editor

**C++**:
```cpp
FNavigationResponse Response = Server->OpenAsset(
    TEXT("/Game/Blueprints/BP_PlayerCharacter")
);
```

**HTTP API**:
```bash
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{
    "command": "OpenAsset",
    "assetName": "/Game/Blueprints/BP_PlayerCharacter"
  }'
```

### Search Assets

**C++**:
```cpp
FNavigationResponse Response = Server->SearchAssets(TEXT("Player"));

// Results are in AdditionalData
for (const auto& Pair : Response.AdditionalData)
{
    UE_LOG(LogTemp, Log, TEXT("%s: %s"), *Pair.Key, *Pair.Value);
}
```

**HTTP API**:
```bash
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Search",
    "assetName": "Player"
  }'
```

**Response**:
```json
{
  "success": true,
  "message": "Found 5 assets matching 'Player'",
  "additionalData": {
    "Result_0": "/Game/Blueprints/BP_PlayerCharacter",
    "Result_1": "/Game/Blueprints/BP_PlayerController",
    "Result_2": "/Game/Characters/Player_Character"
  }
}
```

## Viewport Control

### Navigate to Location

**C++**:
```cpp
FVector TargetLocation(0.0f, 0.0f, 500.0f);
FNavigationResponse Response = Server->NavigateToLocation(TargetLocation);
```

**HTTP API**:
```bash
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Navigate",
    "location": {
      "x": 0,
      "y": 0,
      "z": 500
    }
  }'
```

**Python**:
```python
def navigate_to_location(x, y, z):
    response = requests.post(
        "http://localhost:8080/api/navigate",
        json={
            "command": "Navigate",
            "location": {"x": x, "y": y, "z": z}
        }
    )
    return response.json()

# Navigate to specific coordinates
result = navigate_to_location(100, 200, 500)
```

### Set Camera Position and Rotation

**C++**:
```cpp
FVector CameraLocation(1000.0f, 0.0f, 500.0f);
FRotator CameraRotation(0.0f, 90.0f, 0.0f);

FNavigationResponse Response = Server->SetViewportCamera(
    CameraLocation,
    CameraRotation
);
```

### Focus on Actor

**C++**:
```cpp
FNavigationResponse Response = Server->FocusOnActor(TEXT("PlayerStart"));
```

**HTTP API**:
```bash
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{
    "command": "FocusActor",
    "assetName": "PlayerStart"
  }'
```

## Blueprint Navigation

### Find Blueprint Node

**C++**:
```cpp
FNavigationResponse Response = Server->FindBlueprintNode(
    TEXT("/Game/Blueprints/BP_PlayerCharacter"),
    TEXT("BeginPlay")
);
```

**HTTP API**:
```bash
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Blueprint",
    "assetName": "/Game/Blueprints/BP_PlayerCharacter",
    "editorType": "BeginPlay"
  }'
```

## Session Management

### Save Navigation Session

**C++**:
```cpp
// After navigating to multiple locations
Server->AddBreadcrumb(TEXT("/Game/Maps/Level1"), TEXT("Explored level"));
Server->AddBreadcrumb(TEXT("BP_Enemy"), TEXT("Fixed enemy AI"));

// Save the session
FNavigationResponse Response = Server->SaveNavigationSession(TEXT("BugFix_123"));
```

### Load Navigation Session

**C++**:
```cpp
FNavigationResponse Response = Server->LoadNavigationSession(TEXT("BugFix_123"));

// Get breadcrumb history
TArray<FString> History = Server->GetBreadcrumbHistory();
for (const FString& Breadcrumb : History)
{
    UE_LOG(LogTemp, Log, TEXT("%s"), *Breadcrumb);
}
```

### Navigate Back Using Breadcrumbs

**C++**:
```cpp
// Go back to previous location
FNavigationResponse Response = Server->NavigateToBreadcrumb(
    Server->GetBreadcrumbHistory().Num() - 2
);
```

## External Integration

### Python Automation Script

```python
#!/usr/bin/env python3
"""
UE5 Navigation Automation Script
Automates common navigation tasks in Unreal Editor
"""

import requests
import time
from typing import Dict, Any

class UE5Navigator:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.endpoint = f"{base_url}/api/navigate"

    def send_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """Send a navigation command to UE5."""
        payload = {"command": command, **kwargs}
        try:
            response = requests.post(self.endpoint, json=payload, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def focus_asset(self, asset_name: str) -> Dict[str, Any]:
        """Focus on an asset in Content Browser."""
        return self.send_command("FocusAsset", assetName=asset_name)

    def open_asset(self, asset_path: str) -> Dict[str, Any]:
        """Open an asset in the appropriate editor."""
        return self.send_command("OpenAsset", assetName=asset_path)

    def search_assets(self, search_term: str) -> Dict[str, Any]:
        """Search for assets by name."""
        return self.send_command("Search", assetName=search_term)

    def navigate_to(self, x: float, y: float, z: float) -> Dict[str, Any]:
        """Navigate viewport to location."""
        return self.send_command(
            "Navigate",
            location={"x": x, "y": y, "z": z}
        )

    def focus_actor(self, actor_name: str) -> Dict[str, Any]:
        """Focus viewport on an actor."""
        return self.send_command("FocusActor", assetName=actor_name)

# Example: Automated Asset Review Workflow
def review_player_assets():
    """Review all player-related assets."""
    nav = UE5Navigator()

    # Search for player assets
    print("🔍 Searching for player assets...")
    result = nav.search_assets("Player")

    if not result["success"]:
        print(f"❌ Error: {result['error']}")
        return

    print(f"✅ Found {result['message']}")

    # Open each asset
    for key, asset_path in result.get("additionalData", {}).items():
        print(f"\n📂 Opening: {asset_path}")
        nav.open_asset(asset_path)
        time.sleep(2)  # Wait for asset to open

    print("\n✅ Review complete!")

# Example: Viewport Tour
def viewport_tour():
    """Take a tour of important locations."""
    nav = UE5Navigator()

    locations = [
        (0, 0, 500, "Spawn Point"),
        (1000, 0, 500, "Checkpoint 1"),
        (2000, 1000, 500, "Boss Arena"),
        (0, 2000, 500, "End Point")
    ]

    print("🎬 Starting viewport tour...")

    for x, y, z, name in locations:
        print(f"\n📍 Navigating to: {name}")
        result = nav.navigate_to(x, y, z)

        if result["success"]:
            print(f"✅ {result['message']}")
        else:
            print(f"❌ {result['error']}")

        time.sleep(3)  # Pause at each location

    print("\n✅ Tour complete!")

if __name__ == "__main__":
    # Run examples
    review_player_assets()
    viewport_tour()
```

### JavaScript Web Dashboard

```javascript
// ue5-nav-dashboard.js
// Real-time UE5 Navigation Dashboard

class UE5NavigationDashboard {
    constructor(baseUrl = 'http://localhost:8080') {
        this.baseUrl = baseUrl;
        this.endpoint = `${baseUrl}/api/navigate`;
    }

    async sendCommand(command, params = {}) {
        try {
            const response = await fetch(this.endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command, ...params })
            });
            return await response.json();
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    async focusAsset(assetName) {
        return this.sendCommand('FocusAsset', { assetName });
    }

    async searchAssets(searchTerm) {
        return this.sendCommand('Search', { assetName: searchTerm });
    }

    async navigateTo(x, y, z) {
        return this.sendCommand('Navigate', {
            location: { x, y, z }
        });
    }

    // Create interactive dashboard
    createDashboard() {
        const html = `
            <div id="ue5-dashboard">
                <h2>UE5 Navigation Dashboard</h2>

                <div class="search-section">
                    <input type="text" id="asset-search" placeholder="Search assets...">
                    <button onclick="dashboard.search()">Search</button>
                </div>

                <div class="results" id="results"></div>

                <div class="viewport-control">
                    <h3>Viewport Control</h3>
                    <input type="number" id="pos-x" placeholder="X">
                    <input type="number" id="pos-y" placeholder="Y">
                    <input type="number" id="pos-z" placeholder="Z">
                    <button onclick="dashboard.navigate()">Navigate</button>
                </div>
            </div>
        `;
        document.body.innerHTML = html;
    }

    async search() {
        const searchTerm = document.getElementById('asset-search').value;
        const result = await this.searchAssets(searchTerm);

        const resultsDiv = document.getElementById('results');
        if (result.success) {
            const assets = Object.values(result.additionalData || {});
            resultsDiv.innerHTML = assets.map(asset =>
                `<div class="asset-item" onclick="dashboard.focusAsset('${asset}')">
                    ${asset}
                </div>`
            ).join('');
        } else {
            resultsDiv.innerHTML = `<div class="error">${result.error}</div>`;
        }
    }

    async navigate() {
        const x = parseFloat(document.getElementById('pos-x').value);
        const y = parseFloat(document.getElementById('pos-y').value);
        const z = parseFloat(document.getElementById('pos-z').value);

        const result = await this.navigateTo(x, y, z);
        alert(result.success ? result.message : result.error);
    }
}

// Initialize dashboard
const dashboard = new UE5NavigationDashboard();
dashboard.createDashboard();
```

### PowerShell Automation

```powershell
# UE5-Navigation.ps1
# PowerShell functions for UE5 Navigation

$UE5_NAV_URL = "http://localhost:8080/api/navigate"

function Invoke-UE5Command {
    param(
        [string]$Command,
        [hashtable]$Params = @{}
    )

    $body = @{ command = $Command } + $Params | ConvertTo-Json

    try {
        $response = Invoke-RestMethod -Uri $UE5_NAV_URL -Method Post -Body $body -ContentType "application/json"
        return $response
    } catch {
        Write-Error "Failed to execute command: $_"
        return $null
    }
}

function Focus-UE5Asset {
    param([string]$AssetName)
    Invoke-UE5Command -Command "FocusAsset" -Params @{ assetName = $AssetName }
}

function Open-UE5Asset {
    param([string]$AssetPath)
    Invoke-UE5Command -Command "OpenAsset" -Params @{ assetName = $AssetPath }
}

function Search-UE5Assets {
    param([string]$SearchTerm)
    Invoke-UE5Command -Command "Search" -Params @{ assetName = $SearchTerm }
}

function Move-UE5Viewport {
    param(
        [double]$X,
        [double]$Y,
        [double]$Z
    )
    Invoke-UE5Command -Command "Navigate" -Params @{
        location = @{ x = $X; y = $Y; z = $Z }
    }
}

# Example usage:
# Focus-UE5Asset -AssetName "BP_PlayerCharacter"
# Search-UE5Assets -SearchTerm "Player"
# Move-UE5Viewport -X 0 -Y 0 -Z 500
```

## Best Practices

1. **Always check response success status**
   ```cpp
   if (Response.Success) {
       // Handle success
   } else {
       UE_LOG(LogTemp, Error, TEXT("Error: %s"), *Response.Error);
   }
   ```

2. **Use full asset paths for reliability**
   ```cpp
   // ✅ Good
   Server->OpenAsset(TEXT("/Game/Blueprints/BP_PlayerCharacter"));

   // ⚠️ Less reliable
   Server->FocusAsset(TEXT("BP_PlayerCharacter"));
   ```

3. **Handle network errors in external integrations**
   ```python
   try:
       response = requests.post(url, json=data, timeout=5)
       response.raise_for_status()
   except requests.exceptions.RequestException as e:
       print(f"Error: {e}")
   ```

4. **Use breadcrumbs for navigation history**
   ```cpp
   Server->AddBreadcrumb(Location, Description);
   // ... later ...
   TArray<FString> History = Server->GetBreadcrumbHistory();
   ```
