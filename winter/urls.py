from django.contrib import admin
from django.urls import path
from winter import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index),
    
    # path('category',views.category_page),
    path('category',views.category_main),
    path('contact',views.contact),
    path('all_product',views.all_product),
    path('category/<str:cat_name>',views.category),
    path('category/<str:cat_name>/<str:sub_name>',views.sub_category),
    path('single-product/<str:pro_details>',views.single_product),
    path('login',views.login),
    path('add_cart/<int:id>',views.add_cart),
    path('delete_cart/<int:id>',views.delete_cart),
    path('delete_all_cart',views.delete_all_cart),
    path('update_cart',views.update_cart),
    path('register',views.register),
    path('logout/',views.logout),
    path('cart',views.cart),
    path('checkout',views.checkout),
    path('data',views.data),
    path('faq',views.faq),
    path('tracking',views.tracking),
    path('confirmation',views.confirmation),
    path('profile',views.profile),
    path('edit_address/<int:id>',views.edit_address),
    path('update_address/<int:id>',views.update_address),
    path('add_address',views.add_address),
    path('handlerequest',views.handlerequest),
    
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)