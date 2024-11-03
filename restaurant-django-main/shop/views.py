from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse
from django.core.serializers import serialize
from django.http import JsonResponse

from .models import Product, Contact, Orders, OrderUpdate
from django.contrib.auth.models import User
from django.contrib import messages
from math import ceil
from django.contrib.auth import authenticate, login, logout
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
from .models import Product, Rating  # Make sure to import your models
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';   # Your-Merchant-Key-Here

# views.py
from .models import Product, Orders, OrderUpdate, Rating, Contact, User

from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderUpdate  # Import models here

def admin_order_updates(request):
    order_updates = OrderUpdate.objects.all()  # Retrieve all order updates
    return render(request, 'shop/admin_order_updates.html', {'order_updates': order_updates})

def edit_order_update(request, order_id):
    order_update = get_object_or_404(OrderUpdate, order_id=order_id)
    
    if request.method == 'POST':
        order_update.update_desc = request.POST['update_desc']
        order_update.timestamp = request.POST['timestamp']  # If you want to allow changing timestamp
        order_update.save()
        return redirect('admin_order_updates')  # Redirect to the order updates list

    return render(request, 'shop/edit_order_update.html', {'order_update': order_update})


def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    darshan = {'allProds': allProds}
    return render(request, 'shop/index.html', darshan)
    # return HttpResponse("<h1 align='center'> <font color='#FF0000' size='9' > Welcome Our Restaurant </font> </h1>")


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
        return render(request, 'shop/contact.html', {'thank': thank})
    return render(request, 'shop/contact.html', {'thank': thank})


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        name = request.POST.get('name', '')
        password = request.POST.get('password')
        user = authenticate(username=name, password=password)
        if user is not None:
            try:
                order = Orders.objects.filter(order_id=orderId, email=email)
                if len(order) > 0:
                    update = OrderUpdate.objects.filter(order_id=orderId)
                    updates = []
                    for item in update:
                        updates.append({'text': item.update_desc, 'time': item.timestamp})
                        response = json.dumps({"status": "success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                    return HttpResponse(response)
                else:
                    return HttpResponse('{"status":"noitem"}')
            except Exception as e:
                return HttpResponse('{"status":"error"}')
        else:
            return HttpResponse('{"status":"Invalid"}')
    return render(request, 'shop/tracker.html')


def orderView(request):
    if request.user.is_authenticated:
        current_user = request.user
        orderHistory = Orders.objects.filter(userId=current_user.id)
        if len(orderHistory) == 0:
            messages.info(request, "You have not ordered.")
            return render(request, 'shop/orderView.html')
        return render(request, 'shop/orderView.html', {'orderHistory': orderHistory})
    return render(request, 'shop/orderView.html')


def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.desc or query in item.product_name or query in item.category or query in item.desc.upper() or query in item.product_name.upper() or query in item.category.upper():
        return True
    else:
        return False

# views.py
from .models import Product, Rating
from django.contrib.auth.decorators import login_required

@login_required
def submit_rating(request, product_id):
    if request.method == "POST":
        score = int(request.POST['score'])
        product = get_object_or_404(Product, id=product_id)

        # Check if the user has already rated this product
        existing_rating = Rating.objects.filter(product=product, user=request.user).first()
        if existing_rating:
            existing_rating.score = score
            existing_rating.save()
        else:
            Rating.objects.create(product=product, user=request.user, score=score)

        # Update average rating
        product.total_ratings += 1
        product.average_rating = (product.average_rating * (product.total_ratings - 1) + score) / product.total_ratings
        product.save()

        return render(request, 'shop/rating_success.html', {'product': product})
    return render(request, 'shop/rate_product.html', {'product': product})  # Render rating form if not POST
# shop/views.py
# shop/views.py
# shop/views.py
# shop/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product  # Import your Product model
from django.shortcuts import render

@csrf_exempt  # Only for testing; ideally, you'd use proper CSRF tokens.
def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory', '')
        price = request.POST.get('price')
        description = request.POST.get('description')
        pub_date = request.POST.get('pub_date')
        image = request.FILES.get('image')
        average_rating = request.POST.get('average_rating', 0.0)
        total_ratings = request.POST.get('total_ratings', 0)

        try:
            # Create a new product instance
            product = Product(
                product_name=product_name,
                category=category,
                subcategory=subcategory,
                price=price,
                desc=description,
                pub_date=pub_date,
                image=image,
                average_rating=average_rating,
                total_ratings=total_ratings
            )
            product.save()

            return JsonResponse({'status': 'success', 'product': {
                'product_name': product.product_name,
                'category': product.category,
                'price': product.price,
            }})

        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)})

    # If not a POST request, render the product list page
    products = Product.objects.all()  # Assuming you want to render existing products
    return render(request, 'your_template_name.html', {'products': products})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
from django.shortcuts import get_object_or_404
from .models import Product
import logging

logger = logging.getLogger(__name__)




def update_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        logger.debug(f"Received product_name: {product_name}")

        if not product_name:
            logger.error("Product name cannot be empty.")
            return JsonResponse({'status': 'error', 'message': 'Product name cannot be empty.'}, status=400)

        try:
            product = Product.objects.get(product_name=product_name)
            logger.debug(f"Product found: {product}")

            # Update product fields
            product.category = request.POST.get('category')
            product.subcategory = request.POST.get('subcategory')
            product.price = float(request.POST.get('price'))
            product.pub_date = datetime.strptime(request.POST.get('pub_date'), '%Y-%m-%d')
            product.description = request.POST.get('description')
            product.average_rating = request.POST.get('average_rating')
            product.total_ratings = request.POST.get('total_ratings')

            # Handle image upload if present
            if 'image' in request.FILES:
                product.image = request.FILES['image']
                logger.debug("Image updated")
            product.save()

            return JsonResponse({'status': 'success', 'message': 'Product updated successfully.'})
        except Product.DoesNotExist:
            logger.error("Product not found")
            return JsonResponse({'status': 'error', 'message': 'Product not found.'})
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return JsonResponse({'status': 'error', 'message': 'An error occurred during product update.'}, status=500)

    logger.error("Invalid request method.")
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import OrderUpdate  # Adjust the import according to your model

@csrf_exempt
def update_order(request):
    if request.method == 'POST':
        update_id = request.POST.get('update_id')
        update_desc = request.POST.get('update_desc')

        # Validate input
        if not update_id or not update_desc:
            return JsonResponse({'status': 'error', 'message': 'Invalid input.'})

        try:
            order_update = OrderUpdate.objects.get(id=int(update_id))
            order_update.update_desc = update_desc
            order_update.save()

            return JsonResponse({'status': 'success', 'message': 'Order update successfully.'})
        except OrderUpdate.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Order update not found.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})






from django.shortcuts import render, get_object_or_404
from .models import Product

def edit_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'your_template.html', {'product': product})

# View to list products in the admin view
from django.http import JsonResponse
from .models import Product

def admin_product_list(request):
    # Query all products
    products = Product.objects.all()
    
    # Create a list to hold serialized product data
    products_list = []
    
    # Loop through each product and create a dictionary
    for product in products:
        products_list.append({
            'product_id': product.product_id,
            'product_name': product.product_name,
            'category': product.category,
            'subcategory': product.subcategory,
            'price': product.price,
            'desc': product.desc,
            'pub_date': product.pub_date.isoformat() if product.pub_date else None,  # Format date to string
            'image': product.image.url if product.image else None,  # Get image URL if available
            'average_rating': product.average_rating,
            'total_ratings': product.total_ratings,
        })
    
    # Return the list of products as a JSON response
    return JsonResponse(products_list, safe=False)  # Set safe=False for non-dict objects



def admin_dashboard(request):
    total_users = User.objects.count()
    total_orders = Orders.objects.count()
    total_products = Product.objects.count()
    total_ratings = Rating.objects.count()

    context = {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_products': total_products,
        'total_ratings': total_ratings,
    }
    return render(request, 'shop/admin_dashboard.html', context)
def admin_product_list(request):
    products = Product.objects.all()  # Replace this with your actual query
    return render(request, 'shop/admin_product_list.html', {'products': products})

from django.shortcuts import render
from .models import Orders
def admin_order_list(request):
    orders = Orders.objects.all()  # Retrieve all orders
    return render(request, 'shop/admin_order_list.html', {'orders': orders})


# views.py
# views.py
from django.shortcuts import redirect, get_object_or_404, render
from .models import OrderUpdate

def update_order(request):
    update_id = request.GET.get('update_id')
    order_update = get_object_or_404(OrderUpdate, pk=update_id)

    if request.method == 'POST':
        order_update.update_desc = request.POST.get('update_desc')
        order_update.save()
        return redirect('admin_order_updates')  # Replace with the correct URL name

    return render(request, 'shop/update_order.html', {'order_update': order_update})






def admin_rating_list(request):
    ratings = Rating.objects.all()  # Retrieve all ratings from the database
    return render(request, 'shop/admin_rating_list.html', {'ratings': ratings})

from django.contrib.auth.models import User
from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth.models import User

def admin_user_list(request):
    users = User.objects.all()  # Retrieve all users from the database
    user_list = [
        {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'active': user.is_active  # Assuming this indicates if the user is active
        }
        for user in users
    ]
    return render(request, 'shop/admin_user_list.html', {'users': user_list})


def admin_order_updates(request):
    order_updates = OrderUpdate.objects.all()  # Retrieve all order updates
    print(order_updates)  # Add this line to debug
    return render(request, 'shop/admin_order_updates.html', {'order_updates': order_updates})

def admin_contact_list(request):
    contacts = Contact.objects.all()  # Fetch all contacts from the database
    return render(request, 'shop/admin_contact_list.html', {'contacts': contacts})
def product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/prodView.html', {'product': product})
def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    darshan = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query) < 3:
        darshan = {'msg': "No item available. Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', darshan)


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        user_id = request.POST.get('user_id', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, userId=user_id, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The Order has been Placed")
        update.save()
        thank = True
        id = order.order_id

        # Send confirmation email
        send_confirmation_email(email, id)

        if 'onlinePay' in request.POST:
            # Request paytm to transfer the amount to your account after payment by user
            darshan_dict = {
                'MID': 'WorldP64425807474247',  # Your-Merchant-Id-Here
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',
            }
            darshan_dict['CHECKSUMHASH'] = Checksum.generate_checksum(darshan_dict, MERCHANT_KEY)
            return render(request, 'shop/paytm.html', {'darshan_dict': darshan_dict})
        elif 'cashOnDelivery' in request.POST:
            return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')

from django.core.mail import send_mail
from django.conf import settings

def send_confirmation_email(email, order_id):
    subject = 'Order Confirmation'
    message = f'Thank you for your order! Your order ID is {order_id}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, email_from, recipient_list)

from .models import Product, Rating
from .forms import RatingForm

def productView(request, myid):
    product = Product.objects.filter(id=myid).first()
    user_rating = None

    if request.method == "POST":
        if request.user.is_authenticated:
            form = RatingForm(request.POST)
            if form.is_valid():
                score = form.cleaned_data['score']
                # Create or update the rating
                rating, created = Rating.objects.get_or_create(product=product, user=request.user, defaults={'score': score})
                if not created:  # If the user already rated, update the score
                    rating.score = score
                    rating.save()
                # Update the product's average rating
                total_ratings = Rating.objects.filter(product=product).count()
                average_rating = Rating.objects.filter(product=product).aggregate(models.Avg('score'))['score__avg']
                product.rating = average_rating
                product.total_ratings = total_ratings
                product.save()
                messages.success(request, "Thank you for your rating!")
                return redirect('product_view', myid=myid)  # Redirect to avoid duplicate submission
        else:
            messages.warning(request, "You need to be logged in to rate a product.")

    # Get the user's existing rating
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(product=product, user=request.user).first()

    return render(request, 'shop/prodView.html', {'product': product, 'form': RatingForm(), 'user_rating': user_rating})

def handeLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "Invalid credentials! Please try again")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponse("404- Not found")


def handleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        email = request.POST['email1']
        phone = request.POST['phone']
        password = request.POST['password']
        password1 = request.POST['password1']

        # check for errorneous input
        if (password1 != password):
            messages.warning(request, " Passwords do not match")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        try:
            user = User.objects.get(username=username)
            messages.warning(request, " Username Already taken. Try with different Username.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except User.DoesNotExist:
            # Create the user
            myuser = User.objects.create_user(username=username, email=email, password=password)
            myuser.first_name = f_name
            myuser.last_name = l_name
            myuser.phone = phone
            myuser.save()
            messages.success(request, " Your Account has been successfully created")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse("404 - Not found")


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})
