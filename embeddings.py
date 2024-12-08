import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def generate_embeddings(texts):
    response = openai.Embedding.create(input=texts, model="text-embedding-ada-002")
    return [embedding["embedding"] for embedding in response["data"]]
