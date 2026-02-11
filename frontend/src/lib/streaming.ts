export type StreamHandlers = {
  onMeta?: (data: string) => void;
  onChunk?: (data: string) => void;
  onDone?: (data: string) => void;
  onError?: (ev: Event) => void;
};

export type NotepadStreamOptions = {
  /**
   * Backend file path. Default matches backend default.
   * Example: "backend/data/notepad.txt"
   */
  path?: string;
  chunkSize?: number;
  delayMs?: number;
};

/**
 * Stream a text file from the backend using Server-Sent Events.
 *
 * Backend endpoint: GET /api/streaming/notepad
 */
export function streamNotepad(
  handlers: StreamHandlers,
  options: NotepadStreamOptions = {},
): () => void {
  const params = new URLSearchParams();
  if (options.path) params.set("path", options.path);
  if (options.chunkSize != null)
    params.set("chunk_size", String(options.chunkSize));
  if (options.delayMs != null) params.set("delay_ms", String(options.delayMs));

  const url = `/api/streaming/notepad?${params.toString()}`;
  const es = new EventSource(url);

  es.addEventListener("meta", (e) =>
    handlers.onMeta?.((e as MessageEvent).data),
  );
  es.addEventListener("chunk", (e) =>
    handlers.onChunk?.((e as MessageEvent).data),
  );
  es.addEventListener("done", (e) => {
    handlers.onDone?.((e as MessageEvent).data);
    es.close();
  });

  es.onerror = (ev) => {
    handlers.onError?.(ev);
    // Keep the default EventSource reconnection behavior unless caller closes.
  };

  return () => es.close();
}
