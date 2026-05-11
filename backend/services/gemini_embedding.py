from google import genai

def get_gemini_embedding(text: str) -> list[float]:
    """
    Generates a dense vector embedding using Gemini for a given text.
    """
    # Initialize the client. Assumes GOOGLE_API_KEY is in the environment.
    client = genai.Client()
    
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
    )
    return response.embeddings[0].values
