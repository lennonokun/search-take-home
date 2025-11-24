# Search Take-Home Assignment

This repo contains a small FastAPI backend and a TypeScript frontend. Your task is to implement a simple search endpoint on the backend and a small, type-safe search client plus search-history utility on the frontend that the existing UI uses.

## What You Need to Build

### 1. Backend: `/api/search`

In `backend/features/search/search_router.py`, you'll find a POST endpoint stub for `/api/search`.

Your job:

- Implement ranking logic over a small in-memory corpus `DOCUMENTS`
- Create and utilize FAISS vector database in `search/integrations.py`
- Implement a `CypherQuery` pydantic BaseModel class in `search/models.py`, with it's own `__str__` function that returns itself as a Cypher Query
- Implement a prototype `text_to_cypher` function, which utilizes langchain LLMs, the `CypherQuery` and `with_structured_output` to create a query from natural language
- Search the FAISS index using the natural language query AND the CypherQuery
- Search the knowledgegraph using the mock function (0.0-1.0 range)
- Return the top `k` results as `SearchResult` objects.
- Keep the code clean, readable and maintainable.

### 2. TypeScript: API client & search history

Most of the frontend is already wired up with a simple React UI. Your primary tasks are in the TypeScript modules under `frontend/src/lib`.

Your job:

- In `frontend/src/lib/api.ts`, implement a type-safe `search(query: string, topK?: number)` function that:
  - Calls the `/api/search` endpoint via `fetch` with a JSON body.
  - Returns a `Promise<SearchResult[]>` parsed from the JSON response.
  - Throws a descriptive error when the response is not OK (e.g., non-2xx status).
- In `frontend/src/lib/searchHistory.ts`, implement pure, immutable helpers to manage recent search queries:
  - Represent each entry as a typed object (e.g., `SearchQuery`) containing the query string and timestamp.
  - Implement an `addToHistory` function that adds a new query, trims history to a maximum size, and avoids duplicate adjacent queries.
  - Implement a `getRecentQueries` function that returns a list of recent query strings in most-recent-first order.
- The React file `frontend/src/features/search/SearchPage.tsx` is already set up to use these helpers to display results and recent searches.
  - You generally do **not** need to modify React components to complete the assignment.
  - Minor adjustments to the UI are fine if they help you structure the TypeScript code cleanly.

Styling is intentionally minimal; focus on clear, well-typed TypeScript logic rather than CSS or advanced React patterns.

## Repository Structure

```text
backend/
  main.py                              # FastAPI app setup + router registration
  requirements.txt
  data/
    documents.json                     # Small corpus of documents for search
  features/search/
    data.py                            # Loads DOCUMENTS into memory
    models.py                          # Pydantic models (Document, SearchRequest, SearchResult)
    search_router.py                   # Your backend task lives
    integrations.py                    # Your backend scoring task here
frontend/
  src/lib/api.ts                       # TypeScript client for /api/search (your task)
  src/lib/searchHistory.ts             # Pure TypeScript helpers for search history (your task)
  src/features/search/SearchPage.tsx   # React UI that consumes the TS helpers
```

You should only need to modify:

- `backend/features/search/search_router.py`
- `backend/features/search/integrations.py`
- `backend/features/search/models.py`
- `frontend/src/lib/api.ts`
- `frontend/src/lib/searchHistory.ts`
- (Optional) `frontend/src/features/search/SearchPage.tsx`

## Running the App

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate # or .venv\Scripts\activate on windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Backend runs on `http://localhost:8000`
Frontend runs on `http://localhost:5173`

## What We're Evaluating

- API correctness
- Python clarity and maintainability
- Appropriate use of models and response structure
- TypeScript clarity, typing, and maintainability
- Correct handling of async flows and errors in TypeScript
- Clean, simple usage of React (no advanced patterns required)
- Correct data flow (request, loading, error, results, recent searches)

## Submission Instructions

To submit your work:

1. **Fork this repository on GitHub.**
2. **Clone your fork locally and complete the assignment there.**
3. **Commit and push** your changes to your fork's `master` branch.
4. **Open a Pull Request** from your fork's `master` branch into this repository's `master` branch.
5. Title the PR: `Take-Home submission — <Your Name>`
