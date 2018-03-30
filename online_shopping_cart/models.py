from django.db import models


class Items(models.Model):
    """  To save items """

    product_name = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    quantity = models.IntegerField()
    picture = models.ImageField(null=True, blank=True, upload_to='images/')
    description = models.TextField()

    def __str__(self):
        return self.product_name


class Information(models.Model):
    """ For saving Shipping information"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email=models.EmailField(default="")
    contact_no = models.CharField(max_length=50)
    full_address = models.CharField(max_length=50)
    zipcode = models.IntegerField()

    def __str__(self):
        return self.first_name
