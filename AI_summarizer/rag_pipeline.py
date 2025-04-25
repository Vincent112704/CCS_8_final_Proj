from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from .rag_model import RAGModel


class Chatbot:
    def __init__(self):
        self.rag_model = RAGModel()
        self.Vector_DB = None
        self.retriever = None
    def pdf_to_text(self, pdf_path: str) -> str:
        """
        Converts a PDF file to text.
        """
        try:
            read_pdf = PdfReader(pdf_path)
            content = ""  # Declare an empty string to append text to
            numOfPages = read_pdf.pages  # Gets the number of pages

            for page in numOfPages:
                text = page.extract_text()
                if text:  # Ensure text is not None
                    content += text + '\n\n'

            if not content.strip():  # Check if the content is empty
                raise ValueError("The PDF contains no readable text.")

            return content
        except Exception as e:
            raise ValueError(f"Error reading PDF: {e}")

    def chunk_splitter(self, text: str) -> List[str]:
        """
        Splits text into chunks using a recursive character text splitter.
        """
        if not text.strip():  # Check if the text is empty
            raise ValueError("Input text is empty. Cannot split into chunks.")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=50
        )
        output = text_splitter.split_text(text)

        return output
    
    def vectorInit(self, chunks: List[str]) -> List[str]:
        
        if not chunks:  # Check if chunks are empty
            raise ValueError("Chunks are empty. Cannot summarize your document.")

        try:
            if self.Vector_DB is None:
                self.Vector_DB = self.rag_model.vector_DB(chunks)
            if self.retriever is None:
                self.retriever = self.rag_model.retriever(self.Vector_DB)

        except Exception as e:
            raise ValueError(f"Error generating quiz: {e}")
    
    def __call__(self, query: str):
        """
        Calls the RAG model with a query.
        """
        if self.retriever is None:
            raise ValueError("Retriever is not initialized. Cannot process query.")

        try:
            retrieved_docs = self.retriever.get_relevant_documents(query)
            rag_chain = self.rag_model.rag_chain()
            response = rag_chain.invoke({"input_documents": retrieved_docs})
            return response['output_text']
        except Exception as e:
            raise ValueError(f"Error processing query: {e}")
        