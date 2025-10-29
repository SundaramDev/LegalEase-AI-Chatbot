import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from vector_database import faiss_db

# Step 1: Load environment variables (contains OPENAI_API_KEY)
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found. Please add it to Streamlit Secrets or your .env file.")
else:
    print("🔐 Loaded OpenAI API Key:", api_key[:8], "********")

# Step 2: Setup LLM (OpenAI GPT model)
llm_model = ChatOpenAI(
    model="gpt-4o-mini",   # Alternatives: "gpt-4-turbo" or "gpt-3.5-turbo"
    temperature=0.3
)

# Step 3: Retrieve Docs from FAISS
def retrieve_docs(query):
    return faiss_db.similarity_search(query)

def get_context(documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    return context

# Step 4: Custom Prompt Template
custom_prompt_template = """
Use only the provided context to answer the question.
If the context does not contain the answer, simply say you don’t know.
Avoid guessing or adding information not supported by the context.

Question: {question}
Context: {context}
Answer:
"""

# Step 5: Answer Query Function
def answer_query(documents, model, query):
    context = get_context(documents)
    prompt = ChatPromptTemplate.from_template(custom_prompt_template)
    chain = prompt | model
    response = chain.invoke({"question": query, "context": context})
    return response.content if hasattr(response, "content") else response

# Step 6: Example Query (for local testing)
if __name__ == "__main__":
    question = "Which articles mention the right to freedom of speech?"
    retrieved_docs = retrieve_docs(question)

    if not retrieved_docs:
        print("⚠️ No relevant documents found in FAISS database.")
    else:
        answer = answer_query(documents=retrieved_docs, model=llm_model, query=question)
        print("AI Lawyer:", answer)
