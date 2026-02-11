from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from features.search.router import router as search_router
from features.streaming.router import router as streaming_router

app = FastAPI(title="Search Take-Home")
app.include_router(search_router, prefix="/api")
app.include_router(streaming_router, prefix="/api")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app", host="0.0.0.0", port=8000, reload=True, reload_excludes=".venv"
    )
