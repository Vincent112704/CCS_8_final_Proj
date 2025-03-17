from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

embedder = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("GEMINI_API_KEY"))
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))
class RAGModel:
    def __init__(self):
        self.embedder = embedder
        self.llm = llm

    def vector_DBRetriever(text : List[str]) -> Chroma:
        db = Chroma.from_texts(text, embedder)
        retriever = db.as_retriever(search_type="similarity",search_kwargs={"k":3})
        return retriever

    

    