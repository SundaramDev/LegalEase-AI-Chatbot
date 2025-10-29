# check_faiss.py
from vector_database import faiss_db

try:
    print("FAISS object:", faiss_db)
    # `index` attribute exists on many FAISS wrappers; try reading doc count
    try:
        count = faiss_db.index.ntotal
        print("Number of vectors in FAISS index:", count)
    except Exception:
        # fallback: try stored pickle/index file presence
        print("Could not read ntotal. FAISS object type:", type(faiss_db))
except Exception as e:
    print("Error accessing faiss_db:", e)
