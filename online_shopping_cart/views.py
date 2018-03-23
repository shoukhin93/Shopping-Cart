from django.shortcuts import render, redirect
from online_shopping_cart.forms import AddItems
from online_shopping_cart.models import Items
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.

def admin_panel(request):
    if request.method == 'POST':
        form = AddItems(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminPanel')
        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect(reverse('adminPanel'))

    return render(request, 'admin_panel.html')


def test(request):
    items = Items.objects.all()
    return render(request, 'test.html', context={'items': items})
