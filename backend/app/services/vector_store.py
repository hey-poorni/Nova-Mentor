import logging
import threading
import os
import json
from typing import TYPE_CHECKING, Any, Dict, List, Optional, cast

logger = logging.getLogger(__name__)
_lock = threading.Lock()

# ── TYPE_CHECKING: stubs for IDE/linter (path-with-spaces workaround) ────────
# In the linter's view (TYPE_CHECKING=True), we define minimal class stubs and
# assign concrete instances so Pyre2 treats np/faiss as fully bound names.
# At runtime the real packages are imported in the `else` branch.
if TYPE_CHECKING:
    class _NdArray:
        """Stub for numpy.ndarray."""
        pass

    class _NpModule:
        """Stub for the numpy module."""
        float32: Any

        def array(self, a: Any, dtype: Any = None) -> "_NdArray":  # type: ignore[empty-body]
            ...

    class _FaissIndex:
        """Stub for faiss.IndexFlatL2."""
        ntotal: int

        def add(self, vectors: "_NdArray") -> None:  # type: ignore[empty-body]
            ...

        def search(self, vectors: "_NdArray", k: int) -> "Any":  # type: ignore[empty-body]
            ...

    class _FaissModule:
        """Stub for the faiss module."""
        def IndexFlatL2(self, d: int) -> "_FaissIndex":  # type: ignore[empty-body]
            ...

        def read_index(self, path: str) -> "_FaissIndex":  # type: ignore[empty-body]
            ...

        def write_index(self, index: "_FaissIndex", path: str) -> None:  # type: ignore[empty-body]
            ...

    class SentenceTransformer:
        """Stub for sentence_transformers.SentenceTransformer."""
        def __init__(self, model_name_or_path: str) -> None:  # type: ignore[empty-body]
            ...

        def encode(self, sentences: "List[str]") -> "_NdArray":  # type: ignore[empty-body]
            ...

    # Assign instances so linter sees np/faiss as bound with known types
    np = _NpModule()
    faiss = _FaissModule()

else:
    # Real runtime imports — used by the actual Python interpreter
    import numpy as np
    import faiss
    from sentence_transformers import SentenceTransformer


# ── Embedding model config ────────────────────────────────────────────────────
MODEL_NAME = "all-MiniLM-L6-v2"

# ── Module-level state (typed) ────────────────────────────────────────────────
_model: Optional[SentenceTransformer] = None
_index: Any = None   # faiss.IndexFlatL2 at runtime; Any avoids Optional[Any] tension
_texts: List[str] = []
_dimension: int = 384
_storage_dir: str = os.path.join(os.getcwd(), "data")
_index_path: str = os.path.join(_storage_dir, "vector_store.faiss")
_texts_path: str = os.path.join(_storage_dir, "metadata.json")


def _get_model() -> SentenceTransformer:
    """Lazy-load the sentence transformer model (singleton)."""
    global _model
    if _model is None:
        logger.info("Loading sentence-transformer model: %s", MODEL_NAME)
        _model = SentenceTransformer(MODEL_NAME)
        logger.info("Model loaded successfully.")
    # assert narrows Optional[SentenceTransformer] → SentenceTransformer for Pyre2
    assert _model is not None
    return _model


def init_index() -> None:
    """Initialize or load the FAISS index from disk."""
    global _index, _texts

    if not os.path.exists(_storage_dir):
        os.makedirs(_storage_dir, exist_ok=True)

    if os.path.exists(_index_path) and os.path.exists(_texts_path):
        try:
            logger.info("Loading persistent vector store from %s...", _storage_dir)
            _index = faiss.read_index(_index_path)
            with open(_texts_path, "r", encoding="utf-8") as f:
                loaded: Any = json.load(f)
                _texts = [str(item) for item in loaded] if isinstance(loaded, list) else []
            return
        except Exception as e:
            logger.error("Failed to load vector store: %s. Starting fresh.", e)

    logger.info("Initializing new L2 FAISS index...")
    _index = faiss.IndexFlatL2(_dimension)
    _texts = []


def _save_store() -> None:
    """Commit index and metadata to persistent storage."""
    if _index is not None:
        try:
            faiss.write_index(_index, _index_path)
            with open(_texts_path, "w", encoding="utf-8") as f:
                json.dump(_texts, f)
            logger.debug("Vector store saved to disk.")
        except Exception as e:
            logger.error("Persistence error: %s", e)


def store_text(text: str) -> None:
    """
    Encode a text string and store its embedding in the FAISS index.

    Args:
        text: The text to store (e.g. a student interaction or concept).
    """
    global _index, _texts

    with _lock:
        if _index is None:
            init_index()

        # Narrow Optional[Any] → Any with an explicit guard
        index: Any = _index
        if index is None:
            logger.error("FAISS index could not be initialised.")
            return

        model: SentenceTransformer = _get_model()
        raw: Any = model.encode([text])
        embedding: Any = np.array(raw, dtype=np.float32)

        index.add(embedding)
        _texts.append(text)
        _save_store()

        total: int = int(index.ntotal)
        # enumerate+join avoids Pyre2's broken str.__getitem__(slice) overload
        preview_chars: List[str] = [c for i, c in enumerate(text) if i < 80]
        preview: str = "".join(preview_chars)
        logger.info("Stored text (total=%d): %s", total, preview)


def search_similar(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Search for the most similar stored texts to a query.

    Args:
        query: The search query string.
        top_k: Number of results to return (default 3).

    Returns:
        List of dicts: [{"text": str, "score": float}, ...]
        Score is L2 distance (lower = more similar).
    """
    with _lock:
        # cast() tells Pyre2 the exact type — avoids Optional[Any] → Any tension
        index: Any = cast(Any, _index)
        if index is None or int(index.ntotal) == 0:
            logger.warning("FAISS index is empty. Nothing to search.")
            return []

        model: SentenceTransformer = _get_model()
        raw: Any = model.encode([query])
        query_vec: Any = np.array(raw, dtype=np.float32)

        # Clamp top_k to the number of stored items
        k: int = cast(int, min(top_k, int(index.ntotal)))

        # search() returns (distances_array, indices_array) — kept as Any
        search_out: Any = cast(Any, index.search(query_vec, k))
        dist_arr: Any = cast(Any, search_out[0])
        idx_arr: Any = cast(Any, search_out[1])

        # Materialise to plain Python lists — cast() pins the element types
        distances: List[float] = [cast(float, float(cast(Any, dist_arr[0])[i])) for i in range(k)]
        indices: List[int]     = [cast(int,   int(cast(Any, idx_arr[0])[i]))    for i in range(k)]

        results: List[Dict[str, Any]] = []
        for i in range(k):
            idx: int   = cast(int,   indices[i])
            dist: float = cast(float, distances[i])
            if 0 <= idx < len(_texts):
                text_val: str = cast(str, str(_texts[idx]))
                score_val: float = cast(float, round(dist, 4))
                results.append({
                    "text": text_val,
                    "score": score_val,
                })

    # enumerate+join avoids Pyre2's broken str.__getitem__(slice) overload
    preview_chars2: List[str] = [c for i, c in enumerate(query) if i < 50]
    query_preview: str = "".join(preview_chars2)
    logger.info("Search for '%s' returned %d results.", query_preview, len(results))
    return results
