from django.shortcuts import render, get_object_or_404, redirect
from store.models import ItemRequest, Product
from django.views.decorators.http import require_POST
# from django.db.models import Sum, F

@require_POST
def request_item(request):
    if request.method == "POST":
        request_by = request.POST.get('requester')
        item_name = request.POST.get('itemName')
        message = request.POST.get('message')

        req = ItemRequest(
            request_by = request_by,
            item_name = item_name,
            message = message
        )
        req.save()
        return redirect('store:product_view')

@require_POST
def request_product_restock(request, pk):
    product = get_object_or_404(Product, pk=pk)
    message = "Please restock this product. Thank you!"
    if request.method == "POST":
        request_by = request.POST.get('requestBy')
        req = ItemRequest(
            request_by = "Someone",
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

@require_POST
def request_status_update(request, pk):
    req = get_object_or_404(ItemRequest, pk=pk)
    print(req.is_noted)
    if request.method == "POST":
        req.is_noted = True
        print(req.is_noted)
        req.save()
        return redirect('store:product_view')
    

def delete_request(request, pk):
    item_request = get_object_or_404(ItemRequest, pk=pk)
    item_request.delete()
    return redirect('store:product_view')