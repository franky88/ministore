from django.urls import path
from .views.pos_view import product_order_view, add_order_view, clear_cart_items, cart_updated, order_transaction
from .views.product_view import add_product, delete_product
from .views.order_view import order_view
from .views.customer_view import add_customer_view, customer_view, customer_detail_view
from .views.category_view import add_category

app_name = 'store'
urlpatterns = [
    path('', product_order_view, name='pos_view'),
    path('update-quantity/<bar_code>', cart_updated, name='update_quantity'),
    path('orders/', order_view, name='order_view'),
    path('add-orders/<pk>', add_order_view, name='add_order'),
    path('order-clear/', clear_cart_items, name='clear_order'),
    path('products/', add_product, name='product_view'),
    path('products/categories/add/', add_category, name='add_category'),
    path('customers/', customer_view, name='customer_view'),
    path('customers/add/', add_customer_view, name='add_customer'),
    path('customers/details/<pk>', customer_detail_view, name='customer_details'),
    path('process-order/', order_transaction, name='process_order'),
    path('delete-product/<pk>', delete_product, name='delete_product'),
]