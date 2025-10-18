import requests
import json

def test_nodered_directly():
    """Test if Node-RED is responding directly"""
    print("Testing Node-RED directly...")
    
    test_data = {
        "test_event": {
            "message": "Direct test to Node-RED",
            "timestamp": "2025-01-01T12:00:00Z"
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:1880/api/knime-data",
            json=test_data,
            timeout=10
        )
        print(f"Node-RED direct test: {response.status_code}")
        print(response.json())
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Node-RED. Make sure it's running on port 1880.")
    except requests.exceptions.Timeout:
        print("❌ Node-RED timeout. Service might be overloaded.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_nodered_directly()