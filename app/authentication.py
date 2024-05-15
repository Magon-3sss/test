import jwt, datetime
from rest_framework import exceptions

def get_user_permissions(user):
    # Assuming you are using Django's built-in permissions
    return [perm.codename for perm in user.user_permissions.all()]

def create_access_token(user):
    group = [group.name for group in user.groups.all()]
    print(group)
    permissions = get_user_permissions(user)
    print(permissions)
    return jwt.encode({
        'user_id': user.id,
        'username': user.username,
        'group': group,
        'permissions': permissions,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
        'iat': datetime.datetime.utcnow()
    }, 'access_secret', algorithm='HS256')

def decode_access_token(token):
    try:
        payload = jwt.decode(token, 'access_secret', algorithms='HS256')

        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('unauthenticated')

def create_refresh_token(user):
    groups = [group.name for group in user.groups.all()]
    permissions = get_user_permissions(user)
    return jwt.encode({
        'user_id': id,
        'username': user.username,
        'groups': groups,
        'permissions': permissions,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }, 'refresh_secret', algorithm='HS256')

def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, 'refresh_secret', algorithms='HS256')

        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('unauthenticated')
    
def decode_jwt(token):
    try:
        payload = jwt.decode(token, 'YOUR_SECRET_KEY', algorithms=['HS256'])
        return payload['group']
    except jwt.ExpiredSignatureError:
        return "expired"
    except jwt.InvalidTokenError:
        return "invalid"