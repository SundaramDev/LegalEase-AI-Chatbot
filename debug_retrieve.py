# debug_retrieve.py
from rag_pipeline import retrieve_docs

query = "Which article protects the right to be informed of the reason for arrest?"
docs = retrieve_docs(query)

print(f"\n🔍 Retrieved {len(docs)} documents\n")
for i, d in enumerate(docs, 1):
    print(f"--- Document {i} ---")
    print(d.page_content[:500].replace("\n", " "))
    print("\n--------------------\n")
