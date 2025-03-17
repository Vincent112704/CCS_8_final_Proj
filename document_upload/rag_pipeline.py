'''
This file is responsible for translating pdf documents into text, chunking the texts, 
and generating a quiz usimg a RAG model 
'''

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List

class QuizGenerator:
    def __init__(self):
        pass
    
    def pdf_to_text(pdf_path : str) -> str:
        read_pdf = PdfReader(pdf_path)
        content = "" #declare an empty string to append string to
        numOfPages = read_pdf.pages #gets the number of pages

        for page in numOfPages:
            content += page.extract_text() + '\n\n'

        return content
    
    def chunk_splitter (text : str) -> List[str]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=20,
            chunk_overlap=8
        )
        output = text_splitter.split_text(text)

        return output
    
    def rag_quiz (chunks : List[str]) -> List[str]:
        pass