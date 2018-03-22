from django.shortcuts import render, redirect
from online_shopping_cart.forms import AddItems


# Create your views here.

def adminPanel(request):
    if request.method == 'POST':
        form = AddItems(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminPanel')
    return render(request, 'admin_panel.html')
