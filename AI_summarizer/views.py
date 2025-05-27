from .rag_pipeline import Chatbot
from io import BytesIO
from .models import ChatHistory
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render

summarizer = Chatbot()
def posttempl(request):
    return render(request, "AI_summarizer/index.html")
def posttempl2(request):
    return render(request, "AI_summarizer/ai.html")

@csrf_exempt
def postPDF (request): 

    try: 
        uploaded_file = request.FILES.get('pdf_document')
        pdf_file = BytesIO(uploaded_file.read()) 

        pdf_text = summarizer.pdf_to_text(pdf_file) 
        chunks = summarizer.chunk_splitter(pdf_text) 
        summarizer.vectorInit(chunks)
        
        return JsonResponse({"message": "PDF processed successfully", "status": 200})
    except Exception as e:
        return JsonResponse({"message": str(e), "status": 500})

@csrf_exempt
def chat(request):
    body = json.loads(request.body)
    try:
        res = summarizer(body["user_input"])
        ChatHistory.objects.create(user_input=body["user_input"], llm_output=res)
        chat_history = ChatHistory.objects.all()
        return JsonResponse({"response": res})
    except Exception as e:
        return JsonResponse({"message": str(e), "status": 500})

