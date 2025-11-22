---
description: Generate test scripts and examples for the Navigation Plugin HTTP API
---

# Test Navigation API

Create test scripts and examples to validate the UE5 Navigation Plugin's HTTP API functionality.

## Test Generation Options

1. **cURL Test Scripts**
   - Generate bash/PowerShell scripts with cURL commands
   - Test all available endpoints
   - Include various parameter combinations

2. **Python Test Suite**
   - Create Python scripts using `requests` library
   - Implement automated test cases
   - Add response validation

3. **Postman Collection**
   - Generate Postman collection JSON
   - Include all API endpoints
   - Add example requests and responses

4. **JavaScript/Node.js Examples**
   - Create Node.js integration examples
   - Show how to build automation tools
   - Demonstrate real-time navigation control

## Test Cases to Include

### Basic Navigation
```bash
# Focus on asset
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{
    "command": "FocusAsset",
    "assetName": "BP_PlayerCharacter"
  }'

# Open asset
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{
    "command": "OpenAsset",
    "assetName": "/Game/Blueprints/BP_PlayerCharacter"
  }'

# Search assets
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Search",
    "assetName": "Player"
  }'
```

### Viewport Navigation
```bash
# Navigate to location
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Navigate",
    "location": {
      "x": 0,
      "y": 0,
      "z": 100
    }
  }'

# Focus on actor
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{
    "command": "FocusActor",
    "assetName": "PlayerStart"
  }'
```

### Blueprint Navigation
```bash
# Find blueprint node
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Blueprint",
    "assetName": "/Game/Blueprints/BP_PlayerCharacter",
    "editorType": "BeginPlay"
  }'
```

## Python Test Example

Generate a complete Python test script:

```python
import requests
import json

class NavigationAPITester:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.endpoint = f"{base_url}/api/navigate"

    def send_command(self, command_data):
        response = requests.post(self.endpoint, json=command_data)
        return response.json()

    def test_focus_asset(self, asset_name):
        command = {
            "command": "FocusAsset",
            "assetName": asset_name
        }
        return self.send_command(command)

    def test_navigate_to_location(self, x, y, z):
        command = {
            "command": "Navigate",
            "location": {"x": x, "y": y, "z": z}
        }
        return self.send_command(command)

    def run_all_tests(self):
        print("🧪 Running Navigation API Tests...")

        # Test 1: Focus Asset
        print("✓ Test 1: Focus Asset")
        result = self.test_focus_asset("BP_PlayerCharacter")
        print(f"  Result: {result}")

        # Test 2: Navigate to Location
        print("✓ Test 2: Navigate to Location")
        result = self.test_navigate_to_location(0, 0, 100)
        print(f"  Result: {result}")

        print("✅ All tests completed!")

if __name__ == "__main__":
    tester = NavigationAPITester()
    tester.run_all_tests()
```

## Instructions

1. Ask user which test format they prefer
2. Generate the appropriate test files
3. Include instructions for running the tests
4. Add expected response examples
5. Include troubleshooting tips
