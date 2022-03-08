import jwt
from django.http import JsonResponse
from quest101.settings import ALGORITHM, SECRET_KEY
from users.models import User
from quest101.settings import SECRET_KEY, ALGORITHM


def Authorize(func):
    def wrapper(self, request, *args, **kwargs):
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
    return wrapper


def AuthorizeProduct(func):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            request.user = None
            return func(self, request, *args, **kwargs)

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user = User.objects.get(id=payload['user_id'])
        request.user = user

        return func(self, request, *args, **kwargs)

    return wrapper
