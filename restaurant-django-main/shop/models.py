from django.db import models
from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect



# shop/models.py
from django.shortcuts import render

def admin_dashboard(request):
    total_products = Product.objects.count()
    total_orders = Orders.objects.count()
    total_users = User.objects.count()
    total_ratings = Rating.objects.count()

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users,
        'total_ratings': total_ratings,
    }
    
    return render(request, 'shop/admin_dashboard.html', context)


from django.db import models

# Move import here if you need to use OrderUpdate later in the same file

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=200)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")
    average_rating = models.FloatField(default=0.0)  # Change 'rating' to 'average_rating'
    total_ratings = models.IntegerField(default=0)  # Total ratings given

    def __str__(self):
        return self.product_name
    

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ('product', 'user')  # Ensure one rating per user per product


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


from django.db import models
from django.utils import timezone

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)  # JSON string for items
    userId = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Use DecimalField for currency
    name = models.CharField(max_length=90)
    email = models.EmailField(max_length=111)  # Use EmailField for better validation
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111, default="")
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.order_id} by {self.name}"


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.update_desc

