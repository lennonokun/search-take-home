from __future__ import annotations

import asyncio
from pathlib import Path
from typing import AsyncIterator

import anyio
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse


router = APIRouter(prefix="/streaming", tags=["streaming"])


def _sse(event: str, data: str = "") -> str:
    output = f"event: {event}\n"
    safe_data = data.replace("\n", "\ndata: ")
    output += f"data: {safe_data}\n\n"

    return output


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
    file_path = Path(path)

    if not file_path.is_absolute():
        file_path = (Path.cwd() / file_path).resolve()

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}")

    async def event_generator() -> AsyncIterator[str]:
        yield _sse("meta", path)
        try:
            async with await anyio.open_file(
                file_path, mode="r", encoding="utf-8"
            ) as f:
                while chunk := await f.read(chunk_size):
                    yield _sse("chunk", chunk)

                    if delay_ms > 0:
                        await asyncio.sleep(delay_ms / 1000.0)

            yield _sse("done")
        except Exception as e:
            yield _sse("error", str(e))

    return StreamingResponse(event_generator(), media_type="text/event-stream")
