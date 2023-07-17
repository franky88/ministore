from django.urls import path
from .views.pos_view import product_order_view, add_order_view
from .views.product_view import add_product, delete_product

app_name = 'store'
urlpatterns = [
    path('', product_order_view, name='pos_view'),
    path('add-orders/', add_order_view, name='add_order'),
    path('add-product/', add_product, name='add_product'),
    path('delete-product/<pk>/', delete_product, name='delete_product'),
]