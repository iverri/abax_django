from django.urls import path
from .views import BusInfoApiView

urlpatterns = [
    path("api/", BusInfoApiView.as_view()),
]
