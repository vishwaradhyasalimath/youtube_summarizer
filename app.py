import streamlit as st

st.set_page_config(page_title="YouTube Video Summarizer & QA", page_icon="🎥", layout="centered")

import os
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
import google.generativeai as genai

os.environ["GEMINI_API_KEY"] = "AIzaSyDEQOEvpQ-mRBotbs67y8aEu4nCK-G0hOkkikto3irt0ro0o"
genai.configure(api_key="AIzaSyDEQOEvpQ-mRBotbs67y8aEu4nCK-G0hOk")

llm = genai.GenerativeModel(model_name='models/gemini-2.0-flash')
prompt = PromptTemplate(
    template="""
      You are a helpful assistant.
      Answer ONLY from the provided transcript context.
      If the context is insufficient, just say you don't know.

      {context}
      Question: {question}
    """,
    input_variables=['context', 'question']
)

@st.cache_resource(show_spinner=False)
def process_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["hi", "en"])
    transcript = " ".join(chunk["text"] for chunk in transcript_list)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(chunks, embeddings)

    return vector_store, transcript

st.title(" YouTube Video Summarizer & QA")

video_id = st.text_input("Enter YouTube Video ID")

vector_store = None
transcript_text = ""

if video_id.strip() != "":
    try:
        vector_store, transcript_text = process_transcript(video_id)
    except TranscriptsDisabled:
        st.error("No captions available for this video.")
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")

col1, col2 = st.columns(2)

with col1:
    if st.button(" Summarize Video"):
        if vector_store:
            with st.spinner("Generating summary..."):
                question = "Summarize the main topic discussed in this video in 500 words in point form."
                retrieved_docs = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4}).invoke(question)
                context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

                final_prompt = prompt.invoke({"context": context_text, "question": question})
                final_prompt_str = final_prompt.to_string()

                answer = llm.generate_content(final_prompt_str)
                summary = answer.text

            st.success("Summary generated!")
            st.subheader("Summary:")
            st.write(summary)

with col2:
    user_question = st.text_input(" Ask a question about the video")

    if st.button("Get Answer"):
        if vector_store:
            if user_question.strip() == "":
                st.warning("Please enter your question!")
            else:
                with st.spinner("Generating answer..."):
                    retrieved_docs = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4}).invoke(user_question)
                    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

                    final_prompt = prompt.invoke({"context": context_text, "question": user_question})
                    final_prompt_str = final_prompt.to_string()

                    answer = llm.generate_content(final_prompt_str)
                    result = answer.text

                st.success("Answer generated!")
                st.subheader("Answer:")
                st.write(result)

# Optional: Show YouTube video preview
if video_id.strip() != "":
    st.video(f"https://www.youtube.com/watch?v={video_id}")

