# # pdf_embedder.py

# # import pdfplumber
# # import chromadb
# # from initialize.config import PDF_PATHS, VECTOR_DB_DIR
# # from chromadb.utils import embedding_functions

# # class TarotPDFEmbedder:
# #     def __init__(self, model_name="all-MiniLM-L6-v2", collection_name="tarot_cards"):
# #         self.chroma_client = chromadb.Client()
# #         self.embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)
# #         self.collection = self.chroma_client.get_or_create_collection(
# #             name=collection_name,
# #             embedding_function=self.embed_fn
# #         )

# #     def extract_paragraphs(self):
# #         paragraphs = []
# #         for path in PDF_PATHS:
# #             with pdfplumber.open(path) as pdf:
# #                 for page in pdf.pages:
# #                     text = page.extract_text()
# #                     if text:
# #                         chunks = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 40]
# #                         paragraphs.extend(chunks)
# #         return paragraphs

# #     def build_vector_store(self):
# #         paragraphs = self.extract_paragraphs()
# #         ids = [f"chunk_{i}" for i in range(len(paragraphs))]
# #         if self.collection.count() == 0:
# #             self.collection.add(documents=paragraphs, ids=ids)
# #             print(f"🔗 Indexed {len(paragraphs)} chunks from {len(PDF_PATHS)} PDFs.")
# #         else:
# #             print(f"ℹ️ Collection already contains {self.collection.count()} chunks.")

# #     def retrieve(self, query, top_k=3):
# #         result = self.collection.query(query_texts=[query], n_results=top_k)
# #         return result["documents"][0] if result["documents"] else []


# # pdf_embedder.py


# #Change occurs from here

# import pdfplumber
# import chromadb
# from initialize.config import PDF_PATHS, VECTOR_DB_DIR
# from chromadb.utils import embedding_functions
# from langdetect import detect
# from utils.context import ConversationContext  # <-- import your context

# class TarotPDFEmbedder:
#     def __init__(self, model_name="all-MiniLM-L6-v2", collection_name="tarot_cards"):
#         self.chroma_client = chromadb.Client()
#         self.embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)
#         self.collection = self.chroma_client.get_or_create_collection(
#             name=collection_name,
#             embedding_function=self.embed_fn
#         )

#     def extract_paragraphs(self):
#         paragraphs = []
#         for path in PDF_PATHS:
#             with pdfplumber.open(path) as pdf:
#                 for page in pdf.pages:
#                     text = page.extract_text()
#                     if text:
#                         chunks = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 40]
#                         paragraphs.extend(chunks)
#         return paragraphs

#     def build_vector_store(self):
#         paragraphs = self.extract_paragraphs()
#         ids = [f"chunk_{i}" for i in range(len(paragraphs))]
#         if self.collection.count() == 0:
#             self.collection.add(documents=paragraphs, ids=ids)
#             print(f"🔗 Indexed {len(paragraphs)} chunks from {len(PDF_PATHS)} PDFs.")
#         else:
#             print(f"ℹ️ Collection already contains {self.collection.count()} chunks.")

#     def retrieve(self,
#                  query: str,
#                  context: ConversationContext = None,
#                  top_k: int = 3) -> list[str]:
#         """
#         Run a Chroma query; then (if a context is given) filter to only those
#         chunks whose detected language matches context.language.
#         """
#         result = self.collection.query(query_texts=[query], n_results=top_k)
#         docs = result.get("documents", [[]])[0]

#         # If no context or context.language=='en', just return what Chroma gave us
#         if not context:
#             return docs

#         # Otherwise, detect each doc's lang and keep only matches
#         filtered = [d for d in docs if detect(d) == context.language]
#         return filtered[:top_k]

import pdfplumber
import numpy as np
from langdetect import detect
from initialize.config import PDF_PATHS
from utils.context import ConversationContext

# Simple text similarity function to replace sentence_transformers
def simple_similarity(text1, text2):
    """Simple text similarity using word overlap"""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return len(intersection) / len(union) if union else 0

class TarotPDFEmbedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        # Remove dependency on sentence_transformers
        self.paragraphs = []

    def extract_paragraphs(self):
        paragraphs = []
        for path in PDF_PATHS:
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        chunks = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 40]
                        paragraphs.extend(chunks)
        self.paragraphs = paragraphs
        return paragraphs

    def build_vector_store(self):
        print("🔄 Building simple text index...")
        self.extract_paragraphs()
        print(f"✅ Indexed {len(self.paragraphs)} chunks from {len(PDF_PATHS)} PDFs.")

    def retrieve(self,
                 query: str,
                 context: ConversationContext = None,
                 top_k: int = 3) -> list[str]:

        # Simple keyword-based retrieval
        query_words = set(query.lower().split())
        similarities = []
        
        for i, paragraph in enumerate(self.paragraphs):
            similarity = simple_similarity(query, paragraph)
            similarities.append((similarity, i))
        
        # Sort by similarity and get top_k
        similarities.sort(reverse=True)
        top_indices = [i for _, i in similarities[:top_k]]
        docs = [self.paragraphs[i] for i in top_indices]

        if not context:
            return docs

        filtered = [d for d in docs if detect(d) == context.language]
        return filtered[:top_k]

