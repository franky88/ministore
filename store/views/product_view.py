from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product, Category, ItemRequest
from store.forms.product_form import ProductForm
from store.cartitem import Cart
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count, F

# @require_POST
def product_view(request):
    form = ProductForm(request.POST or None)
    products = Product.objects.all()
    categories = Category.objects.all()
    all_requests = ItemRequest.objects.all()
    # total_product_category = categories.aggregate(total_count=Count('product__id'))
    
    cart = Cart(request)
    cart_items = cart.__len__()
    
    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        if form.is_valid():
            obj = form.save(commit=False)
            obj.bar_code = barcode
            obj.user = request.user
            obj.save()
            return redirect('store:product_view')
        
    context = {
        "title": "add product",
        "form": form,
        "products": products,
        "cart_items": cart_items,
        "categories": categories,
        "all_requests": all_requests
    }
    return render(request, 'product_view.html', context)

def add_product(request):
    form = ProductForm(request.POST or None)

    cart = Cart(request)
    cart_items = cart.__len__()

    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        if form.is_valid():
            obj = form.save(commit=False)
            obj.bar_code = barcode
            obj.user = request.user
            obj.save()
            return redirect('store:product_view')

    context = {
        "title": "add product",
        "form": form,
        "cart_items": cart_items
    }
    return render(request, 'add_product_view.html', context)

def delete_product(request, pk):
    instance = get_object_or_404(Product, pk=pk)
    instance.delete()
    return redirect('store:product_view')