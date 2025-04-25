from django.shortcuts import render
from django.http import HttpResponse
from .rag_pipeline import Chatbot
from io import BytesIO
from .models import ChatHistory

summarizer = Chatbot()
# def hello (request):
#     return render(request, "AI_summarizer/index.html")

def index (request): 
    try: 
        if request.method == "POST":
            if "pdf_document" not in request.FILES:
                return HttpResponse("No file uploaded.")
            elif request.FILES["pdf_document"].name.split('.')[-1] != "pdf":
                return HttpResponse("File is not a PDF.")
            else:
                uploaded_file = request.FILES["pdf_document"] #Accesses the uploaded file from the form in index.html.
                pdf_file = BytesIO(uploaded_file.read()) #Reads the file and stores it in a BytesIO object.

                pdf_text = summarizer.pdf_to_text(pdf_file) #Converts the pdf file to text.
                chunks = summarizer.chunk_splitter(pdf_text) #Splits the text into chunks.
                summarizer.vectorInit(chunks)
                return render(request, "AI_summarizer/index.html", {"msg": "File uploaded successfully."})
        elif request.method == "GET":
            return render(request, "AI_summarizer/index.html")
    except Exception as e:
        return HttpResponse(f"Error: {e}")

def chat(request):
    try:
        res = summarizer(request.POST["user_input"])
        ChatHistory.objects.create(user_input=request.POST["user_input"], llm_output=res)
        chat_history = ChatHistory.objects.all()
        return render(request, "AI_summarizer/index.html", {"chat_history": chat_history})
    except Exception as e:
        return HttpResponse(f"Error: {e}")

