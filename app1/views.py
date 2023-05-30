from django.shortcuts import render,redirect
from django.http import HttpResponse
from app1.models import *
# Create your views here.

def first(request):
    return HttpResponse("<h1>my first web page....</h1>")

def login(request):
    if request.method == 'POST':
        email1 = request.POST['email']
        password1=request.POST['psw']
        try:
            data=UserRegister.objects.get(email=email1,password=password1)
            if data:
                request.session['email']=data.email
                request.session['id']=data.pk
                return redirect('index')
            else:
                return render(request,'Login.html',{'message':'Invalid email or password'})
        except:
            return render(request,'Login.html',{'message':'Invalid email or password'})
    return render(request, 'Login.html')

def table_all(request):
    a=UserRegister.objects.all()
    print('data',a)
    return render(request, 'table.html',{'data':a})

def table_filter(request):
    a=UserRegister.objects.filter(phone=9327058588)
    print('data',a)
    return render(request, 'table.html',{'data':a})

def table_all_p(request):
    a=Product.objects.all()
    print('data',a)
    return render(request, 'table.html',{'data':a})

def table_filter_p(request):
    a=Product.objects.filter(description="art")
    print('data',a)
    return render(request, 'table.html',{'data':a})

def table_get(request):
    a=Product.objects.get(price=2000)
    print('data',a)
    return render(request, 'table_get.html',{'data':a})

def index(request):
    data=Category.objects.all()
    return render(request,'base.html',{'data':data})

def productcall(request):
    data=Product.objects.all()
    return render(request,'productcall.html',{'data':data})

def productcategorywise(request,id):
    data=Product.objects.filter(Category=id)
    return render(request,'productcall.html',{'data':data})

def register(request):
    if request.method=="POST":
        name1=request.POST['username']
        email1=request.POST['email']
        password1=request.POST['psw']
        phone1=request.POST['phone']
        address1=request.POST['Address']
        print(name1,email1,password1,address1,phone1)
        data=UserRegister(name=name1,email=email1,password=password1,phone=phone1,address=address1)
        a=UserRegister.objects.filter(email=email1)
        if len(a)==0:
            data.save()
            return redirect('login1')
        else:
            return render(request,'register.html',{'message':' user already exist..'})
    return render(request,'register.html')


def singleproduct(request,id):
    data=Product.objects.get(pk=id)
    return render(request,'singleproduct.html',{'data':data})