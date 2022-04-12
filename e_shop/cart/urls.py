from django.urls import path
from .views import (
    CartMain
)


urlpatterns = [
    path('cart/', CartMain.as_view(), name='cart-main')
]