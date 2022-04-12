# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')

from django.urls import path
from .views import (
    ContactsMain,
)


urlpatterns = [
    path('contacts/', ContactsMain.as_view(), name='contacts-main'),
]