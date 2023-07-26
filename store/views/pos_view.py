from django.shortcuts import render, get_object_or_404, redirect
from store.cartitem import Cart
from store.models import Product, Customer, OrderTransaction
from django.views.decorators.http import require_POST
from store.forms.customer_form import CustomerForm
from django.contrib import messages


# Create your views here.
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

@require_POST
def cart_updated(request, bar_code):
    number = None
    cart = Cart(request)
    if request.method == 'POST':
        number = int(request.POST.get('number'))
    product = get_object_or_404(Product, bar_code=bar_code)
    cart.add(product=product, quantity=number, update_quantity=True)
    return redirect('store:pos_view')

@require_POST
def order_transaction(request):
    cart = Cart(request)
    if request.method == 'POST':
        customer = request.POST.get('customer_01')
        cus = get_object_or_404(Customer, name=customer)
        is_paid = request.POST.get('is_paid')
        if is_paid == None:
            paid = False
        else:
            paid = True
        for item in cart:
            order = OrderTransaction.objects.create(
                customer = cus,
                product = item['product'],
                price = item['price'],
                quantity = item['quantity'],
                total_amount = cart.get_total_price(),
                is_paid = paid
            )
            order.product.quantity -= order.quantity
            order.product.save()
            order.save()
            url = "orders/details/%s"%(order.order_id)
            messages.add_message(request, messages.SUCCESS, 'Your order successfully posted. <a href="%s">View order</a>'%(url))
        cart.clear()
        return redirect('store:pos_view')