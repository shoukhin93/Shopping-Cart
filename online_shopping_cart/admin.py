from django.contrib import admin
from online_shopping_cart.models import Items, UserInformation, ShippingInfo, Voucher

# Register your models here.
admin.site.register(Items)
admin.site.register(UserInformation)
admin.site.register(ShippingInfo)
admin.site.register(Voucher)
