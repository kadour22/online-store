from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model) :
    user       = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name       = models.CharField(max_length=200, null=True)
    email      = models.CharField(max_length=200 , unique=True)
    phone      = models.CharField(max_length=200, null=True)
    adress     = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

class Discount(models.Model):
    code       = models.CharField(max_length=200, unique=True)
    percent    = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.amount}"

class Category(models.Model):
    name       = models.CharField(max_length=200 , unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name       = models.CharField(max_length=200)
    price      = models.DecimalField(max_digits=7, decimal_places=2)
    image      = models.ImageField(null=True, blank=True)
    about      = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category   = models.ForeignKey(Category, on_delete=models.CASCADE , related_name="products" , null=True)

    def get_discount_price(self):
        return self.price - (self.price * (self.discount.percent / 100))
    
    def __str__(self):
        return self.name

class CartItem(models.Model) :
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer   = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="items")
    quantity   = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"    

class Order(models.Model) :
    customer   = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items      = models.ManyToManyField(CartItem , related_name="order")
    created_at = models.DateTimeField(auto_now_add=True)
    complete   = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.name} - {self.created_at}"


class Shipping(models.Model):
    customer   = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order      = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    adress     = models.CharField(max_length=200)
    city       = models.CharField(max_length=200)
    state      = models.CharField(max_length=200)
    zipcode    = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.adress}"
