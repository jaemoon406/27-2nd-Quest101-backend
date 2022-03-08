import jwt
from django.http import JsonResponse
from quest101.settings import ALGORITHM, SECRET_KEY
from users.models import User
from quest101.settings import SECRET_KEY, ALGORITHM



class MyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user, True)

def Authorize(func):
    def __init__(self, original_function):
        self.original_function = original_function
    
    def __call__(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')

            if not token:
                return JsonResponse({'message': 'TOKEN_REQUIRED'}, status=401)

            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.user = User.objects.get(id=payload['user_id'])

            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)



def AuthorizeProduct(func):
    def wrapper(self, request, *args, **kwargs):
        print(request.body, 'request.bodyrequest.bodyrequest.body')
        token = request.headers.get('Authorization')

        if not token:
            request.user = None
            return func(self, request, *args, **kwargs)

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user = User.objects.get(id=payload['user_id'])
        request.user = user

        return func(self, request, *args, **kwargs)

    return wrapper
