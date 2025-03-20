from django.urls import path
from . import views

urlpatterns = [
    path("" , views.product_list , name="product_list"),
    path("product/<int:product_id>/" , views.product_detail , name="product"),
    path("products/<int:category_id>/" , views.products_by_category , name="products"),
    path("add-to-cart/<int:product_id>/" , views.add_to_cart , name="add-to-cart"),
    path("register/" , views.create_user_view , name="register"),
    path("login/" , views.login_user , name="login"),
    # 
]