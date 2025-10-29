from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from vector_database import faiss_db
from dotenv import load_dotenv

# Step 1: Load environment variables (contains GROQ_API_KEY)
load_dotenv()

# Step 2: Setup LLM (DeepSeek R1 via Groq)
llm_model = ChatGroq(model="llama-3.3-70b-versatile")

# Step 3: Retrieve Docs from FAISS
def retrieve_docs(query):
    return faiss_db.similarity_search(query)

def get_context(documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    return context

# Step 4: Custom Prompt Template
custom_prompt_template = """
Use the pieces of information provided in the context to answer the user's question.
If you don't know the answer, just say that you don't know — don't try to make up an answer.
Don't provide anything outside the given context.

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

# Step 6: Example Query
if __name__ == "__main__":
    question = "If a government forbids the right to assemble peacefully, which articles are violated and why?"
    retrieved_docs = retrieve_docs(question)

    if not retrieved_docs:
        print("⚠️ No relevant documents found in FAISS database.")
    else:
        answer = answer_query(documents=retrieved_docs, model=llm_model, query=question)
        print("AI Lawyer:", answer)