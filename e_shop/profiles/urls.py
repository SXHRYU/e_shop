from django.urls import path
from .views import (
    ProfileAll,
    ProfileCreate,
    ProfileDetail,
    ProfileDelete,
    ProfileUpdate,
)


urlpatterns = [
    path('profiles/all/', ProfileAll.as_view(), name='profiles-all'),
    path('profiles/create/', ProfileCreate.as_view(), name='profiles-create'),
    path('profiles/<int:pk>/', ProfileDetail.as_view(), name='profiles-detail'),
    path('profiles/<int:pk>/delete/', ProfileDelete.as_view(), name='profiles-delete'),
    path('profiles/<int:pk>/update/', ProfileUpdate.as_view(), name='profiles-update'),
]