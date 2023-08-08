from django.urls import path
from .views.pos_view import product_order_view, add_order_view, clear_cart_items, cart_updated, order_transaction, remove_cart_item
from .views.product_view import product_view, delete_product, update_product, publish_unpublish_product
from .views.order_view import sales_view, pay_balance, pay_order, sales_details, order_view, accept_order, cancel_order
from .views.customer_view import customer_view, customer_detail_view, update_customer
from .views.category_view import add_category
from .views.item_request_view import request_item, delete_request, request_product_restock, request_status_update, item_request_view
from .views.user_view import register_user


app_name = 'store'
urlpatterns = [
    path('pos', product_order_view, name='pos_view'),
    path('update-quantity/<bar_code>', cart_updated, name='update_quantity'),
    path('remove-item/<bar_code>', remove_cart_item, name='remove_cart_item'),
    path('sales', sales_view, name='sales_view'),
    path('orders', order_view, name='order_view'),
    path('orders/accept/<order_id>', accept_order, name='accept_order'),
    path('orders/cancel/<order_id>', cancel_order, name='cancel_order'),
    path('add-orders/<pk>', add_order_view, name='add_order'),
    path('orders/clear', clear_cart_items, name='clear_order'),
    path('orders/details/<order_id>', sales_details, name='sales_details'),
    path('orders/balance/<pk>', pay_balance, name='pay_balance'),
    path('orders/pay/<order_id>', pay_order, name='pay_order'),
    path('', product_view, name='product_view'),
    # path('add', add_product, name='add_product_view'),
    path('categories/add', add_category, name='add_category'),
    path('update/<pk>', update_product, name='update_product'),
    path('publish/update/<pk>', publish_unpublish_product, name='publish_unpublish_product'),
    path('delete/<pk>', delete_product, name='delete_product'),
    path('request', item_request_view, name='item_request_view'),
    path('request/item', request_item, name='request_item'),
    path('request/item/restock/<pk>', request_product_restock, name='request_product_restock'),
    path('request/item/delete/<pk>', delete_request, name='delete_request'),
    path('request/item/update/<pk>', request_status_update, name='request_status_update'),
    path('customers', customer_view, name='customer_view'),
    path('customers/update/<pk>', update_customer, name='update_customer'),
    path('customers/details/<pk>', customer_detail_view, name='customer_details'),
    path('process-order', order_transaction, name='process_order'),
    path('users/registration', register_user, name='register_user'),
]