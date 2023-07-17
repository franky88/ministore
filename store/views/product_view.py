from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product
from store.forms.product_form import ProductForm


def add_product(request):
    form = ProductForm(request.POST or None)
    products = Product.objects.all()
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('store:add_product')
    context = {
        "title": "add product",
        "form": form,
        "products": products
    }
    return render(request, 'add_product.html', context)

def delete_product(request, pk):
    instance = get_object_or_404(Product, pk=pk)
    instance.delete()
    return redirect('store:add_product')