from django.shortcuts import render, redirect
from online_shopping_cart.forms import AddItems, UserInformationForm, UserRegistrationForm
from online_shopping_cart.models import Items, UserInformation, ShippingInfo, Voucher
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import collections
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout


def index(request):
    items = Items.objects.all()
    total_price = calculate_cart_items(request)
    cart_items = request.session.get('items', [])
    return render(request, 'index.html', context={'items': items, 'cart_item': cart_items,
                                                  'total_price': total_price["total_price"]})


@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
def edit_item(request, id):
    """ To Edit Item from database(Admin privilege required)"""

    item = Items.objects.get(id=id)

    if request.method == "POST":
        updated_info = AddItems(request.POST, request.FILES)

        if updated_info.is_valid():
            AddItems(request.POST, request.FILES, instance=item).save()
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'edit_item.html', context={'item': item})


@user_passes_test(lambda u: u.is_superuser)
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

        # print(key)
        try:
            temp_item = Items.objects.get(id=key)
        except ObjectDoesNotExist:
            continue

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


def update_cart_items(request, id):
    """ TO update cart items"""

    if request.method == "POST":
        amount = int(request.POST['amount'])
        if amount >= 0:
            # First removing the cart items and then appending to the list
            cart_items = request.session.get('items', [])

            # Removing duplicate items from session which are matched with passed id
            updated_cart_items = [x for x in cart_items if x != id]

            # updated amount of cart item is appending to the list
            for i in range(0, amount):
                updated_cart_items.append(id)

            request.session['items'] = updated_cart_items  # Updating session

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
        product_id = Items.objects.get(id=cart_item['id'])
        voucher_item = Voucher(v_id=shipping_info, product_id=product_id, quantity=cart_item['quantity'],
                               price=cart_item['quantity'] * product_id.price)
        voucher_item.save()

        # Updating quantity after confirming order
        # product_id.quantity -= int(cart_item['quantity'])
        # product_id.save()

    return HttpResponseRedirect('/')


def confirm_shipping_info(request):
    """ To save confirmed shopping info """

    error_messages = []
    flag = True
    temp_value = calculate_cart_items(request)
    cart_items = temp_value['cart_items']

    for cart_item in cart_items:
        id = cart_item['id']

        try:
            temp_item = Items.objects.get(id=id)
        except ObjectDoesNotExist:
            continue

        if temp_item.quantity < cart_item['quantity']:
            error_messages.append("Not enough " + temp_item.product_name + " in our store")
            flag = False

    if flag:
        return render(request, 'confirm_shipping_order.html',
                      context={'cart_items': temp_value["cart_items"], 'total_price': temp_value["total_price"]})

    else:
        return render(request, 'product_summary.html',
                      context={'cart_items': temp_value["cart_items"], 'total_price': temp_value["total_price"],
                               'error_messages': error_messages})


@user_passes_test(lambda u: u.is_superuser)
def shipping_history(request):
    shipping_information = ShippingInfo.objects.all()
    return render(request, 'shipping_history.html', context={'shipping_information': shipping_information})


@user_passes_test(lambda u: u.is_superuser)
def approve_shipping_info(request, id):
    """ To approve the pending status"""

    info = ShippingInfo.objects.get(id=id)

    # Updating stored quantity
    vouchers = info.voucher_set.all()
    for voucher in vouchers:
        temp_item = voucher.product_id
        temp_item.quantity -= voucher.quantity
        if temp_item.quantity >= 0:
            temp_item.save()
        else:
            error = "Sorry, not enough stock for " + temp_item.product_name
            shipping_information = ShippingInfo.objects.all()
            return render(request, 'shipping_history.html',
                          context={'shipping_information': shipping_information, 'errors': error})

    # No error found, change the payment status
    info.payment_status = "approved"
    info.save()

    return HttpResponseRedirect('/shipping_history/')


@user_passes_test(lambda u: u.is_superuser)
def reject_payment_status(request, id):
    """ To reject the pending status"""

    info = ShippingInfo.objects.get(id=id)
    info.delete()

    return HttpResponseRedirect('/shipping_history/')


@user_passes_test(lambda u: u.is_superuser)
def show_voucher_information(request, id):
    """ To show the voucher details information """

    shipping_information = ShippingInfo.objects.get(id=id)
    return render(request, 'voucher_info.html', context={'shipping_information': shipping_information})


def search_result(request):
    search_string = request.POST['search_string']

    items = Items.objects.filter(product_name__icontains=search_string)
    total_price = calculate_cart_items(request)
    cart_items = request.session.get('items', [])
    return render(request, 'index.html', context={'items': items, 'cart_item': cart_items,
                                                  'total_price': total_price["total_price"]})


def login_or_register(request):
    return render(request, 'login_or_register.html')


def user_login(request):
    """ To login general user"""

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect('/confirm_shipping_info/')
        else:
            messages.error(request, "invalid username or password")
            return HttpResponseRedirect('/login_or_register/')


def user_logout(request):
    """ TO logged out logged in user """
    logout(request)
    return HttpResponseRedirect('/')
