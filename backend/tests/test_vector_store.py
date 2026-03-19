# Test: vector_store.py
# Run: python backend/tests/test_vector_store.py

import sys
import os
from typing import TYPE_CHECKING, List, Dict, Any

# ─── Fix Path Resolution (Ensures app modules can be found despite space in path) ───
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ─── TYPE_CHECKING Guard ──────────────────────────────────────────────────
if TYPE_CHECKING:
    def init_index() -> None: ...
    def store_text(text: str) -> None: ...
    def search_similar(query: str, top_k: int = 3) -> List[Dict[str, Any]]: ...
else:
    from app.services.vector_store import init_index, store_text, search_similar

def test_vector_store() -> None:
    print("\n[1] Initializing FAISS index...")
    init_index()

    print("\n[2] Storing texts...")
    texts = [
        "sorting algorithm basics",
        "binary search implementation",
        "linked list operations",
        "bubble sort vs quick sort",
        "array traversal techniques",
    ]
    for t in texts:
        store_text(t)
        print(f"    Stored: {t}")

    print("\n[3] Searching for: 'sorting'")
    results = search_similar("sorting", top_k=3)
    for r in results:
        print(f"    - {r['text']}  (score: {r['score']})")

    print("\n[4] Searching for: 'search algorithm'")
    results = search_similar("search algorithm", top_k=3)
    for r in results:
        print(f"    - {r['text']}  (score: {r['score']})")

    print("\n[PASS] Vector store test completed successfully!")

if __name__ == "__main__":
    test_vector_store()
