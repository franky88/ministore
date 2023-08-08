from django.shortcuts import render, get_object_or_404, redirect
from store.models import ItemRequest, Product
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from store.cartitem import Cart
# from django.db.models import Sum, F


@login_required
@permission_required('store.view_itemrequest', raise_exception=True)
def item_request_view(request):
    item_request = ItemRequest.objects.filter(is_noted=True)

    cart = Cart(request)
    cart_items = cart.__len__()

    context = {
        'title': 'request items',
        'item_request': item_request,
        'cart_items': cart_items
    }
    return render(request, 'item_request_view.html', context)

@login_required
@require_POST
def request_item(request):
    if request.method == "POST":
        item_name = request.POST.get('itemName')
        message = request.POST.get('message')

        req = ItemRequest(
            request_by = request.user,
            item_name = item_name,
            message = message
        )
        req.save()
        return redirect('store:product_view')

@login_required
@require_POST
def request_product_restock(request, pk):
    product = get_object_or_404(Product, pk=pk)
    message = "Please restock this product. Thank you!"
    if request.method == "POST":
        req = ItemRequest(
            request_by = request.user,
            item_name = product.name,
            message = message
        )
        req.save()
        return redirect('store:product_view')

# @require_POST
# def noted_all_request(request):
#     all_request = ItemRequest.objects.filter(is_noted=False)
#     for req in all_request:
#         req.is_noted = True
#         print(req.is_noted)
#     # if request.method == "POST":
#     #     for req in all_request:
#     #         req.is_noted = True
#     #         print(req.is_noted)
#         # return redirect('store:product_view')

@login_required
@require_POST
@permission_required("store.update_itemrequest", raise_exception=True)
def request_status_update(request, pk):
    req = get_object_or_404(ItemRequest, pk=pk)
    print(req.is_noted)
    if request.method == "POST":
        req.is_noted = True
        print(req.is_noted)
        req.save()
        return redirect('store:product_view')
    

@login_required
def delete_request(request, pk):
    item_request = get_object_or_404(ItemRequest, pk=pk)
    print(item_request.request_by)
    if request.user.is_superuser or request.user == item_request.request_by:
        item_request.delete()
    else:
        messages.add_message(request, messages.DANGER, 'Access denied!')
    return redirect('store:product_view')