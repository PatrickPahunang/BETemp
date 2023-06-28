from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password , check_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.conf import settings
from datetime import datetime, timedelta
import jwt
from django.core import serializers
import json
from django.core.files.base import ContentFile
import uuid
from django.contrib.auth.decorators import permission_required
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model






# Create your views here.

def landing(request):
    return HttpResponse('<div style="width:100vw; height:100vh; font-weight:1000; color:green; display:flex; justify-content:center; align-items:center; font-family:helvetica; font-size:20px;">DJANGO Backend Server is UP and RUNNING!<div>')
    


def generate_jwt(user):
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token

    # Return the JWT as a string or JSON response, depending on your use case
    return str(access_token)


@csrf_exempt
def update_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        user = CustomUser.objects.get(id=user_id)
        #print(user)
        #print(request.POST)
        #print(request.FILES)
        
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            profile_picture = request.FILES.get('profile_picture')

            

            if profile_picture.name != user.profile_picture.name:
                    # Save the new profile picture
                    filename = f"{profile_picture.name.split('.')[0]}_{uuid.uuid4().hex}.{profile_picture.name.split('.')[-1]}"
                    user.profile_picture.save(filename, profile_picture, save=False)
            user.first_name = first_name
            user.last_name = last_name     
            user.save()  # Save the updated user in the database
            return JsonResponse({'message': 'User updated successfully'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)

@csrf_exempt
def get_user(request,user_id):
    if request.method == 'GET':
        try:
            user = CustomUser.objects.get(id=user_id)
            user_data = {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'profile_picture': user.profile_picture.url if user.profile_picture else None,
            }
            response = JsonResponse(user_data, status=200)
            response["Access-Control-Allow-Origin"] = "http://127.0.0.1:3000/"
            response["Access-Control-Allow-Methods"] = "GET, DELETE, HEAD, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            return response
        
        except CustomUser.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)

    return JsonResponse({'message': 'Invalid request method'}, status=400)


@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(username=username)
            if check_password(password, user.password):
                login(request, user)
                payload = {
                    'user_id': user.id,
                    'exp': datetime.utcnow() + timedelta(days=1)  # Token expiration
                    }
                tkn = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                serialized_user = serializers.serialize('json', [user])
                deserialized_user = json.loads(serialized_user)[0]
                fields = deserialized_user['fields']
                user_id = deserialized_user['pk']
                specific_fields = {
                    'id': user_id,
                }





                return JsonResponse({'message': 'Login successful', 'status': 200 , 'token': tkn ,'data': specific_fields  } )
                
            else:
                return JsonResponse({'message': 'Incorrect Password'}, status=401)
        except CustomUser.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)

    return JsonResponse({'message': 'Invalid request method'}, status=400)



@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        # Get the data from the Axios request
        data = request.POST
        email = data.get('email')
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')
        password2 = data.get('password2')
        profile_picture = request.FILES.get('profile_picture') 


        try:
            # Check if the user or email already exists
            if CustomUser.objects.filter(username=username).exists():
                raise ValidationError('Username already exists')
        
            if CustomUser.objects.filter(email=email).exists():
                raise ValidationError('Email already exists')
            if password != password2:
                raise ValidationError('Password Does not Match')
        
            # Create a new CustomUser object
            user = CustomUser(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
            
            if profile_picture:
                filename = f"{profile_picture.name.split('.')[0]}_{uuid.uuid4().hex}.{profile_picture.name.split('.')[-1]}"
                user.profile_picture.save(filename, profile_picture, save=False)
        
            user.set_password(password)
            user.save()


            # Return a JSON response indicating success
            response = {'message': 'User created successfully', 'status': 'success'}
            return JsonResponse(response)
        except ValidationError as e:
            # Return a JSON response with the validation error message
            response = {'message': str(e), 'status': 'error'}
            return JsonResponse(response, status=400)
        except IntegrityError:
            # Return a JSON response if there is an integrity error
            response = {'message': 'An error occurred while creating the user', 'status': 'error'}
            return JsonResponse(response, status=500)

    # Handle other HTTP methods if needed
    else:
        response = {'message': 'Invalid request method', 'status': 'error'}
        return JsonResponse(response, status=400)




@csrf_exempt
def api_example(request):
    if request.method == 'GET':
        # Logic for handling GET requests
        data = {
            'message': 'This is a GET request.',
            'status': 'success'
        }
        return JsonResponse(data)

    elif request.method == 'POST':
        # Logic for handling POST requests
        data = {
            'message': 'This is a POST request.',
            'status': 'success'
        }
        return JsonResponse(data)

    elif request.method == 'PATCH':
        # Logic for handling POST requests
        data = {
            'message': 'This is a PATCH request.',
            'status': 'success'
        }
        return JsonResponse(data)

    # Add other HTTP methods (PUT, DELETE, etc.) if needed
    else:
        data = {
            'message': 'Invalid request method.',
            'status': 'error'
        }
        return JsonResponse(data, status=400)