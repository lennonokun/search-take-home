export type SearchDocumentMetadata = {
  id: number;
  title: string;
  // Allow additional metadata fields without losing type safety.
  [key: string]: unknown;
};

export type SearchDocument = {
  page_content: string;
  metadata: SearchDocumentMetadata;
};

export type SearchResult = {
  document: SearchDocument;
  score: number;
  reason?: string;
};

export class SearchError extends Error {
  status?: number;

  constructor(message: string, status?: number) {
    super(message);
    this.name = "SearchError";
    this.status = status;
  }
}

/**
 * Perform a search request against the backend.
 *
 * TODO (candidate):
 * - Call the `/api/search` endpoint via `fetch`.
 * - Send `{ query, top_k: topK }` as a JSON body.
 * - On non-OK responses, throw a `SearchError` with a helpful message and
 *   the HTTP status code.
 * - Parse and return the JSON response typed as `SearchResult[]`.
 */
export async function search(query: string, topK = 5): Promise<SearchResult[]> {
  // Stub implementation so the app compiles; replace this with a real call.
  try {
    const response = await fetch("/api/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      }, body: JSON.stringify({
        query: query,
        top_k: topK
      })
    });

    if (!response.ok)
      throw new SearchError(`HTTP Error: ${response.status}`)

    return await response.json();
  } catch (error) {
    throw new SearchError(`Error: ${error.message}`);
  }



  throw new SearchError("search() not implemented yet");
}
