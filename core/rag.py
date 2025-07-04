# from utils.pdf_reader import TarotPDFEmbedder
# from initialize.config import VECTOR_DB_DIR, MODEL_NAME

# _embedder = TarotPDFEmbedder(model_name="all-MiniLM-L6-v2")

# def get_card_meaning(card_name: str, k: int = 3) -> str:
#     results = _embedder.retrieve(card_name, top_k=k)
#     return "\n\n".join(results)
from utils.pdf_reader import TarotPDFEmbedder
from initialize.config import VECTOR_DB_DIR, MODEL_NAME

# Initialize the embedder
_embedder = TarotPDFEmbedder(model_name="all-MiniLM-L6-v2")

def get_card_meaning(card_name: str, k: int = 3) -> str:
    # Ensure the FAISS index is built before retrieving
    if _embedder.index is None:
        try:
            _embedder.build_vector_store()
        except Exception as e:
            return f"⚠️ Failed to build vector index: {str(e)}"

    try:
        results = _embedder.retrieve(card_name, top_k=k)
        if not results:
            return f"🤔 No relevant meanings found for {card_name}."
        return "\n\n".join(results)
    except Exception as e:
        return f"⚠️ Retrieval error for '{card_name}': {str(e)}"
