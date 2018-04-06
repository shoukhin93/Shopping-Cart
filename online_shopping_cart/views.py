from django.shortcuts import render, redirect
from online_shopping_cart.forms import AddItems, UserInformationForm, UserRegistrationForm
from online_shopping_cart.models import Items, UserInformation, ShippingInfo, Voucher
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import collections
from django.contrib.auth.decorators import login_required


def index(request):
    items = Items.objects.all()
    total_price = calculate_cart_items(request)
    cart_items = request.session.get('items', [])
    return render(request, 'index.html', context={'items': items, 'cart_item': cart_items,
                                                  'total_price': total_price["total_price"]})


@login_required
def admin_panel(request):
    if request.method == 'POST':
        form = AddItems(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, form.errors)
        return HttpResponseRedirect(reverse('adminPanel'))

    return render(request, 'admin_panel.html')


@login_required
def edit_item(request, id):
    """ To Edit Item from database(Admin privilege required)"""

    item = Items.objects.get(id=id)

    if request.method == "POST":
        updated_info = AddItems(request.POST, request.FILES)

        if updated_info.is_valid():
            AddItems(request.POST, request.FILES, instance=item).save()
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'edit_item.html', context={'item': item})


@login_required
def delete_item(request, id):
    """ To Delete Item from database(Admin privilege required)"""

    Items.objects.get(id=id).delete()  # Deleting objects

    # clearing sessions
    request.session['items'] = []

    return HttpResponseRedirect(reverse('index'))


def calculate_cart_items(request):
    """ To Calculate cart items and their price"""

    cart_item_ids = request.session.get('items', [])

    # Gathering duplicate elements into key, occurrences  pair
    cleaned_cart_items = collections.Counter(cart_item_ids)

    cart_items = []
    total_price = 0.00

    for key, value in cleaned_cart_items.items():
        # Getting the saved item from database
        temp_item = Items.objects.get(id=key)

        quantity = value
        temp_price = temp_item.price * quantity  # total Price of a single item = quantity * price
        total_price += temp_price  # Total shopping price

        cart_items.append(
            {'id': key, 'product_name': temp_item.product_name, 'price': temp_item.price, 'quantity': quantity,
             'picture': temp_item.picture.url,
             'total': temp_price})

    return {'cart_items': cart_items, 'total_price': total_price}


def product_summary(request):
    """To view the cart items which are stored in session"""

    temp_value = calculate_cart_items(request)

    return render(request, 'product_summary.html',
                  context={'cart_items': temp_value["cart_items"], 'total_price': temp_value["total_price"]})


def add_cart_item(request):
    """ To add cart item and save to session """

    if request.method == 'POST':
        id = int(request.POST['cart_item_id'])
        items = request.session.get('items', [])
        items.append(id);
        request.session['items'] = items

    return HttpResponseRedirect(reverse('index'))


def remove_cart_item(request, id):
    """To remove cart item from session"""

    updated_cart_items = request.session.get('items', [])

    # Removing duplicate items from session which are matched with passed id
    updated_cart_items = [x for x in updated_cart_items if x != id]
    request.session['items'] = updated_cart_items

    return HttpResponseRedirect(reverse('product_summary'))


def remove_all_cart_items(request):
    """To remove all carts from session"""

    request.session['items'] = []
    return HttpResponseRedirect(reverse('product_summary'))


def user_registration(request):
    """ To register a user and save his information """

    if request.method == "POST":
        registration_form = UserRegistrationForm(data=request.POST)
        user_information = UserInformationForm(data=request.POST)

        if registration_form.is_valid() and user_information.is_valid():

            # Registering user
            user = registration_form.save()
            user.set_password(user.password)
            user.save()

            # Saving Registered User data
            temp = user_information.save(commit=False)
            temp.user_id = user
            temp.save()

        else:
            messages.error(request, registration_form.errors)

            # for message in messages:
            print(registration_form.errors)
            print(user_information.errors)

        return HttpResponseRedirect(reverse('product_summary'))

    return render(request, 'product_summary.html')


def add_shopping_info(request):
    """ To save shopping info """

    username = request.user
    current_cart_info = calculate_cart_items(request)
    total_price = current_cart_info['total_price']

    # Saving Shipping info summary
    shipping_info = ShippingInfo(username=username, total_price=total_price)
    shipping_info.save()

    # Saving shipping info details
    cart_items = current_cart_info['cart_items']

    for cart_item in cart_items:
        print(cart_item['id'])
        product_id = Items.objects.get(id=cart_item['id'])
        voucher_item = Voucher(v_id=shipping_info, product_id=product_id, quantity=cart_item['quantity'],
                               price=cart_item['quantity'] * product_id.price)
        voucher_item.save()

    return render(request, 'index.html')


def confirm_shipping_info(request):
    """ To save confirmed shopping info """

    temp_value = calculate_cart_items(request)

    return render(request, 'confirm_shipping_order.html',
                  context={'cart_items': temp_value["cart_items"], 'total_price': temp_value["total_price"]})


@login_required
def shipping_history(request):
    shipping_information = ShippingInfo.objects.all()
    return render(request, 'shipping_history.html', context={'shipping_information': shipping_information})


@login_required
def approve_shipping_info(request, id):
    """ To approve the pending status"""

    info = ShippingInfo.objects.get(id=id)
    info.payment_status = "approved"
    info.save()

    shipping_information = ShippingInfo.objects.all()
    return render(request, 'shipping_history.html', context={'shipping_information': shipping_information})
    #return HttpResponseRedirect(reverse('product_summary'))
