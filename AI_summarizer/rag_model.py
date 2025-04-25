from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
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
        self.db = None

    def vector_DB(self, text : List[str]):
        self.db = Chroma.from_texts(text, self.embedder)
        return self.db
    
    def retriever(self, db: Chroma):
        if self.db is None:
            raise ValueError("DB is None")
        return self.db.as_retriever(search_type="similarity",search_kwargs={"k":3})
    
    
    def rag_chain(self):
        prompt_template = PromptTemplate(
            template='''
            Given the following {context} answer the question
            ''',
            input_variables=["context"]
        )
        llm_chain = LLMChain(llm=self.llm, prompt=prompt_template)

        return StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="context")

    