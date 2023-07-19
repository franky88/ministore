from store.models import Category
from django.shortcuts import render, get_object_or_404, redirect
from store.cartitem import Cart
from django.views.decorators.http import require_POST
from django.db.models import Sum, F


@require_POST
def add_category(request):
    category_name = request.POST.get('categoryName')
    if request.method == 'POST':
        category = Category(
            name = category_name,
        )
        category.save()
        return redirect('store:product_view')