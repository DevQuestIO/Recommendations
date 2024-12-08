from fastapi import FastAPI, HTTPException
from typing import List, Dict
from leetcode_api import (
    fetch_solved_questions,
    fetch_last_solved_questions,
    suggest_similar_questions,
)
from embeddings import generate_embeddings
from vector_store import store_embeddings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Suggestions Service",
    description="API for generating coding question suggestions",
    version="1.0.0",
)

origins = [
    "http://localhost:3000",  # React development server
    "http://localhost:3001",
    "http://localhost:8000",  # FastAPI server
    "http://localhost:5000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5000",
    # Add your production domains here
    "https://devquest.io",
    "https://api.devquest.io",
    "https://www.devquest.io",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers,
    expose_headers=["*"],
)


@app.get("/api/v1/suggestions", response_model=List[Dict[str, str]])
async def fetch_suggestions():
    try:
        solved_questions = fetch_solved_questions()
        print("Stage 1 cleared")
        question_titles = [q["title"] for q in solved_questions]
        print("Stage 2 cleared")
        embeddings = generate_embeddings(question_titles)
        print("Stage 3 cleared")
        store_embeddings(solved_questions, embeddings)
        print("Stage 4 cleared")
        last_solved_data = fetch_last_solved_questions("kalpessh_patil", 1)
        print("Stage 5 cleared")
        suggested_questions = suggest_similar_questions(last_solved_data)
        print(suggested_questions)
        return [
            {"title": q["title"], "difficulty": q["difficulty"]}
            for q in suggested_questions
        ]

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch suggestions")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
