from django.urls import path
from .views import home, departures

urlpatterns = [
    path('', home, name='home'),
    path('departures/', departures, name='departures'),
]
