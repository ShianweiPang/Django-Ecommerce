from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    username = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return self.email
    

class Product(models.Model):
    name =models.CharField(max_length=30)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    # OOP programming, making it as an attribute of the object
    # It also allows getter setter and deleters method
    # https://www.youtube.com/watch?v=jCzT9XFZ5bw
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    cart_complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=30, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total_price(self):
        order_products = self.order_product_set.all()
        total_price = sum([order_product.get_total for order_product in order_products])
        return total_price

    @property
    def get_total_quantity(self):
        order_products = self.order_product_set.all()
        total_quantity = sum([order_product.quantity for order_product in order_products])
        return total_quantity

    @property
    def shipping(self):
        shipping = False
        order_products = self.order_product_set.all()
        for order_product in order_products:
            if order_product.product.digital==False:
                shipping = True
                break
        return shipping


class Order_Product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_ordered = models.TimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total 

class Shipping(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address =models.CharField(max_length=30)
    city =models.CharField(max_length=30)
    state =models.CharField(max_length=30)
    zipcode =models.CharField(max_length=30)

    def __str__(self):
        return self.address