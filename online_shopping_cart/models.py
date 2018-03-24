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
