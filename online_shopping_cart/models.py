from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Items(models.Model):
    """  To save items """

    product_name = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    quantity = models.IntegerField()
    picture = models.ImageField(null=True, blank=True, upload_to='images/')
    description = models.TextField()

    def __str__(self):
        return self.product_name


class UserInformation(models.Model):
    """ For saving User registration information"""

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=50)
    full_address = models.CharField(max_length=50)
    zipcode = models.IntegerField()

    def __str__(self):
        return self.first_name


class ShippingInfo(models.Model):
    """ For saving User Shipping information"""

    username = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    total_price = models.FloatField(default=0)
    payment_status = models.CharField(default="Pending", max_length=10)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username.username


class Voucher(models.Model):
    """ For saving User Voucher information"""

    v_id = models.ForeignKey(ShippingInfo, on_delete=models.CASCADE, default=0)
    product_id = models.ForeignKey(Items, on_delete=models.CASCADE, default=0)
    quantity = models.IntegerField()
    price = models.FloatField(default=0)

    def __str__(self):
        return self.v_id.username.username
