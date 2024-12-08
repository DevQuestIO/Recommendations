from embeddings import generate_embeddings
from vector_store import query_similar_questions


def suggest_questions(query_slug):
    """
    Query the vector database for questions similar to the given question slug.

    Args:
        query_slug (str): The slug of the question to base the suggestions on.

    Returns:
        list: A list of suggested questions.
    """
    # Generate an embedding for the question slug (assuming you use a pre-trained embedding model)
    query_embedding = generate_embeddings([query_slug])[0]

    # Query the vector database
    results = query_similar_questions(query_embedding)

    # Extract and return the suggestions
    suggestions = [
        {
            "title": metadata["title"],
            "difficulty": metadata["difficulty"],
            "tags": metadata["tags"],
        }
        for metadata_list in results["metadatas"]
        for metadata in metadata_list
    ]
    return suggestions
