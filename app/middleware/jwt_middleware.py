import jwt
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone

from noa.settings import SECRET_KEY

def jwt_middleware(get_response):
    def middleware(request):
        jwt_token = request.COOKIES.get('jwt_token')
        if jwt_token:
            # Vérifier le JWT ici en utilisant la clé secrète
            try:
                payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
                user_id = payload['user_id']
                user = User.objects.get(id=user_id)
                login(request, user)  # Connecter l'utilisateur
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token expiré'}, status=401)
            except (jwt.DecodeError, User.DoesNotExist):
                return JsonResponse({'error': 'Token invalide'}, status=401)
        response = get_response(request)
        return response
    return middleware

class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Votre logique de middleware ici
        response = self.get_response(request)
        return response


