"""
ASGI config for gigachat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from Users.routing import ws_urlpatterns
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gigachat.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': JWTAuthMiddlewareStack(URLRouter(ws_urlpatterns)),
})
