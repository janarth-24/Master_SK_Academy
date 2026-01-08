import requests
import json
import time

def test(query):
    print(f"Query: {query}")
    try:
        r = requests.post("http://localhost:8000/chat", json={"message": query})
        if r.status_code == 200:
            print(f"Response: {r.json()['answer']}")
        else:
            print(f"Status: {r.status_code}, Text: {r.text}")
    except Exception as e:
        print(f"Error: {e}")

print("Waiting for server to stabilize...")
time.sleep(2)

def check_bold(query, keywords):
    print(f"\nQuery: {query}")
    try:
        r = requests.post("http://localhost:8000/chat", json={"message": query})
        if r.status_code == 200:
            ans = r.json()['answer']
            print(f"Response: {ans}")
            
            missing = [k for k in keywords if f"<b>{k}</b>" not in ans and f"<b>{k}" not in ans]
            if not missing:
                print("PASSED: All keywords bolded.")
            else:
                print(f"WARNING: Missing bold tags for: {missing}")
                # Sometimes LLM might do <b> ₹4000 </b> with spaces, or <b>₹4000</b>.
        else:
            print(f"Status: {r.status_code}, Text: {r.text}")
    except Exception as e:
        print(f"Error: {e}")

check_bold("What are the fees for Class 10 and 12?", ["4000", "5000"])
check_bold("How many students and branches?", ["80+", "2+"])
