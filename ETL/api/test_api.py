import requests
import time

def comprehensive_test():
    print("=== COMPREHENSIVE API TEST ===")
    
    # Test 1: Flask health
    print("1. Testing Flask health...")
    try:
        response = requests.get("http://127.0.0.1:5000/api/health", timeout=5)
        print(f"   ✅ Flask: {response.status_code}")
    except:
        print("   ❌ Flask not responding")
        return
    
    # Test 2: Node-RED direct
    print("2. Testing Node-RED direct...")
    try:
        response = requests.post(
            "http://localhost:1880/api/knime-data",
            json={"test": "data"},
            timeout=5
        )
        print(f"   ✅ Node-RED: {response.status_code}")
    except:
        print("   ❌ Node-RED not responding")
        return
    
    # Test 3: Complete flow
    print("3. Testing complete flow...")
    test_data = {
        "events": [
            {
                "event_id": "test_001",
                "message": "Test event from Knime simulation",
                "status": "success"
            }
        ]
    }
    
    try:
        response = requests.post(
            "http://127.0.0.1:5000/api/forward-to-nodered",
            json=test_data,
            timeout=10
        )
        print(f"   ✅ Complete flow: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Flow failed: {e}")

if __name__ == "__main__":
    comprehensive_test()