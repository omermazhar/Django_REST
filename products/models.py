import random
from django.conf import settings
from django.db import models
from django.db.models import Q
from numpy import product

# auth.User

User = settings.AUTH_USER_MODEL


class Product(models.Model):

    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)
    public = models.BooleanField(default=False)

    def get_absolute_url(self):
        print(self)
        return f"/api/products/{self.pk}/"

    @property
    def endpoint(self):
        return self.get_absolute_url()

    @property
    def path(self):
        return f"/products/{self.pk}/"


    @property
    def sale_price(self):
        return "%.2f" % (float(self.price) * 0.8)

    @property
    def assigned_product(self):
        Product_Items = ['Tesla', 'Iphone', 'private jet', 'Macbook']
        return random.choice(Product_Items)

