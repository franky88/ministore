from django.urls import path
from .views.pos_view import product_order_view, add_order_view, clear_cart_items, cart_updated, add_customer_view, order_transaction
from .views.product_view import add_product, delete_product

app_name = 'store'
urlpatterns = [
    path('', product_order_view, name='pos_view'),
    path('update-quantity/<bar_code>', cart_updated, name='update_quantity'),
    path('add-orders/<pk>', add_order_view, name='add_order'),
    path('order-clear/', clear_cart_items, name='clear_order'),
    path('add-product/', add_product, name='add_product'),
    path('add-customer/', add_customer_view, name='add_customer'),
    path('process-order/', order_transaction, name='process_order'),
    path('delete-product/<pk>', delete_product, name='delete_product'),
]