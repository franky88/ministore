from django.shortcuts import render, get_object_or_404, redirect
from store.models import OrderTransaction, Customer
from store.cartitem import Cart
from django.views.decorators.http import require_POST
from django.db.models import Sum, F


@require_POST
def add_customer_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        customer = Customer(
            name=name,
            contact=contact
        )
        customer.save()
        return redirect('store:pos_view')

def customer_view(request):
    customers = Customer.objects.all()
    cart = Cart(request)
    cart_items = cart.__len__()
    context = {
        'title': 'customers',
        'customers': customers,
        'cart_items': cart_items
    }
    return render(request, 'customer_view.html', context)

def customer_detail_view(request, customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)
    unpaid_orders = OrderTransaction.objects.filter(customer=customer).filter(is_paid=False)
    total_unpaid_orders = unpaid_orders.aggregate(total_unpaid=(Sum(F('price') * F('quantity'))))
    cart = Cart(request)
    cart_items = cart.__len__()
    context = {
        'title': 'customer details',
        'customer': customer,
        'cart_items': cart_items,
        'unpaid_orders': unpaid_orders,
        'total_unpaid_orders': total_unpaid_orders['total_unpaid']
    }
    return render(request, 'customer_detail_view.html', context)