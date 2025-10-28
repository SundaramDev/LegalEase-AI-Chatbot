from rag_pipeline import answer_query, retrieve_docs, llm_model
import streamlit as st

# Step 1: Setup Upload PDF functionality
uploaded_files = st.file_uploader("Upload PDF",
                                  type="pdf",
                                  accept_multiple_files=True)

# Step 2: Chatbot Skeleton (Questions & Answers)
user_query = st.text_area("Enter your prompt:", height=150, placeholder="Ask Anything!")

ask_question = st.button("Ask AI Lawyer")

if ask_question:
    if uploaded_files:
        st.chat_message("user").write(user_query)

        # Retrieve relevant documents from FAISS
        retrieved_docs = retrieve_docs(user_query)

        # Get AI's response
        response = answer_query(documents=retrieved_docs, model=llm_model, query=user_query)

        st.chat_message("AI Lawyer").write(response)

    else:
        st.error("Kindly upload a valid PDF file first!")
