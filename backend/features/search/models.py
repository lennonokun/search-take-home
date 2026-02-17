from datetime import datetime
from typing import Literal, Optional
from typing_extensions import Self

from langchain_core.documents import Document
from pydantic import BaseModel, Field, model_validator


class SearchResult(BaseModel):
    document: Document
    score: float = Field(..., ge=0)
    reason: str | None = None


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(5, ge=1, le=50)


class SearchEntry(BaseModel):
    query: str = Field(..., min_length=1)
    timestamp: datetime


CypherEntity = Literal["disease", "symptom", "drug", "patient"]
CypherRelationship = Literal["TREATS", "CAUSES", "EXPERIENCING", "SUFFERING_FROM"]


class CypherQuery(BaseModel, extra="ignore"):
    """Flattened union of single node queries and full node-relationship-node queries."""

    query_type: Literal["node", "relationship"] = Field(
        description="The type of query to perform: either a single node lookup or a relationship search."
    )

    # node query fields
    node_tag: Optional[CypherEntity] = Field(
        default=None, description="The entity tag to filter by if query_type is 'node'."
    )

    # relationship query fields
    start_tag: Optional[CypherEntity] = Field(
        default=None, description="The starting entity tag for a relationship query."
    )
    relationship_tag: Optional[CypherRelationship] = Field(
        default=None, description="The type of relationship."
    )
    end_tag: Optional[CypherEntity] = Field(
        default=None, description="The ending entity tag for a relationship query."
    )
    return_node: Optional[Literal["start", "end"]] = Field(
        default=None,
        description="Which node in the relationship to return (start or end).",
    )

    @model_validator(mode="after")
    def check(self) -> Self:
        if self.query_type == "relationship" and self.return_node is None:
            raise ValueError("relationship queries must specify a return_node")
        return self

    def __str__(self) -> str:
        if self.query_type == "node":
            return f"MATCH (node:{self.node_tag or ''}) RETURN node"
        start_query = f"(start:{self.start_tag or ''})"
        rel_query = f"-[:{self.relationship_tag or ''}]->"
        end_query = f"(end:{self.end_tag or ''})"
        return f"MATCH {start_query}{rel_query}{end_query} RETURN {self.return_node}"
