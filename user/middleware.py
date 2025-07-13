from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.db import database_sync_to_async
from django.db import close_old_connections

@database_sync_to_async
def get_user(validated_token):
    try:
        jwt_authenticator = JWTAuthentication()
        user = jwt_authenticator.get_user(validated_token)
        return user
    except Exception:
        return AnonymousUser()

class TokenAuthMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token")

        if token:
            try:
                validated_token = UntypedToken(token[0])
                scope["user"] = await get_user(validated_token)
            except Exception:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        close_old_connections()

        return await self.app(scope, receive, send)
