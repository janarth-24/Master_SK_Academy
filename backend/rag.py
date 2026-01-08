import os
import re
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RAGBrain:
    def __init__(self, data_path: str = None):
        if data_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(base_dir, "data", "academy_data.md")
        self.data_path = data_path
        self.chunks: List[str] = []
        self.embeddings = None
        
        # Load embedding model (lightweight, runs locally)
        print("Loading embedding model...")
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize knowledge base
        self.load_and_process_data()
        
    def load_and_process_data(self):
        """Reads markdown file and creates chunks."""
        if not os.path.exists(self.data_path):
            print(f"Warning: Data file not found at {self.data_path}")
            return

        with open(self.data_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Simple semantic chunking by headers or paragraphs
        # For this size, splitting by sections starts (#) is good
        sections = re.split(r'(?=\n##? )', text)
        self.chunks = [s.strip() for s in sections if s.strip()]
        
        print(f"Created {len(self.chunks)} chunks from knowledge base.")
        
        # Create embeddings
        if self.chunks:
            self.embeddings = self.embed_model.encode(self.chunks)
            print("Knowledge base embeddings created.")

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        """Finds most relevant chunks for a query."""
        if not self.chunks or self.embeddings is None:
            return []
            
        query_embedding = self.embed_model.encode([query])
        
        # Calculate similarity
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            score = similarities[idx]
            if score > 0.25: # relevancy threshold
                results.append(self.chunks[idx])
                
        return results

    def generate_response(self, query: str) -> Dict[str, str]:
        """
        Full RAG pipeline: Retrieve + Generate
        """
        retrieved_context = self.retrieve(query)
        context_text = "\n\n".join(retrieved_context)
        
        # Check for API Key
        api_key = os.getenv("OPENAI_API_KEY")
        
        if api_key:
            # Determine API URL and Model based on key type
            api_url = "https://api.openai.com/v1/chat/completions"
            model = "gpt-4o-mini"
            headers = {"Authorization": f"Bearer {api_key}"}

            if api_key.startswith("sk-or-v1"):
                 api_url = "https://openrouter.ai/api/v1/chat/completions"
                 # OpenRouter often requires a Referer header
                 headers["HTTP-Referer"] = "http://localhost:8000" 
                 headers["X-Title"] = "Master SK Academy RAG"
                 # Use a model that OpenRouter supports (mapping generic to one available)
                 model = "openai/gpt-4o-mini" # Standard OpenRouter ID

            try:
                import requests
                
                prompt = f"""
You are the Official Website Support Assistant for "Master SK Academy". Your objective is to answer visitor queries with absolute accuracy, using ONLY the approved website data provided below.

### APPROVED CONTACT DATA (AUTHORITATIVE TRUTH)
*   <b>Phone:</b> +91 8608200435
*   <b>Email:</b> senthil87ks@gmail.com
*   <b>Address:</b> Master SK Academy, No: 381/1A, TVS Complex, First Floor, Kalinjur Main Road, Kalinjur, Vellore – 632 006
*   <b>Instagram:</b> https://www.instagram.com/master_sk_academy_vellore/?utm_source=qr

### STRICT RESPONSE RULES
1.  **Contact Queries:** When asked for phone, email, address, or social media, you must use the EXACT details listed above.
2.  **Course/Fee Queries:** Answer using the retrieved CONTEXT sections below.
3.  **No Hallucinations:** If a detail (e.g., a specific teacher's phone number) is not in the data, state it is not available.
4.  **Format:** Use HTML <b> tags for bold text (e.g., <b>Phone:</b>). Do NOT use Markdown asterisks (**).
5.  **Highlighting:** ALWAYS use <b> tags to bold important keywords, especially:
    *   Class Names (e.g., <b>Class 10</b>, <b>Class 12</b>)
    *   Fees and Numbers (e.g., <b>₹4000</b>, <b>₹5000</b>, <b>80+ students</b>)
    *   Key specifics in the answer.


### FALLBACK TEMPLATES
*   *For missing contact info:* "The website does not list that specific contact detail. Please use the official phone number: +91 8608200435."
*   *General:* "I apologize, but I don't have that information available right now."

### CONTEXT FROM WEBSITE
{context_text}

### USER QUESTION
{query}
"""
                response = requests.post(
                    api_url,
                    headers=headers,
                    json={
                        "model": model, 
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.2
                    }
                )
                
                if response.status_code == 200:
                    return {
                        "answer": response.json()['choices'][0]['message']['content'],
                        "context": retrieved_context
                    }
                else:
                    print(f"API Error {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"LLM Error: {e}")
                
        # FALLBACK (No API Key or Error)
        # We construct a response based on retrieval success
        if not retrieved_context:
            return {
                "answer": "I apologize, but I couldn't find information about that right now. Please contact our office at +91 86082 00435 for detailed assistance.",
                "context": []
            }
        
        return {
            "answer": "Here is the relevant information I found from the Academy's knowledge base:\n\n" + 
                      "\n---\n".join(retrieved_context) + 
                      "\n\n(Note: API Key issue or not set. Using offline fallback.)",
            "context": retrieved_context
        }

# Singleton instance
rag_system = RAGBrain()
