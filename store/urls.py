from django.urls import path
from .views.pos_view import product_order_view, add_order_view, clear_cart_items, cart_updated, order_transaction
from .views.product_view import product_view, delete_product, add_product, update_product
from .views.order_view import order_view, pay_balance
from .views.customer_view import add_customer_view, customer_view, customer_detail_view, update_customer
from .views.category_view import add_category
from .views.item_request_view import request_item, delete_request, request_product_restock, request_status_update

app_name = 'store'
urlpatterns = [
    path('', product_order_view, name='pos_view'),
    path('update-quantity/<bar_code>', cart_updated, name='update_quantity'),
    path('sales', order_view, name='order_view'),
    path('add-orders/<pk>', add_order_view, name='add_order'),
    path('orders/clear', clear_cart_items, name='clear_order'),
    path('orders/balance/<customer_id>', pay_balance, name='pay_balance'),
    path('products/', product_view, name='product_view'),
    path('products/add', add_product, name='add_product_view'),
    path('products/categories/add', add_category, name='add_category'),
    path('products/update/<pk>', update_product, name='update_product'),
    path('products/delete/<pk>', delete_product, name='delete_product'),
    path('products/request/item', request_item, name='request_item'),
    path('products/request/item/restock/<pk>', request_product_restock, name='request_product_restock'),
    path('products/request/item/delete/<pk>', delete_request, name='delete_request'),
    path('products/request/item/update/<pk>', request_status_update, name='request_status_update'),
    path('customers', customer_view, name='customer_view'),
    path('customers/add', add_customer_view, name='add_customer'),
    path('customers/update/<customer_id>', update_customer, name='update_customer'),
    path('customers/details/<customer_id>', customer_detail_view, name='customer_details'),
    path('process-order', order_transaction, name='process_order'),
]