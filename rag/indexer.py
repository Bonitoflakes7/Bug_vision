import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from config import CHROMA_DB_PATH, EMBED_MODEL, OLLAMA_BASE_URL


def index_codebase(project_path: str) -> None:
    """
    Reads all .py files from project_path, chunks them,
    embeds them with nomic-embed-text, and stores in ChromaDB.
    Call this once before running the main loop, or whenever
    your codebase changes significantly.
    """
    print(f"[📂] Indexing project: {project_path}")

    # Step 1 — Load all .py files
    loader = DirectoryLoader(
        project_path,
        glob="**/*.py",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )
    documents = loader.load()
    print(f"[📄] Loaded {len(documents)} Python files")

    if not documents:
        print("[⚠] No .py files found. Check your project path.")
        return

    # Step 2 — Split into chunks
    # RecursiveCharacterTextSplitter tries to split on class/function
    # boundaries first, then falls back to paragraphs, then lines.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\nclass ", "\ndef ", "\n\n", "\n", " "],
    )
    chunks = splitter.split_documents(documents)
    print(f"[✂] Split into {len(chunks)} chunks")

    # Step 3 — Embed and store in ChromaDB
    print(f"[🧠] Embedding with {EMBED_MODEL}... (this may take a minute)")
    embeddings = OllamaEmbeddings(
        model=EMBED_MODEL,
        base_url=OLLAMA_BASE_URL,
    )

    # Chroma.from_documents embeds every chunk and saves to disk
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH,
    )

    print(f"[✅] Indexed {len(chunks)} chunks → saved to {CHROMA_DB_PATH}")