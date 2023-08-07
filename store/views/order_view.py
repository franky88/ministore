from django.shortcuts import render, get_object_or_404, redirect
from store.models import OrderTransaction, Customer
from django.contrib.auth.models import User
from store.cartitem import Cart
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count, F, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required("store.view_ordertransaction", raise_exception=True)
def sales_view(request):
    orders = OrderTransaction.objects.all()
    paid_orders = OrderTransaction.objects.filter(Q(is_paid=True), Q(is_accepted=True)).aggregate(total=(Sum(F('price') * F('quantity'))))
    unpaid_orders = OrderTransaction.objects.filter(Q(is_paid=False), Q(is_accepted=True)).aggregate(total=(Sum(F('price') * F('quantity'))))
    cart = Cart(request)
    cart_items = cart.__len__()
    context = {
        "title": "sales",
        "orders": orders,
        "cart_items": cart_items,
        "paid_orders": paid_orders['total'],
        "unpaid_orders": unpaid_orders['total']
    }
    return render(request, 'sales_view.html', context)

@login_required
@permission_required("store.view_ordertransaction", raise_exception=True)
def sales_details(request, order_id):
    instance = get_object_or_404(OrderTransaction, order_id=order_id)

    cart = Cart(request)
    cart_items = cart.__len__()

    context = {
        'title': 'sales details',
        'instance': instance,
        'cart_items': cart_items,
    }
    return render(request, 'sales_details.html', context)

@login_required
def order_view(request):
    if request.user.is_superuser:
        orders = OrderTransaction.objects.all()
        balance = orders.filter(Q(is_paid=False) and Q(is_accepted=True)).aggregate(total=(Sum(F('price') * F('quantity'))))
    else:
        orders = OrderTransaction.objects.filter(customer=request.user)
        balance = orders.filter(Q(is_paid=False) and Q(is_accepted=True)).aggregate(total=(Sum(F('price') * F('quantity'))))
    cart = Cart(request)
    cart_items = cart.__len__()

    context = {
        "title": "orders",
        "orders": orders,
        "cart_items": cart_items,
        "balance": balance['total']
    }
    return render(request, 'order_view.html', context)

@login_required
@require_POST
@permission_required("store.update_ordertransaction", raise_exception=True)
def accept_order(request, order_id):
    instance = get_object_or_404(OrderTransaction, order_id=order_id)
    if request.method == 'POST':
        instance.is_accepted = True
        instance.save()
    messages.add_message(request, messages.SUCCESS, 'Order accepted.')
    return redirect('store:order_view')

@login_required
@require_POST
@permission_required("store.update_ordertransaction", raise_exception=True)
def pay_balance(request, pk):
    customer = get_object_or_404(User, pk=pk)
    unpaid_orders = OrderTransaction.objects.filter(customer=customer).filter(is_paid=False)
    if request.method == "POST":
        for instance in unpaid_orders:
            instance.is_paid = True
            instance.save()
            messages.add_message(request, messages.SUCCESS, '%s paid balance successfully. Thank you!'%(customer.username))
        return redirect('store:customer_details', customer.pk)

@login_required
@require_POST
@permission_required("store.update_ordertransaction", raise_exception=True)
def pay_order(request, order_id, *args, **kwargs):
    instance = get_object_or_404(OrderTransaction, order_id=order_id)
    if request.method == "POST":
        instance.is_paid = True
        instance.save()
        messages.add_message(request, messages.SUCCESS, 'Order paid successfully.')
        return redirect('store:customer_details', instance.customer.pk)