# DevQuest.IO - Recommendation Service

## Overview
The Recommendation Service is a component of the DevQuest.IO platform, responsible for generating personalized coding question suggestions for users. It leverages AI-driven insights, user progress data, and advanced data retrieval techniques to provide tailored recommendations.

---

## Key Features
- **Personalized Recommendations**:
  - Suggests coding questions based on user progress and goals.
  - Prioritizes problems tagged similarly to previously solved questions.
- **Data Integration**:
  - Fetches and normalizes user progress data from external APIs.
  - Stores data in MongoDB for efficient querying and analysis.
- **AI-Powered Insights**:
  - Utilizes Retrieval-Augmented Generation (RAG) architecture with OpenAI APIs.
  - Combines embeddings from ChromaDB for context-aware suggestions.

---

## Tech Stack
- **Programming Language**: Python
- **Framework**: FastAPI
- **Database**: MongoDB
- **Embedding Storage**: ChromaDB

---

## Installation

### Prerequisites
- Python 3.8+
- MongoDB instance (local or cloud)
- ChromaDB setup

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd recommendation-service
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   - Set up the following variables in a `.env` file:
     ```env
     MONGO_URI=<your_mongodb_connection_string>
     OPENAI_API_KEY=<your_openai_api_key>
     CHROMADB_URI=<your_chromadb_connection_string>
     ```

---

## Usage
1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
2. API Endpoints:
   - **GET `/recommendations`**: Fetch personalized recommendations for a user.
     - Query Parameters:
       - `user_id` (string): Unique identifier for the user.
   - **POST `/sync-progress`**: Sync progress data from external APIs.
     - Body:
       ```json
       {
         "user_id": "<user_id>",
         "platform_data": {
           "leetcode": { ... },
           "geeksforgeeks": { ... }
         }
       }
       ```

---

## Architecture
1. **Fetching Data**:
   - Connects to external APIs to gather user progress data.
   - Normalizes and stores data in MongoDB.
2. **Recommendation Generation**:
   - Retrieves user embeddings from ChromaDB.
   - Queries OpenAI's API to enhance recommendations.
   - Suggests questions based on user goals and historical performance.

