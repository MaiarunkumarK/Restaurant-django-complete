from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import Product, Rating, Contact, Orders, OrderUpdate
from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderUpdate

def admin_order_updates(request):
    order_updates = OrderUpdate.objects.all()  # Retrieve all order updates
    return render(request, 'shop/admin_order_updates.html', {'order_updates': order_updates})
OrderUpdate.objects.create(order_id=1, update_desc="Order has been shipped.", timestamp="2024-11-01T12:00:00Z")

class OrderUpdateAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'update_desc', 'timestamp')
    list_filter = ['timestamp']

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'score')
    list_filter = ('product',)

from django.apps import AppConfig

class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'userId', 'name', 'email', 'timestamp')
    list_filter = ['timestamp']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'price')
    list_filter = ['category']
    search_fields = ['product_name']

from django.shortcuts import render
from .models import Product

def admin_product_list(request):
    products = Product.objects.all().values('product_id', 'product_name', 'category', 'subcategory', 'price', 'desc', 'pub_date', 'image', 'average_rating', 'total_ratings')
    return render(request, 'admin_product_list.html', {'products': products})


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'email', 'timestamp')
    list_filter = ['timestamp']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

# Custom UserAdmin to display additional fields
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_active',)

# Register your models with the admin site
admin.site.register(Product, ProductAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderUpdate, OrderUpdateAdmin)

# Unregister the default User admin
admin.site.unregister(User)
# Register the custom User admin
admin.site.register(User, CustomUserAdmin)

admin.site.site_header = "The Restaurant"
admin.site.index_title = "The Restaurant Administration"
admin.site.site_title = "The Restaurant Admin"
