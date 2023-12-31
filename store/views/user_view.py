from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import messages

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