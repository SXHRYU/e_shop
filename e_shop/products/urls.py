from django.urls import path
from .views import (
    products_add_view,
    products_all_view,
    products_detail_view,
    products_filter_view,
    products_update_view,
    products_delete_view,
)


urlpatterns = [
    path('products/add/', products_add_view, name='products-add'),
    path('products/', products_all_view, name='products-all'),
    path('products/filter/', products_filter_view, name='products-filter'),
    path('products/<int:id>/', products_detail_view, name='products-detail'),
    path('products/<int:id>/update/', products_update_view, name='products-update'),
    path('products/<int:id>/delete/', products_delete_view, name='products-delete'),
]