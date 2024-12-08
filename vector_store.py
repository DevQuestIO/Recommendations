from chromadb import PersistentClient
from chromadb.config import Settings


# # Initialize the Chroma client with the appropriate settings
# client = chromadb.Client(
#     Settings(
#         chroma_db_impl="duckdb+parquet",
#         persist_directory="./chroma",  # Directory for persistent storage
#     )
# )

client = PersistentClient(
    path="./chroma_data",  # Persistent storage path
    settings=Settings(anonymized_telemetry=False),
)

collection = client.get_or_create_collection("leetcode_questions")


def store_embeddings(questions, embeddings):
    for question, embedding in zip(questions, embeddings):
        tags = ", ".join(tag["name"] for tag in question["topicTags"])
        collection.add(
            ids=[question["titleSlug"]],
            embeddings=[embedding],
            metadatas=[
                {
                    "title": question["title"],
                    "difficulty": question["difficulty"],
                    "tags": tags,
                }
            ],
        )


def query_similar_questions(query_embedding, n_results=5):
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
    return results
