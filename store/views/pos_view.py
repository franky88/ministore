from django.shortcuts import render, get_object_or_404, redirect
from store.cartitem import Cart
from store.models import Product


# Create your views here.
def product_order_view(request):
    products = Product.objects.all()
    context={
        "title": "product view",
        "products": products
    }
    return render(request, 'pos_view.html', context)

def add_order_view(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    cart.add(product=product, quantity=1, update_quantity=False)
    return redirect('store:pos_view')