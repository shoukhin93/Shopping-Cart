from django import forms
from online_shopping_cart.models import Items, UserInformation, Voucher, ShippingInfo
from django.core.exceptions import ValidationError
import math
from django.contrib.auth.models import User


class AddItems(forms.ModelForm):
    class Meta:
        model = Items
        fields = ('product_name', 'price', 'quantity', 'picture', 'description',)

    def clean_price(self):

        price = self.cleaned_data['price']
        try:

            price = float(price)
            price = (math.ceil(price * 100) / 100)  # Rounding into 2 floating points
        except ValueError:
            raise ValidationError("Invalid Price")

        return price

    def clean_quantity(self):

        quantity = self.cleaned_data['quantity']
        try:
            int(quantity)
        except ValueError:
            raise ValidationError("Invalid Quantity")

        return quantity


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class UserInformationForm(forms.ModelForm):
    class Meta:
        model = UserInformation
        fields = ('first_name', 'last_name', 'contact_no', 'full_address', 'zipcode',)


class ShippingInfoForm(forms.ModelForm):
    class Meta:
        model = ShippingInfo
        fields = ('v_id', 'username', 'total_price', 'time',)


class VoucherForm(forms.ModelForm):
    class Meta:
        model = Voucher
        fields = ('v_id', 'product_id', 'quantity', 'price', 'payment',)
