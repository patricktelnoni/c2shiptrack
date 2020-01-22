from django.conf.urls import url
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    url(r'ws/maps/(?P<room_name>\w+)/$', consumers.MapsConsumer),
]