from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import submit_rating, product_view  # Ensure product_view is imported
from .views import admin_order_updates, edit_order_update



urlpatterns = [
    path('product/rate/<int:product_id>/', submit_rating, name='submit_rating'),
    path('product/<int:product_id>/', product_view, name='product_view'),  # This line should work now
    path('', views.index, name='index'),
     # In your urls.py
         path('shop/update_order/', views.update_order, name='update_order'),
    path('update_order/',views.update_order, name='update_order'),
    path('update_product/', views.update_product, name='update_product'),
    path('add_product/', views.add_product, name='add_product'),
    path('admin_product_list/', views.admin_product_list, name='admin_product_list'),  # example for the list view
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
     path('admin_dashboard/dashboard/',views.admin_dashboard, name='admin_dashboard'),
    path('admin_product_list/', views.admin_product_list, name='admin_product_list'),
    path('admin_order_list/', views.admin_order_list, name='admin_order_list'),  # Ensure this line exists
    path('admin_rating_list/', views.admin_rating_list, name='admin_rating_list'),
    path('admin_order_updates/', views.admin_order_updates, name='admin_order_updates'),  # Add this line
    path('admin/order-update/edit/<int:order_id>/', edit_order_update, name='edit_order_update'),
    path('admin_contact_list/', views.admin_contact_list, name='admin_contact_list'),
    path('admin_user_list/', views.admin_user_list, name='admin_user_list'),  # Add this if needed
    path('signup/', views.handleSignUp, name='handleSignUp'),
    path('login/', views.handeLogin, name="handleLogin"),
    path('logout/', views.handleLogout, name="handleLogout"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="ContactUs"),
    path('tracker/', views.tracker, name="TrackingStatus"),
    path('search/', views.search, name="Search"),
    path('checkout/', views.checkout, name="Checkout"),
    path('productView/<int:myid>', views.productView, name="productView"),
    path('orderView/', views.orderView, name="orderView"),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="shop/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="shop/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="shop/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="shop/password_reset_done.html"),
         name="password_reset_complete"),

]