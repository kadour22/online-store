from django.contrib import admin
from .models import *


admin.site.register(Customer)
# admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Category)