import sqlite3
from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product, Category, ItemRequest
from store.forms.product_form import AddProductForm, UpdateProductForm, ProductTransactionForm
from store.cartitem import Cart
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count, F
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

# @require_POST

@login_required
def product_view(request):
    # print("sqliteversion", sqlite3.sqlite_version)
    form = AddProductForm(request.POST or None)
    if request.user.is_superuser:
        products = Product.objects.all()
        categories = Category.objects.annotate(count=Count('product__id'))
    else:
        products = Product.objects.filter(on_display=True)
        categories = Category.objects.filter(product__on_display=True).annotate(count=Count('product__id'))
    all_requests = ItemRequest.objects.all()
    # total_product_category = categories.aggregate(total_count=Count('product__id'))
    product_transaction_form = ProductTransactionForm(request.POST or None)
    query = request.GET.get('q')
    
    cart = Cart(request)
    cart_items = cart.__len__()
    
    if request.method == 'POST':
        if product_transaction_form.is_valid():
            obj = product_transaction_form.save(commit=False)
            obj.user = request.user
            obj.product.quantity += obj.quantity
            if obj.cost:
                obj.product.cost = obj.new_cost
            else:
                obj.cost = obj.product.cost
            obj.product.save()
            obj.save()
            return redirect('store:product_view')

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
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
        "product_transaction_form": product_transaction_form,
        "query": query
    }
    return render(request, 'product_view.html', context)

@login_required
@permission_required("store.add_product", raise_exception=True)
def add_stock_quantity(request):
    product_transaction_form = ProductTransactionForm(request.POST or None)

    cart = Cart(request)
    cart_items = cart.__len__()

    if request.method == 'POST':
        if product_transaction_form.is_valid():
            obj = product_transaction_form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('store:product_view')
    context = {
        "title": "add product",
        "product_transaction_form": product_transaction_form,
        "cart_items": cart_items
    }
    print(dir(Product.objects))
    return render(request, 'add_product_view.html', context)

@login_required
@permission_required("store.update_product", raise_exception=True)
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

@login_required
@permission_required("store.delete_product", raise_exception=True)
def delete_product(request, pk):
    instance = get_object_or_404(Product, pk=pk)
    instance.delete()
    return redirect('store:product_view')

@login_required
@require_POST
@permission_required("store.update_product", raise_exception=True)
def publish_unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        if product.on_display:
            product.on_display = False
            product.save()
        else:
            product.on_display = True
            product.save()
        print(product.on_display)
        if product.on_display:
            messages.add_message(request, messages.SUCCESS, 'Product published successfully.')
        else:
            messages.add_message(request, messages.SUCCESS, 'Product unpublished successfully.')
        return redirect('store:product_view')
