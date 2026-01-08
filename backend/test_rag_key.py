
import sys
import os

# Add backend directory to path so we can import rag
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from rag import rag_system
    
    print("Testing RAG System with new API Key...")
    response = rag_system.generate_response("What is the phone number of the academy?")
    
    print("\n--- RESPONSE ---")
    print(response['answer'])
    print("----------------")
    
    if "8608200435" in response['answer'] or "contact" in response['answer'].lower():
         print("SUCCESS: RAG system retrieved context and generated response.")
    else:
         print("WARNING: Response might not be accurate, please check logs.")

except Exception as e:
    print(f"ERROR: {e}")
