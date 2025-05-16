from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework_simplejwt.tokens import AccessToken
from accounts.models import users
from .models import Notes, Pages, Block
from django.http import JsonResponse

@csrf_exempt
@permission_classes([IsAuthenticated])
def saveNotebook(request):
    body = json.loads(request.body)
    token = request.headers.get('Authorization').split(' ')[1]
    access_token = AccessToken(token)
    user_id = access_token['user_id']
    
    try:
        user = users.objects.get(id=user_id)
        notebook = Notes.objects.create(user=user, title=body["title"])
    
        for page_data in body["pages"]:
            page = Pages.objects.create(noteBook=notebook, title=page_data["title"])
            for block_data in page_data["blocks"]:
                Block.objects.create(page=page, content=block_data["content"])
        
        pages= Pages.objects.filter(noteBook=notebook)
        blocks = Block.objects.all()
        return JsonResponse({
            "notebook ID": notebook.id,
            "user ID": user.id,
            "title": notebook.title,
            "pages": [{
                "page ID": page.id,
                "title": page.title,
                "blocks": [{
                    "block ID": block.id,
                    "content": block.content
                } for block in blocks if block.page == page]
            } for page in pages],
            "status": 200})
    except Exception as e:  
        return JsonResponse({"message": str(e), "status": 500})
    

@csrf_exempt
@permission_classes([IsAuthenticated])
def getNotebook(request):
    token = request.headers.get('Authorization').split(' ')[1]
    access_token = AccessToken(token)
    user_id = access_token['user_id']
    
    try:
        user = users.objects.get(id=user_id)
        notebooks = Notes.objects.filter(user=user)
        
        notebook_data = []
        for notebook in notebooks:
            pages = Pages.objects.filter(noteBook=notebook)
            blocks = Block.objects.all()
            
            notebook_data.append({
                "notebook ID": notebook.id,
                "title": notebook.title,
                "pages": [{
                    "page ID": page.id,
                    "title": page.title,
                    "blocks": [{
                        "block ID": block.id,
                        "content": block.content
                    } for block in blocks if block.page == page]
                } for page in pages]
            })
        
        return JsonResponse({"notebooks": notebook_data, "status": 200})
    except Exception as e:
        return JsonResponse({"message": str(e), "status": 500})
    
@csrf_exempt
@permission_classes([IsAuthenticated])
def deleteNotebook(request):
    body = json.loads(request.body)
    token = request.headers.get('Authorization').split(' ')[1]
    access_token = AccessToken(token)
    user_id = access_token['user_id']

    try:
        user = users.objects.get(id=user_id)
        notebook = Notes.objects.get(id=body["notebook_ID"], user=user)
        notebook.delete()
        
        return JsonResponse({"message": "Notebook deleted successfully!", "status": 200})
    except Exception as e:
        return JsonResponse({"message": str(e), "status": 500})

@csrf_exempt
@permission_classes([IsAuthenticated])
def getOneNB(request):
    body = json.loads(request.body)
    token = request.headers.get('Authorization').split(' ')[1]
    access_token = AccessToken(token)
    user_id = access_token['user_id']
    
    try:
        user = users.objects.get(id=user_id)
        notebook = Notes.objects.get(id=body["notebook_ID"], user=user)
        pages = Pages.objects.filter(noteBook=notebook)
        blocks = Block.objects.all()
        
        notebook_data = {
            "notebook ID": notebook.id,
            "title": notebook.title,
            "pages": [{
                "page ID": page.id,
                "title": page.title,
                "blocks": [{
                    "block ID": block.id,
                    "content": block.content
                } for block in blocks if block.page == page]
            } for page in pages]
        }
        
        return JsonResponse({"notebook": notebook_data, "status": 200})
    except Exception as e:
        return JsonResponse({"message": str(e), "status": 500})
