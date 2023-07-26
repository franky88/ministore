from django.shortcuts import render, get_object_or_404, redirect
from store.models import OrderTransaction, Customer
from store.cartitem import Cart
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count, F
from django.contrib import messages

def order_view(request):
    orders = OrderTransaction.objects.all()
    paid_orders = OrderTransaction.objects.filter(is_paid=True).aggregate(total=(Sum(F('price') * F('quantity'))))
    unpaid_orders = OrderTransaction.objects.filter(is_paid=False).aggregate(total=(Sum(F('price') * F('quantity'))))
    cart = Cart(request)
    cart_items = cart.__len__()
    context = {
        "title": "orders",
        "orders": orders,
        "cart_items": cart_items,
        "paid_orders": paid_orders['total'],
        "unpaid_orders": unpaid_orders['total']
    }
    return render(request, 'order_view.html', context)

def order_details(request, order_id):
    instance = get_object_or_404(OrderTransaction, order_id=order_id)
    cart = Cart(request)
    cart_items = cart.__len__()
    context = {
        'title': 'order details',
        'instance': instance,
        'cart_items': cart_items,
    }
    return render(request, 'order_details.html', context)

@require_POST
def pay_balance(request, customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)
    unpaid_orders = OrderTransaction.objects.filter(customer=customer).filter(is_paid=False)
    if request.method == "POST":
        for instance in unpaid_orders:
            instance.is_paid = True
            instance.save()
            messages.add_message(request, messages.SUCCESS, '%s paid balance successfully. Thank you!'%(customer.name))
        return redirect('store:customer_details', customer.customer_id)

@require_POST
def pay_order(request, order_id, *args, **kwargs):
    instance = get_object_or_404(OrderTransaction, order_id=order_id)
    orderID = kwargs.get('order_id')
    
    if request.method == "POST":
        instance.is_paid = True
        instance.save()
        messages.add_message(request, messages.SUCCESS, 'Order paid successfully.')
        return redirect('store:customer_details', instance.customer.customer_id)