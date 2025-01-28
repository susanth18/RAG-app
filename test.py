import requests
import json

BASE_URL = "http://localhost:5000"
ENDPOINT = "/ask"

test_queriess = [
    "Effect of DeepSeek on US stock market",
    "comparison on DeepSeek and GPT"
]

def test_queries():
    for query in test_queriess:
        try:
            print(f"\nSending query: {query}")
            response = requests.post(
                f"{BASE_URL}{ENDPOINT}",
                json={"question": query},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print("Response:")
                print(json.dumps(response.json(), indent=2))
            else:
                print(f"Error: {response.status_code}")
                print(response.text)
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")

if __name__ == "__main__":
    test_queries()