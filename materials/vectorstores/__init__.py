"""Vector store integrations for material chunks."""

from .chroma_store import ChromaVectorStore, ChromaUnavailableError

__all__ = ["ChromaVectorStore", "ChromaUnavailableError"]
