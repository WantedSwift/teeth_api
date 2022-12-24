from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from api.models import users
import json
from django.forms.models import model_to_dict
import uuid
import requests
# Create your views here.


@csrf_exempt
def get_user(request):
    try:
        token = request.POST["token"]
      
    except Exception as exc:
        return  JsonResponse({
            'status' : False,
            'message' : "please insert token"
         } , encoder=json.JSONEncoder)

    try:
        object_user = users.objects.get(token=token)
        ll = model_to_dict(object_user)
        ll['created_at'] = str(object_user.created_at)

        return JsonResponse({
            'status': True,
            'data': ll
        }, encoder=json.JSONEncoder)

    except Exception as exc:
 
        return JsonResponse({
            'status': False,
            'message': "user is worng"
        }, encoder=json.JSONEncoder)

@csrf_exempt
def login_register(request):
    try:
        email = request.POST["email"]
        fb_token = request.POST["fb_token"]
        id_apple = request.POST["id_apple"]
    except Exception as exc:
        return  JsonResponse({
            'status' : False,
            'message' : "please insert email"
         } , encoder=json.JSONEncoder)

    try:
        object_user = users.objects.get(email=email)
        ll = model_to_dict(object_user)
        ll['created_at'] = str(object_user.created_at)
      

        return JsonResponse({
            'status': True,
            'data': ll
        }, encoder=json.JSONEncoder)

    except users.DoesNotExist:
        token =  uuid.uuid4().hex
        object_user = users.objects.create(token=token ,email=email,fb_token=fb_token,id_apple=id_apple)
        ll = model_to_dict(object_user)
        ll['created_at'] = str(object_user.created_at)
      
        
        return JsonResponse({
            'status': True,
            'data': ll
        }, encoder=json.JSONEncoder)




@csrf_exempt
def oauth_return(request):
    try:
        token = request.POST['id_token']
        fb_token = request.POST['fc_token']
        url = "https://oauth2.googleapis.com/tokeninfo?id_token=" + token
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        users_json = json.loads(response.text)
        email = users_json['email']
        print(users_json)
        print('email is => ',email)

        try:
            user = users.objects.get(email=email)
            if not user.token:
                token =  uuid.uuid4().hex
                user.token = token
                
            user.fb_token = fb_token
            user.save()

            #user.created_at = str(user.created_at)
            json_user = model_to_dict(user)
            json_user['created_at'] = str(user.created_at)

            return JsonResponse({
               'status': True,
                'message': 'ok',
                'user': json_user
            }, encoder=json.JSONEncoder)

        except users.DoesNotExist:
            user = users.objects.create(email=email)
            if not user.token:
                token =  uuid.uuid4().hex
                user.token = token
                user.fb_token = fb_token
                user.save()

          
            #user.created_at = str(user.created_at)
            json_user = model_to_dict(user)
            json_user['created_at'] = str(user.created_at)

           

            return JsonResponse({
               'status': True,
                'message': 'ok',
                'user': json_user
            }, encoder=json.JSONEncoder)

  
    #except Exception as exc:
    except Exception as exc:
        return JsonResponse({
            'status': False,
            'message': "invalid id_token"
        })
   

