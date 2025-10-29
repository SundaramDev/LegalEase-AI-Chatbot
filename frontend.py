import streamlit as st
from rag_pipeline import answer_query, retrieve_docs, llm_model
import time

# --------------------------
# App Configuration
# --------------------------
st.set_page_config(
    page_title="LegalEase | AI Legal Assistant",
    page_icon="⚖️",  # Favicon (judgment symbol)
    layout="wide",
)

# --------------------------
# Sidebar
# --------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center;">
            <img src="https://cdn-icons-png.flaticon.com/512/3176/3176366.png" width="85" style="margin-bottom:10px;" />
            <h2 style="margin-bottom:5px;">LegalEase</h2>
            <p style="font-size:14px; color:#888;">
                Your trusted <b>AI-powered Legal Assistant</b>.<br>
                Upload legal documents and receive precise, context-aware responses.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader(
        "📄 Upload Legal Documents (PDF)",
        type="pdf",
        accept_multiple_files=True,
        help="Upload one or more legal PDF documents for analysis."
    )

    st.divider()
    st.markdown("### ⚙️ Settings")
    tone = st.selectbox("Response Style", ["Formal", "Simplified", "Summary"])
    st.caption("© 2025 LegalEase. All rights reserved.")

# --------------------------
# Main Interface
# --------------------------
st.title("⚖️ AI Legal Assistant")
st.markdown("Ask any legal question related to your uploaded documents.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------------------------
# Input Area
# --------------------------
user_query = st.text_area(
    "Enter your question:",
    height=120,
    placeholder="Example: What are the legal obligations of the employer mentioned in the document?",
)

# --------------------------
# Submit Button
# --------------------------
if st.button("Submit Query", use_container_width=True):
    if uploaded_files and user_query.strip():
        st.chat_message("user").markdown(f"**You:** {user_query}")

        with st.spinner("Analyzing documents and preparing your response..."):
            time.sleep(0.5)
            retrieved_docs = retrieve_docs(user_query)
            response = answer_query(documents=retrieved_docs, model=llm_model, query=user_query)

        with st.chat_message("assistant"):
            st.markdown(f"**AI Response:**\n\n{response}")
            st.markdown("_Response generated based on uploaded document context._")

        # Save chat
        st.session_state.chat_history.append({"user": user_query, "ai": response})

    elif not uploaded_files:
        st.error("⚠️ Please upload at least one PDF file before asking a question.")
    else:
        st.warning("⚠️ Please enter your question before submitting.")

# --------------------------
# Chat History Section
# --------------------------
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("### 💬 Previous Conversations")

    for i, chat in enumerate(st.session_state.chat_history[::-1]):
        idx = len(st.session_state.chat_history) - 1 - i
        with st.expander(f"Conversation {idx + 1}"):
            col1, col2 = st.columns([12, 1])
            with col1:
                st.markdown(f"**You:** {chat['user']}")
                st.markdown(f"**AI:** {chat['ai']}")
            with col2:
                if st.button("❌", key=f"delete_{idx}", help="Delete this conversation"):
                    st.session_state.chat_history.pop(idx)
                    st.rerun()

# --------------------------
# Custom Styling
# --------------------------
st.markdown(
    """
    <style>
        /* Global font */
        body, div, textarea, button {
            font-family: 'Segoe UI', sans-serif;
        }

        /* Text area styling */
        .stTextArea textarea {
            border-radius: 8px;
            border: 1px solid #ccc;
            padding: 10px;
            font-size: 15px;
            background-color: #f9f9f9;
        }

        /* Buttons */
        .stButton>button {
            border-radius: 6px;
            background-color: #2E86C1;
            color: white;
            font-size: 15px;
            font-weight: 600;
            border: none;
            width: 100%;
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            background-color: #1F618D;
        }

        /* Expander styling */
        .streamlit-expanderHeader {
            font-weight: 600;
            font-size: 15px;
        }

        /* Sidebar logo alignment */
        [data-testid="stSidebar"] img {
            display: block;
            margin: 0 auto;
        }

        /* Footer hidden */
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)
