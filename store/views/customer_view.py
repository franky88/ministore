from django.shortcuts import render, get_object_or_404, redirect
from store.models import OrderTransaction, Customer
from django.contrib.auth.models import User
from store.cartitem import Cart
from django.views.decorators.http import require_POST
from django.db.models import Sum, F, Q
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import messages

# @login_required
# @require_POST
# def add_customer_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         contact = request.POST.get('contact')
#         customer = Customer.objects.create(
#             name=name,
#             contact=contact
#         )
#         customer.save()
#         return redirect('store:pos_view')
    


@login_required
@permission_required("store.view_user", raise_exception=True)
def customer_view(request):
    customers_balance = User.objects.filter(Q(ordertransaction__is_paid=False), Q(ordertransaction__is_accepted=True)).annotate(total_balance=(Sum(F('ordertransaction__price') * F('ordertransaction__quantity'))))
    total_balance = customers_balance.aggregate(balance = Sum('total_balance'))
    customers = User.objects.all()
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.add_message(request, messages.SUCCESS,
                                 'User successfully created name: %s.' % (instance.username.title()))
            return redirect('store:customer_view')
    else:
        form = UserCreationForm(request.POST or None)

    cart = Cart(request)
    cart_items = cart.__len__()

    context = {
        'title': 'customers',
        'customers': customers,
        'customers_balance': customers_balance,
        'cart_items': cart_items,
        'total_balance': total_balance,
        'form': form,
    }
    return render(request, 'customer_view.html', context)

@login_required
@permission_required("store.view_user", raise_exception=True)
def customer_detail_view(request, pk):
    customer = get_object_or_404(User, pk=pk)
    unpaid_orders = OrderTransaction.objects.filter(customer=customer).filter(is_paid=False)
    total_unpaid_orders = unpaid_orders.aggregate(total_unpaid=(Sum(F('price') * F('quantity'))))
    form = UserChangeForm(request.POST or None, instance=customer)
    cart = Cart(request)
    cart_items = cart.__len__()

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
    
    context = {
        'title': 'customer details',
        'customer': customer,
        'cart_items': cart_items,
        'unpaid_orders': unpaid_orders,
        'total_unpaid_orders': total_unpaid_orders['total_unpaid'],
        'form': form,
    }
    return render(request, 'customer_detail_view.html', context)

# @login_required
# @permission_required("store.update_user", raise_exception=True)
# def update_customer(request, pk):
#     customer = get_object_or_404(User, pk=pk)
#     form = UserChangeForm(request.POST or None, instance=customer)

#     cart = Cart(request)
#     cart_items = cart.__len__()
#     # print(form)
    
#             return redirect('store:update_customer', pk=customer.pk)