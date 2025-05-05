from django.shortcuts import render
from django.http import JsonResponse
from .models import users
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
import json

# def loginTemplate(request):
#     return render(request, "accounts/login.html")
# def signupTemplate(request):
#     return render(request, "accounts/signup.html")
# def deleTemplate(request):
#     return render(request, "accounts/delete.html")

@csrf_exempt
@permission_classes([IsAuthenticated])
def deleteAccount(request):
    body = json.loads(request.body)
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        user = users.objects.get(id=user_id)
        
        if body["password"] == user.password:
            user.delete()
            return JsonResponse({"message": "User deleted successfully!", "status": 200})
        else:
            return JsonResponse({"message": "Invalid password!", "status": 401})
    except Exception as e:
        return JsonResponse({"message": str(e), "status": 500})
    
@csrf_exempt
@permission_classes([IsAuthenticated])
def manageAccount(request):
    body = json.loads(request.body)
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        user = users.objects.get(id=user_id)
        
        if body["username"]:
            user.username = body["username"]
        if body["email"]:
            user.email = body["email"]
        if body["phone"]:
            user.phone = body["phone"]
        if body["school"]:
            user.school = body["school"]
        if body["address"]:
            user.address = body["address"]
        if body["password"]:
            user.password = body["password"]
        
        user.save()

        return JsonResponse({"message": "User updated successfully!",
                             "user": {
                                 "username": user.username,
                                 "email": user.email,
                                 "phone": user.phone,
                                 "school": user.school,
                                 "address": user.address
                             }, 
                             "status": 200})

    except Exception as e:
        return JsonResponse({"message": str(e), "status": 500})

def signup(request):
    body = json.loads(request.body)
    try:
    
        if body["username"] in users.objects.values_list('username', flat=True):
            return JsonResponse({"message": "Username already exists!", "status": 400})
        if body["email"] in users.objects.values_list('email', flat=True):
            return JsonResponse({"message": "Email already exists!", "status": 400})
        if body["password"] in users.objects.values_list('password', flat=True):
            return JsonResponse({"message": "Password already exists!", "status": 400})
        
        new_user = users.objects.create(
            username=body["username"],
            password=body["password"],
            email=body["email"],        
        )

        new_user.save()

        return JsonResponse({"message": "User created successfully!", 
                             "user": {
                                 "username": new_user.username,
                                 "email": new_user.email
                             }, 
                             "status": 200})
    except Exception as e:
        return JsonResponse({"message": str(e), "status": 500})
    
@csrf_exempt
def login(request):
    try:
        body = json.loads(request.body)
        user = users.objects.get(username=body["username"])
        if user.password == body["password"]:
            refresh = RefreshToken.for_user(user)

            return JsonResponse({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=200)
        else:
            return JsonResponse({"message": "Invalid password!", "status": 401})
    except users.DoesNotExist:
        return JsonResponse({"message": "User does not exist!", "status": 404})
    except Exception as e:
        return JsonResponse({"message": str(e), "status": 500})
