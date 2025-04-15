from django.urls import path
from .views import BuyAccessView

urlpatterns = [
    path("", BuyAccessView.as_view(), name="buy_access"),
]
