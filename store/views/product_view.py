from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product, Category, ItemRequest
from store.forms.product_form import AddProductForm, UpdateProductForm
from store.cartitem import Cart
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count, F
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# @require_POST
def product_view(request):
    form = AddProductForm(request.POST or None)
    products = Product.objects.all()
    categories = Category.objects.annotate(count=Count('product__id'))
    all_requests = ItemRequest.objects.all()
    # total_product_category = categories.aggregate(total_count=Count('product__id'))
    query = request.GET.get('q')
    
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
        
    if query:
        products = products.filter(
        Q(bar_code__icontains=query) |
        Q(created__date__icontains=query) |
        Q(name__icontains=query) |
        Q(category__name__icontains=query)
        )
    
    breadcrumbs_link = ""
    if query:
        breadcrumbs_link = query
    else:
        breadcrumbs_link = "All Tasks"

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "title": "add product",
        "form": form,
        "products": products,
        "cart_items": cart_items,
        "categories": categories,
        "all_requests": all_requests,
        "breadcrumbs_link": breadcrumbs_link,
        "page_obj": page_obj,
    }
    return render(request, 'product_view.html', context)

def add_product(request):
    form = AddProductForm(request.POST or None, request.FILES or None)

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

def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = UpdateProductForm(request.POST or None, request.FILES or None, instance=product)

    cart = Cart(request)
    cart_items = cart.__len__()

    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('store:product_view')
    
    context = {
        "title": "update product",
        "form": form,
        "cart_items": cart_items,
        "product": product
    }

    return render(request, 'update_product_view.html', context)

def delete_product(request, pk):
    instance = get_object_or_404(Product, pk=pk)
    instance.delete()
    return redirect('store:product_view')