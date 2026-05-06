from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from config import CHROMA_DB_PATH, EMBED_MODEL, OLLAMA_BASE_URL, TOP_K_RESULTS
import os


def load_vectorstore() -> Chroma:
    """
    Load the existing ChromaDB index from disk.
    Call this once at startup after indexing.
    """
    if not os.path.exists(CHROMA_DB_PATH):
        raise FileNotFoundError(
            f"No ChromaDB index found at {CHROMA_DB_PATH}.\n"
            f"Run indexer.index_codebase(your_project_path) first."
        )

    embeddings = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url=OLLAMA_BASE_URL,
    )

    return Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings,
    )


def retrieve_context(vectorstore: Chroma, error_text: str) -> str:
    """
    Given an error string, find the TOP_K_RESULTS most relevant
    code chunks from the indexed codebase.
    Returns them as a single formatted string ready to inject into a prompt.
    """
    results = vectorstore.similarity_search(error_text, k=TOP_K_RESULTS)

    if not results:
        return ""

    parts = []
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get("source", "unknown file")
        # Make the path shorter for readability in the prompt
        source = os.path.basename(source)
        parts.append(f"# [{i}] from {source}\n{doc.page_content}")

    return "\n\n".join(parts)