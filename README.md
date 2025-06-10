## YouTube Video Summarizer and Hindi Translator
This project automates the process of summarizing YouTube video content and translating it into Hindi. It combines modern NLP techniques with generative AI to offer concise, accessible summaries of video content for users who prefer to consume information in Hindi.

🧠 Key Features
📽️ Extracts video transcripts using youtube-transcript-api

🔍 Semantic chunking and embedding using Hugging Face's sentence-transformers

⚡ Fast similarity search using FAISS vector database

🌐 Translation of text chunks to Hindi

🤖 Summary generation using Google Gemini AI

🖥️ Simple and user-friendly web interface

📌 How It Works
1. Input
User provides a YouTube video link.

2. Transcript Extraction
The system retrieves captions using youtube-transcript-api (only works if captions are available).

3. Chunking & Embedding
Transcript is divided into small chunks.

Each chunk is converted to embeddings using Hugging Face's Sentence Transformers.

4. Vector Storage
Embeddings are stored in a FAISS vector database for fast and efficient semantic search.

5. Translation
Transcript chunks are translated into Hindi using translation APIs (e.g., Google Translate or similar).

6. Semantic Search & Summarization
User query (in Hindi) is semantically matched to the most relevant chunks from the video.

Google Gemini AI generates a coherent summary or direct response in Hindi.

7. Output
The response is presented to the user via a simple web interface.

🛠️ Technologies Used
Component	Technology
Transcript Extraction	youtube-transcript-api
Embedding	Hugging Face sentence-transformers
Vector Search	FAISS (Facebook AI Similarity Search)
Translation	Google Translate API (or similar)
Summarization	Google Gemini AI
Backend	Flask / FastAPI
Frontend	Streamlit / HTML-CSS-JS
