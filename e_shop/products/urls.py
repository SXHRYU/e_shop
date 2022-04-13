from django.urls import path
from .views import (
    products_all_view,
    products_add_view,
    products_detail_view,
    products_filter_view,
    products_update_view,
    products_delete_view,
    products_maker_view,
)


urlpatterns = [
    path('products/', products_all_view, name='products-all'),
    path('products/add/', products_add_view, name='products-add'),
    path('products/filter/', products_filter_view, name='products-filter'),
    path('products/<int:id_>/', products_detail_view, name='products-detail'),
    path('products/<int:id_>/update/', products_update_view, name='products-update'),
    path('products/<int:id_>/delete/', products_delete_view, name='products-delete'),
    path('products/maker/<int:id_>/', products_maker_view, name='products-maker')
]