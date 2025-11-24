from functools import lru_cache

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from .models import SearchResult, CypherQuery


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
    # TODO - Convert text to Cypher query
    return ""


@lru_cache()
def load_FAISS(documents: list[Document]) -> FAISS:
    """Create and return a FAISS vector store from the DOCUMENTS list."""
    # TODO
    return


def search_knowledgegraph(cypher_query: str) -> list[SearchResult]:
    """This is a mock function that will search the knowledge graph using a cypher query."""
    return [
        SearchResult(
            document=Document(page_content=cypher_query), score=0.9, reason="test"
        )
    ]


def search_documents(query: str, documents: list[Document]) -> list[SearchResult]:
    """Using the FAISS vector store, search for the query and return a list of SearchResults.

    After searching FAISS, you should rerank all the remaining results using your custom 'rerank_result'
    function, and removing bad results. You may add args/kwargs as needed.
    """
    # - TODO
    # 1) load the FAISS store
    # 2) convert the query to Cypher
    # 3) Search for the query on the FAISS store
    # 4) Search for the cypher query on the knowledgebase
    # 5) Return all the results
    return []
