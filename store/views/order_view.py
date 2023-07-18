from django.shortcuts import render, get_object_or_404, redirect
from store.models import OrderTransaction


def order_view(request):
    orders = OrderTransaction.objects.all()
    context = {
        "title": "orders",
        "orders": orders
    }
    return render(request, 'order_view.html', context)