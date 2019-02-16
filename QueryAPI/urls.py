from django.urls import path, include
from . import views


urlpatterns = [
    path('user/', include([
        path('', views.UserAPI.as_view(), name='api_user'),
    ])),
]