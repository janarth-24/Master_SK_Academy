import sys
import os

# Add the parent directory of 'backend' to sys.path so we can import backend.rag
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from backend.rag import rag_system
except ImportError:
    # Try importing directly if running from inside backend
    try:
        from rag import rag_system
    except ImportError:
        print("Could not import rag_system. Make sure you support running this script.")
        sys.exit(1)

def test_query(description, query, expected_substrings, forbidden_substrings=None):
    print(f"\n--- Testing: {description} ---")
    print(f"Query: {query}")
    response = rag_system.generate_response(query)
    answer = response['answer']
    print(f"Answer: {answer}")
    
    passed = True
    for sub in expected_substrings:
        if sub not in answer:
            print(f"FAILED: Expected substring '{sub}' not found.")
            passed = False
            
    if forbidden_substrings:
        for sub in forbidden_substrings:
            if sub in answer:
                print(f"FAILED: Forbidden substring '{sub}' found.")
                passed = False
                
    if passed:
        print("PASSED")
    else:
        print("FAILED")

if __name__ == "__main__":
    print("Initializing RAG System Verification...")
    
    # query = "What is the phone number?"
    test_query(
        "Phone Number", 
        "What is the contact number?", 
        ["+91 8608200435"]
    )

    test_query(
        "Email", 
        "What is the email address?", 
        ["senthil87ks@gmail.com"]
    )
    
    test_query(
        "Social Media", 
        "What is the Instagram link?", 
        ["instagram.com/master_sk_academy_vellore"]
    )

    test_query(
        "Contact Method Unavailability", 
        "Do you have WhatsApp?", 
        ["+91 8608200435"],
        forbidden_substrings=["WhatsApp", "yes", "sure"]
    )
