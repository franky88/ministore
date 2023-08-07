from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# @login_required()
# @permission_required("store.add_user", raise_exception=True)
# def add_user(request):
#     form = UserCreationForm(request.POST or None)
#     if request.method == "POST":
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.save()
#             messages.add_message(request, messages.SUCCESS,
#                                  'User successfully created name: %s.' % (instance.username.title()))
#             return redirect('store:product_view')
#     else:
#         form = UserCreationForm(request.POST or None)
#     context = {
#         'title': 'add user',
#         'form': form
#     }
#     return render(request, 'registration/register_user.html', context)

def register_user(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.add_message(request, messages.SUCCESS, 'User successfully created name: %s.' % (instance.username.title()))
            return redirect('login')
    else:
        form = UserCreationForm(request.POST or None)
    context = {
        'title': 'registration',
        'form': form
    }
    return render(request, 'registration/register_user.html', context)