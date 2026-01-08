# Secure LLM Data Pipeline & Execution Architecture

**Role:** Senior Machine Learning Engineer & API Architect
**Objective:** Design a production-ready, secure, and reliable pipeline for LLM integration.

---

## 1. Data Handling Strategy

A robust pipeline must rigorously classify data to prevent leakage and hallucination while ensuring relevance.

### A. Data Classification
*   **Always Included (The Context):**
    *   **Definition:** Authoritative, static knowledge base (e.g., verified documentation, approved FAQs, database records).
    *   **Handling:** Vectorized and stored in a vector database (e.g., Chroma, pinecone) or structured knowledge graph.
    *   **Example:** "Company verified fee structure", "Official Return Policy".
*   **Conditionally Excluded (The Noise):**
    *   **Definition:** Data that is irrelevant, sensitive, or low-confidence for the specific query context.
    *   **Handling:** Filtered out *before* context construction using metadata tags or relevance thresholds (e.g., Cosine Similarity < 0.7).
    *   **Example:** "Internal employee comments", "Draft documents", "Unrelated product specs".
*   **Original User Query (The Immutable Inputs):**
    *   **Definition:** The raw input from the end-user.
    *   **Constraint:** Must **NEVER** be altered, summarized, or paraphrased by the `system` logic before reaching the LLM, as this introduces bias and destroys intent.

### B. Query Immutability Enforcement
To guarantee the user's intent is preserved:
1.  **Read-Only Propagation:** Pass the query string as a `final` or `const` variable throughout the pipeline.
2.  **Integrity Checks:** Hash user input at the entry point (API Gateway) and verify the hash matches the input sent to the LLM model adapter.
3.  **No "Prompt Injection" Filtering on the Query:** Sanitize for *security* (e.g., SQL injection), but do not rewrite the semantic meaning. Handle "jailbreaks" via the System Prompt, not by editing the user's words.

---

## 2. Secure Code Execution (API Key Management)

Security is paramount. Defaulting to hardcoded keys is immediate technical debt and a security vulnerability.

### A. Storage & Injection
*   **Storage:** Keys typically live in a Secrets Manager (AWS Secrets Manager, HashiCorp Vault) or Environment Variables (`.env`) for local dev. **Never in git**.
*   **Runtime Injection:** The application reads from the environment at startup.
*   **Principle of Least Privilege:** The API token used should have limits (quota, scopes) strictly necessary for inference.

### B. Implementation Rules
1.  **Environment Isolation:** Use different keys for `DEV`, `staging`, and `prod`.
2.  **Code Separation:** The inference logic (calling the LLM) should be decoupled from the key loading logic.

---

## 3. Production Code Example (Python)

This example demonstrates loading data, enforcing query immutability, and secure execution.

```python
import os
import hashlib
from typing import List, Dict
from dotenv import load_dotenv

# 1. Secure Configuration
load_dotenv() # Load from .env locally; in prod, this might be injected by the orchestrator
API_KEY = os.getenv("LLM_PROVIDER_API_KEY")

if not API_KEY:
    raise RuntimeError("CRITICAL: API Key not found in environment.")

class LLMPipeline:
    def __init__(self, training_data: List[Dict]):
        # "Always Included" - Simulated Vector Store
        self.knowledge_base = training_data

    def _get_context(self, query: str) -> str:
        """
        Retrieves context. Filters "Excluded" data based on relevance/rules.
        """
        relevant_chunks = []
        for item in self.knowledge_base:
            # 2. Conditional Exclusion logic (Simplified)
            if item.get("status") == "draft":
                continue # Exclude drafts
            if "internal_only" in item.get("tags", []):
                continue # Exclude internal data
            
            # Simple keyword match for demo (Real world: use Vector Similarity)
            if any(word in item["content"].lower() for word in query.lower().split()):
                relevant_chunks.append(item["content"])
        
        return "\n\n".join(relevant_chunks)

    def execute_inference(self, user_query: str) -> str:
        # 3. Query Immutability Check
        original_hash = hashlib.sha256(user_query.encode()).hexdigest()

        # ... (Processing happens) ...
        
        # Verify Query wasn't mutated before forming the prompt
        current_hash = hashlib.sha256(user_query.encode()).hexdigest()
        if current_hash != original_hash:
            raise ValueError("Integrity Error: User query was altered internally!")

        context = self._get_context(user_query)
        
        # 4. Secure Execution
        # Note: We pass the API_KEY explicitly to the client, never hardcoded.
        try:
            # Simulated API Call
            # client = OpenAI(api_key=API_KEY)
            # response = client.chat.completions.create(...)
            
            print(f">>> Authenticating with key: {API_KEY[:5]}***")
            print(f">>> Sending Prompt with Context length: {len(context)}")
            print(f">>> User Query (Verbatim): {user_query}")
            
            return "Simulated LLM Response based on secure context."
            
        except Exception as e:
            # 5. Error Handling: Log error, but NEVER log the full API Key
            print(f"Execution failed: {str(e)}")
            return "System Error"

# --- Runtime Usage ---
if __name__ == "__main__":
    # Mock Data
    data = [
        {"content": "Product A costs $10.", "status": "approved", "tags": ["public"]},
        {"content": "Product B release date is TBD.", "status": "draft", "tags": ["public"]}, # Should be excluded
        {"content": "Admin password is '1234'.", "status": "approved", "tags": ["internal_only"]} # Should be excluded
    ]

    pipeline = LLMPipeline(data)
    
    # Execution
    result = pipeline.execute_inference("How much does Product A cost?")
    print(f"Result: {result}")
```

---

## 4. Common Mistakes & Risks

1.  **Logging Secrets:**
    *   *Risk:* Printing the `API_KEY` or the entire `request` object (headers included) to stdout/logs.
    *   *Mitigation:* Use log redaction tools.

2.  **Mutating the Query:**
    *   *Risk:* Pre-processing the user query (e.g., "correcting" grammar) can change the semantic meaning, leading to wrong retrieval.
    *   *Mitigation:* Treat `user_query` as Read-Only. Use a separate variable for `search_query` if optimization is needed.

3.  **Mixing Training vs. Inference:**
    *   *Risk:* Hardcoding "training examples" directly into the inference code flow.
    *   *Mitigation:* Keep data stored externally (database/files). Load it dynamically.

4.  **Implicit Auth:**
    *   *Risk:* Relying on global config without validation, leading to runtime crashes in Prod.
    *   *Mitigation:* Fail fast at startup if keys are missing (as shown in the example provided).
