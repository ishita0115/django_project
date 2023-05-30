from django.contrib import admin
from app1.models import *
# Register your models here.

admin.site.register(Category)


class productregister(admin.ModelAdmin):
    list_display=['name','price','description']

admin.site.register(Product,productregister)

class userregister(admin.ModelAdmin):
    list_display=['name','email','phone']
    list_filter=['name','email','phone']

admin.site.register(UserRegister,userregister)