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
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langdetect import detect
from initialize.config import PDF_PATHS
from utils.context import ConversationContext

class TarotPDFEmbedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
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
        print("🔄 Building FAISS index...")
        self.extract_paragraphs()
        embeddings = self.model.encode(self.paragraphs, show_progress_bar=True)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        print(f"✅ Indexed {len(self.paragraphs)} chunks from {len(PDF_PATHS)} PDFs.")

    def retrieve(self,
                 query: str,
                 context: ConversationContext = None,
                 top_k: int = 3) -> list[str]:

        query_embedding = self.model.encode([query]).astype('float32')
        D, I = self.index.search(query_embedding, top_k)
        docs = [self.paragraphs[i] for i in I[0]]

        if not context:
            return docs

        filtered = [d for d in docs if detect(d) == context.language]
        return filtered[:top_k]

