from django.shortcuts import render
from django.http import HttpResponse
from .rag_pipeline import QuizGenerator
from io import BytesIO

def hello (request):
    return render(request, "document_upload/index.html")

def upload (request):
    if request.method == "POST":
        uploaded_file = request.FILES["pdf_document"] #Accesses the uploaded file from the form in index.html.
        pdf_file = BytesIO(uploaded_file.read()) #Reads the file and stores it in a BytesIO object.
        pdf_text = QuizGenerator.pdf_to_text(pdf_file) #Converts the pdf file to text.
        chunks = QuizGenerator.chunk_splitter(pdf_text) #Splits the text into chunks.
        return HttpResponse(chunks)
    

