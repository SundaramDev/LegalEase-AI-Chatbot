from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
import os

# Step 1: PDF folder setup
pdfs_directory = 'pdfs/'
os.makedirs(pdfs_directory, exist_ok=True)

def upload_pdf(file):
    with open(os.path.join(pdfs_directory, file.name), "wb") as f:
        f.write(file.getbuffer())

def load_pdf(file_path):
    print(f"📘 Loading: {os.path.basename(file_path)}")
    loader = PDFPlumberLoader(file_path)
    documents = loader.load()
    print(f"✅ Loaded {len(documents)} document pages from {pdfs_directory}")
    return documents

file_path = 'pdfs/universal_declaration_of_human_rights.pdf'
documents = load_pdf(file_path)

# Step 2: Create text chunks
def create_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    text_chunks = text_splitter.split_documents(documents)
    print(f"✅ Created {len(text_chunks)} text chunks.")
    return text_chunks

text_chunks = create_chunks(documents)

# Step 3: Use stronger embeddings model (nomic-embed-text)
ollama_model_name = "nomic-embed-text"

def get_embedding_model(ollama_model_name):
    embeddings = OllamaEmbeddings(model=ollama_model_name)
    return embeddings

# Step 4: Create and save FAISS vector database
FAISS_DB_PATH = "vectorstore/db_faiss"
faiss_db = FAISS.from_documents(text_chunks, get_embedding_model(ollama_model_name))
faiss_db.save_local(FAISS_DB_PATH)
print(f"✅ FAISS vector database saved successfully at: {FAISS_DB_PATH}")
