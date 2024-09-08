import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hub.settings')

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import ai_gen.routing
from daphne.server import Server
import logging

# Set the logging level (you can adjust it based on your needs)
logging.basicConfig(level=logging.INFO)




application = ProtocolTypeRouter({
    'http' : get_asgi_application(),
    'websocket' : AuthMiddlewareStack( 
            URLRouter( 
                ai_gen.routing.websocket_urlpatterns
            )   
    )
})  

if __name__ == "__main__":
    server = Server(application)
    # server.listen('0.0.0.0',2020)
    server.run(port=8000)
    # server.run(application, host='0.0.0.0', port=8000)
