from __future__ import annotations

import asyncio
from pathlib import Path
from typing import AsyncIterator

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse


router = APIRouter(prefix="/streaming", tags=["streaming"])


def _sse(data: str, event: str | None = None) -> str:
    """Format a Server-Sent Event (SSE) message.

    Candidates: you may keep this helper or replace it.
    """

    lines: list[str] = []
    if event:
        lines.append(f"event: {event}")

    for line in data.splitlines() or [""]:
        lines.append(f"data: {line}")

    return "\n".join(lines) + "\n\n"


@router.get("/notepad")
async def stream_notepad(
    path: str = Query(
        default=str(Path("data/notepad.txt")),
        description="Path to the .txt file to stream. Relative paths are resolved from the backend working directory.",
    ),
    chunk_size: int = Query(default=256, ge=1, le=8192),
    delay_ms: int = Query(default=25, ge=0, le=5000),
) -> StreamingResponse:
    """Stream a .txt file to the frontend as Server-Sent Events (SSE).

    Take-home objective:
    - Implement SSE streaming from the provided `.txt` file.
    - Stream incremental chunks so the UI can render as data arrives.
    - Handle missing files and invalid params cleanly.

    Notes:
    - The function currently returns a stub response (non-streaming) so candidates
      can implement the actual streaming logic.
    """

    # Keep imports referenced for candidates. These are unused until implemented.
    _ = (asyncio, AsyncIterator, chunk_size, delay_ms)

    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = (Path.cwd() / file_path).resolve()

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}")

    async def event_generator() -> AsyncIterator[bytes]:
        # TODO (candidate): yield SSE events that stream `file_path` progressively.
        yield _sse(
            "TODO: implement SSE streaming in backend/features/streaming/router.py",
            event="todo",
        ).encode("utf-8")

    return StreamingResponse(event_generator(), media_type="text/event-stream")
