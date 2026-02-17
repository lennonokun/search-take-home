from typing import List

import faiss
from langchain.chat_models import init_chat_model
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.documents import Document
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import OpenAIEmbeddings

from .models import SearchResult, CypherQuery

# TODO makes some assumptions about relationships
CYPHER_SYSTEM_PROMPT = """
You are a specialized medical knowledge graph assistant. Your task is to translate natural language user queries into a structured CypherQuery object based on a specific medical ontology.

### 1. Medical Ontology
- **Entities (Tags):** disease, symptom, drug, patient
- **Relationships:**
  - TREATS (drug -> disease/symptom)
  - CAUSES (disease/drug -> symptom)
  - EXPERIENCING (patient -> symptom)
  - SUFFERING_FROM (patient -> disease)

### 2. Translation Rules
- **Map Names to Tags:** Do not use specific entity names (e.g., "Covid", "John", "Advil") in the tags. Instead, map them to their corresponding entity type:
  - Specific diseases -> "disease"
  - Specific drugs -> "drug"
  - People or "someone" -> "patient"
  - Specific ailments -> "symptom"
- **Identify Query Type:**
  - **node:** Use when the user asks about a single entity (e.g., "Tell me about malaria").
  - **relationship:** Use when the user asks about connections (e.g., "What treats malaria?" or "What symptoms does this cause?").

### 3. Structural Requirements
- For **node** queries: Provide only the `node_tag`.
- For **relationship** queries: Provide `start_tag`, `relationship_tag`, `end_tag`, and specify the `return_node` ("start" or "end") based on what the user is looking for.
  - *Example:* "What drugs treat malaria?" -> start: drug, rel: TREATS, end: disease, return: start.

Always output a valid CypherQuery object adhering to these allowed literals. If no useful information can be inferred, give a blank **node** query.
"""


async def text_to_cypher(text: str) -> str:
    """Convert a text query to a Cypher query.

    You should use an LangChain LLM using 'with_structured_output' to generate the Cypher query.
    Reference the docs here: https://docs.langchain.com/oss/python/langchain/structured-output#:~:text=LangChain%20automatically%20uses%20ProviderStrategy%20when%20you%20pass%20a%20schema%20type%20directly%20to%20create_agent.response_format%20and%20the%20model%20supports%20native%20structured%20output%3A

    Assume the knowledge graph has the following ontology:
    - Entities:
     - Disease
     - Symptom
     - Drug
     - Patient
    - Relationships:
     - TREATS
     - CAUSES
     - EXPERIENCING
     - SUFFERING_FROM

    You should have the model construct a Cypher query via a structured output (using JSON schema or
    Pydantic BaseModels) that can be used to query the system. If you have an API key, you may use it -
    otherwise, simply construct the LLM & assume that the the API key will be populated later.
    """

    # create model once
    if hasattr(text_to_cypher, "_model"):
        model = text_to_cypher._model
    else:
        model = init_chat_model("gpt-4o-mini")
        model = model.with_structured_output(CypherQuery, method="function_calling")
        text_to_cypher._model = model

    messages = [
        SystemMessage(content=CYPHER_SYSTEM_PROMPT),
        HumanMessage(content=text),
    ]
    try:
        cypher: CypherQuery = await model.ainvoke(messages)  # pyright: ignore
    except ValueError:
        cypher = CypherQuery(query_type="node")

    return str(cypher)


def load_FAISS(documents: list[Document]) -> FAISS:
    """Create and return a FAISS vector store from the DOCUMENTS list."""
    # create FAISS once
    if hasattr(load_FAISS, "_store"):
        return load_FAISS._store

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    example_query = embeddings.embed_query("testing")
    vector_store = FAISS(
        embedding_function=embeddings,
        index=faiss.IndexFlatIP(len(example_query)),
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    ids = [doc.metadata["id"] for doc in documents]
    vector_store.add_documents(documents=documents, ids=ids)

    load_FAISS._store = vector_store
    return vector_store


def search_knowledgegraph(cypher_query: str) -> list[SearchResult]:
    """This is a mock function that will search the knowledge graph using a cypher query."""
    return [
        SearchResult(
            document=Document(
                id=5,
                page_content=cypher_query,
                metadata={"title": "The Crazy Document", "id": 5},
            ),
            score=0.9,
            reason="cypher query",
        )
    ]


def rerank_results(
    vector_results: List[SearchResult], graph_results: List[SearchResult], top_k: int
):
    vector_organized = {r.document.metadata["id"]: r for r in vector_results}
    graph_organized = {r.document.metadata["id"]: r for r in graph_results}
    all_ids = set(vector_organized.keys()) | set(graph_organized.keys())

    # simply rerank by average
    # TODO a weighing would definitely be better
    reranked_results = []
    for id in all_ids:
        r_vector = vector_organized.get(id)
        r_graph = graph_organized.get(id)
        rs_valid = [r for r in [r_vector, r_graph] if r is not None]
        better_result = max(rs_valid, key=lambda r: r.score)
        reranked_results.append(
            SearchResult(
                document=rs_valid[0].document,
                score=sum(r.score for r in rs_valid) / 2,
                reason=better_result.reason,
            )
        )

    reranked_results.sort(key=lambda r: r.score, reverse=True)
    return reranked_results[:top_k]


async def search_documents(
    documents: list[Document],
    query: str,
    top_k: int,
) -> list[SearchResult]:
    """Using the FAISS vector store, search for the query and return a list of SearchResults.

    After searching FAISS, you should rerank all the remaining results using your custom 'rerank_result'
    function, and removing bad results. You may add args/kwargs as needed.
    """
    vector_store = load_FAISS(documents)
    cypher_query = await text_to_cypher(query)

    # no top_k for similarity search, instead only for reranked
    # TODO for a larger number of documents consider using some multiple of top_k
    similarities = vector_store.similarity_search_with_score(query)
    vector_results = [
        SearchResult(document=document, score=score, reason="vector similarity")
        for (document, score) in similarities
    ]

    graph_results = search_knowledgegraph(cypher_query)

    return rerank_results(vector_results, graph_results, top_k)
