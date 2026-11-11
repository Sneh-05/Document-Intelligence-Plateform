import os
import random
import time
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

load_dotenv()

# Initialize official SDK client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-3.8-flash"


def generate_answer(query: str, context_chunks: list[str], max_retries: int = 4) -> str:
    """
    Sends query and retrieved context to Gemini with exponential backoff 
    and jitter to handle 503 (Server Busy) and 429 (Rate Limit) errors.
    """
    if not context_chunks:
        return "No relevant context found to answer the question."

    context = "\n\n".join(context_chunks)

    prompt = f"""You are an intelligent document assistant.
Use ONLY the context provided below to answer the question.
If the answer is not found in the context, say "I could not find this information in the document."

Context:
{context}

Question: {query}

Answer:"""

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )
            return response.text

        except APIError as e:
            # Handle 503 (Server Busy/High Demand) or 429 (Rate Limited)
            if e.code in [503, 429]:
                if attempt == max_retries:
                    return f"Error: The AI model is currently busy ({e.code}). Please try again in a few moments."
                
                # Exponential backoff with jitter (e.g., ~4s, ~8s, ~16s)
                base_delay = 2 ** (attempt + 1)
                jitter = random.uniform(0.5, 1.5)
                wait_time = base_delay + jitter
                
                print(f"Server returned {e.code} (High Demand/Rate Limit). Retrying in {wait_time:.1f}s... (Attempt {attempt}/{max_retries})")
                time.sleep(wait_time)
            else:
                return f"API Error ({e.code}): {e.message}"
                
        except Exception as e:
            if attempt == max_retries:
                return f"Unexpected Error: {str(e)}"
            
            print(f"Network error on attempt {attempt}/{max_retries}. Retrying in 3s...")
            time.sleep(3)
