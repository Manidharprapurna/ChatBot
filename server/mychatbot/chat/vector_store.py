from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
from .models import FAQ

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "faiss_index.bin")
MODEL_NAME = "all-MiniLM-L6-v2"

_model = None
_index = None


def get_model():
    global _model
    if _model is None:
        print("[Vector DB] Loading model...")
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def get_index():
    global _index

    if _index is None:
        if os.path.exists(INDEX_PATH):
            _index = faiss.read_index(INDEX_PATH)
        else:
            create_vector_db()

    return _index


def create_vector_db():
    global _index

    model = get_model()
    faqs = FAQ.objects.filter(is_active=True)

    if not faqs.exists():
        print("[Vector DB] No FAQs found.")
        return

    faq_list = list(faqs)

    texts = [f"{faq.question} {faq.answer}" for faq in faq_list]

    embeddings = model.encode(texts, normalize_embeddings=True)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index = faiss.IndexIDMap(index)

    ids = np.array([faq.id for faq in faq_list]).astype("int64")

    index.add_with_ids(np.array(embeddings), ids)

    faiss.write_index(index, INDEX_PATH)

    _index = index

    print(f"[Vector DB] Created with {len(faq_list)} FAQs.")


# UPDATED SEARCH WITH DEPARTMENT FILTER
def search_vector(query, k=3, department=None):
    index = get_index()
    if index is None:
        return []

    model = get_model()

    query_vector = model.encode([query], normalize_embeddings=True)

    distances, ids = index.search(query_vector, k)

    result_ids = [int(i) for i in ids[0] if i != -1]

    faqs = FAQ.objects.filter(id__in=result_ids, is_active=True)

    # FILTER BY DEPARTMENT
    if department:
        faqs = faqs.filter(department__name=department)

    faq_map = {faq.id: faq for faq in faqs}

    results = []

    for i, rid in enumerate(result_ids):
        if rid in faq_map:
            score = float(distances[0][i])
            results.append((faq_map[rid], score))

    return results