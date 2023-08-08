from django.shortcuts import render, get_object_or_404, redirect
from store.cartitem import Cart
from store.models import Product, Customer, OrderTransaction, CustomerOrder
from django.views.decorators.http import require_POST
from store.forms.customer_form import CustomerForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def product_order_view(request):
    products = Product.objects.all()
    cart = Cart(request)
    customers = Customer.objects.all()
    cart_items = cart.__len__()
    for item in cart:
        item['update_quantity_form'] = {'quantity': item['quantity'], 'update': True}
    context={
        "title": "product view",
        "products": products,
        "cart": cart,
        "cart_items": cart_items,
        "customers": customers
    }
    return render(request, 'pos_view.html', context)

@login_required
def add_order_view(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    # if product.quantity < 1:
    #     pass
    cart.add(product=product, quantity=1, update_quantity=False)
    return redirect('store:product_view')

def clear_cart_items(request):
    cart = Cart(request)
    cart.clear()
    return redirect('store:pos_view')

@login_required
@require_POST
def cart_updated(request, bar_code):
    number = None
    cart = Cart(request)
    if request.method == 'POST':
        number = int(request.POST.get('number'))
    product = get_object_or_404(Product, bar_code=bar_code)
    if number > product.quantity:
        messages.add_message(request, messages.WARNING, 'Quantity not grater than %s.'%(product.quantity))
    cart.add(product=product, quantity=number, update_quantity=True)
    return redirect('store:pos_view')

@login_required
@require_POST
def remove_cart_item(request, bar_code):
    cart = Cart(request)
    product = get_object_or_404(Product, bar_code=bar_code)
    cart.remove(product=product)
    messages.add_message(request, messages.SUCCESS, 'Item removed successfully.')
    return redirect('store:pos_view')

@login_required
@require_POST
def order_transaction(request):
    cart = Cart(request)
    if request.method == 'POST':
        for item in cart:
            order = OrderTransaction(
                customer = request.user,
                product = item['product'],
                price = item['price'],
                quantity = item['quantity'],
                total_amount = cart.get_total_price(),
            )
            if order.product.quantity < order.quantity:
                messages.add_message(request, messages.WARNING, 'Quantity not grater than %s.'%(order.product.quantity))
                return redirect('store:pos_view')
            order.product.quantity -= order.quantity
            order.product.save()
            order.save()
        messages.add_message(request, messages.SUCCESS, 'Your order successfully posted.')
        cart.clear()
        return redirect('store:pos_view')