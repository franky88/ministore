from django.shortcuts import render, get_object_or_404, redirect
from store.models import OrderTransaction, Customer
from store.cartitem import Cart
from django.views.decorators.http import require_POST


def order_view(request):
    orders = OrderTransaction.objects.all()
    cart = Cart(request)
    cart_items = cart.__len__()
    context = {
        "title": "orders",
        "orders": orders,
        "cart_items": cart_items
    }
    return render(request, 'order_view.html', context)