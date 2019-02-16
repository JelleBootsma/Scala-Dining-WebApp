from django.urls import path, include

from . import views
from .views import DayView, index

urlpatterns = [
    path('user/', include([
        path('', DayView.as_view(), name='api_user'),
    ])),
]