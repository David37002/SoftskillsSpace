import os

# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter  # , URLRouter
from django.core.asgi import get_asgi_application

from softskillspace.utils.settings import get_app_settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", get_app_settings())
django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        # "websocket": AuthMiddlewareStack(
        #     URLRouter(
        #         chat.routing.websocket_urlpatterns
        #     )
        # ),
    }
)
