export type SearchQuery = {
  /** Raw query string entered by the user. */
  query: string;
  /** Unix timestamp in milliseconds when the query was executed. */
  timestamp: number;
};

export type SearchHistory = SearchQuery[];

export type AddToHistoryOptions = {
  /**
   * Maximum number of entries to keep.
   * Defaults to 10 if not provided.
   */
  maxEntries?: number;
};

/**
 * Add a new query to the existing history and return a new history array.
 *
 * TODO (candidate):
 * - Ignore queries that are empty or only whitespace.
 * - Add the new query as the most recent entry with the current timestamp.
 * - Avoid duplicate *adjacent* queries (if the last query has the same text,
 *   update its timestamp instead of adding a new entry).
 * - Trim the history so it never exceeds `maxEntries` (default 10).
 * - Do not mutate the `history` array; always return a new one.
 */
export function addToHistory(
  history: SearchHistory,
  query: string,
  options: AddToHistoryOptions = {},
): SearchHistory {
  const { maxEntries = 10 } = options;

  if (!query.trim())
    return history;

  const last = history[history.length - 1];
  const entry: SearchQuery = { query, timestamp: Date.now() };

  let next: SearchHistory;
  if (last?.query.trim() === query.trim()) {
    next = [...history.slice(0, -1), entry];
  } else {
    next = [...history, entry];
  }

  return next.slice(-maxEntries);
}

/**
 * Return a list of recent query strings in most-recent-first order.
 *
 * TODO (candidate):
 * - Use the provided `history` array (do not mutate it).
 * - Return only the `query` strings, ordered from newest to oldest.
 * - Optionally deduplicate consecutive identical strings if your
 *   `addToHistory` implementation does not already enforce this.
 */
export function getRecentQueries(history: SearchHistory): string[] {
  return [...history].reverse().map((h) => h.query);
}

