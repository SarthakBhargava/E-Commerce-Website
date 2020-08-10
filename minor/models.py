from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, auth
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField(default="")
    category = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    offers = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    image_1 = models.ImageField(upload_to='images', null=True, blank=True)
    image_2 = models.ImageField(upload_to='images', null=True, blank=True)
    image_3 = models.ImageField(upload_to='images', null=True, blank=True)
    image_4 = models.ImageField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        ship = False
        orderItems = self.orderitems_set.all()
        for i in orderItems:
            if i.product.digital == False:
                ship = True
        return ship

    @property
    def get_cart_total(self):
        order_items = self.orderitems_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitems_set.all()
        total = sum([item.quantity for item in order_items])
        return total

class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order.id) + ' Items'

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=10, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    pincode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address