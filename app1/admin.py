from django.contrib import admin
from app1.models import *


admin.site.register(Category)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'description']
    list_filter = ['Category']
    search_fields = ['name', 'description']

admin.site.register(Product, ProductAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']
    list_filter = ['name', 'email', 'phone']
    search_fields = ['name', 'email']

admin.site.register(UserRegister, UserAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']

admin.site.register(Contactus, ContactAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['userName', 'userEmail', 'orderAmount', 'paymentMethod', 'orderDate']
    list_filter = ['paymentMethod', 'orderDate']
    search_fields = ['userName', 'userEmail', 'transactionId']

admin.site.register(Ordermodel, OrderAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'product', 'quantity', 'added_at']

admin.site.register(Cart, CartAdmin)


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'product', 'added_at']

admin.site.register(Wishlist, WishlistAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'product', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['user_name', 'comment']

admin.site.register(Review, ReviewAdmin)
