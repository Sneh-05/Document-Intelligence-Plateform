import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.8-flash")

def generate_answer(query: str, context_chunks: list[str]) -> str:
    """
    Sends the query and retrieved context to Gemini and returns an answer.

    Args:
        query: The user's natural language question.
        context_chunks: Relevant text chunks retrieved from FAISS.

    Returns:
        The generated answer as a string.
    """
    if not context_chunks:
        return "No relevant context found to answer the question."

    # Combine chunks into a single context block
    context = "\n\n".join(context_chunks)

    prompt = f"""You are an intelligent document assistant.
Use ONLY the context provided below to answer the question.
If the answer is not found in the context, say "I could not find this information in the document."

Context:
{context}

Question: {query}

Answer:"""

    response = model.generate_content(prompt)
    return response.text



if __name__ == "__main__":
    sample_chunks = [
        "The contract was signed in January 2020.",
        "Payment terms are net 30 days.",
        "This agreement is governed by the laws of New York."
    ]

    query = "What are the payment terms?"
    answer = generate_answer(query, sample_chunks)
    print("Answer:", answer)
