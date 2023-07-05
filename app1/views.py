from django.shortcuts import render, redirect
from django.http import HttpResponse
from app1.models import *
import random
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

def first(request):
    return HttpResponse("<h1>my first web page....</h1>")

def login(request):
    if request.method == 'POST':
        email1=request.POST['email']
        password1=request.POST['psw']
        try:
            data=UserRegister.objects.get(email=email1,password=password1)
            if data:
                request.session['email']=data.email
                print(request.session['email'])
                return redirect('index')
            else:
                return render(request,'login.html',{'message':'Invalid email or password'})
        except:
            return render(request,'login.html',{'message':'Invalid email or password'})
    return render(request, 'login.html')

def logout(request):
    if 'email' in request.session.keys():
        del request.session['email']
        return redirect('index')
    else:
        return redirect('index')

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
    if 'email' in request.session:
        a=request.session['email']
        data=Category.objects.all()
        return render(request,'base.html',{'data':data,'a':a})
    else:
        data=Category.objects.all()
        return render(request,'base.html',{'data':data})


def productcall(request):
    if 'email' in request.session:
        a=request.session['email']
        data=Product.objects.all()
        return render(request,'productcall.html',{'data':data,'a':a})
    else:
        data=Product.objects.all()
        return render(request,'productcall.html',{'data':data})
    
    

def productcategorywise(request,id):
    if 'email' in request.session:
        a=request.session['email']
        data=Product.objects.filter(Category=id)
        return render(request,'productcall.html',{'data':data,'a':a})
    else:
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
    if 'email' in request.session:
        a=request.session['email']
        data=Product.objects.get(pk=id)
        return render(request,'singleproduct.html',{'data':data,'a':a})
    else:
        data=Product.objects.get(pk=id)
        return render(request,'singleproduct.html',{'data':data})

def changepass(request):
    if 'email' in request.session:
        a=request.session['email']
        user=UserRegister.objects.get(email=a)
        if request.method=="POST":
            old=request.POST['oldpass']
            newpass=request.POST['newpass']
            newpass1=request.POST['newpass1']
            if old==user.password:
                if newpass==newpass1:
                    user.password=newpass
                    user.save()
                    return render(request,'changepass.html',{'message':"New password update",'a':a})
                else:
                    return render(request,'changepass.html',{'message':"New password not match",'a':a})
            else:
                return render(request,'changepass.html',{'message':"Old password not match",'a':a})
            
        return render(request,'changepass.html',{'a':a})
    else:
        return redirect('login1')

def contact(request):
    if 'email' in request.session:
        a=request.session['email']
        data=UserRegister.objects.get(email=a)
        if request.method=="POST":
            contact_us=Contactus()
            contact_us.name=request.POST['name']
            contact_us.email=request.POST['email']
            contact_us.phone=request.POST['phone']
            contact_us.message=request.POST['message']
            contact_us.save()
            return render(request,'contactus.html',{'message':"Message Sent Successfully",'a':a})
        return render(request,'contactus.html',{'data':data,'a':a})
    else:
        if request.method=="POST":
            contact_us=Contactus()
            contact_us.name=request.POST['name']
            contact_us.email=request.POST['email']
            contact_us.phone=request.POST['phone']
            contact_us.message=request.POST['message']
            contact_us.save()
            return render(request,'contactus.html',{'message':"Message Sent Successfully"})
        return render(request,'contactus.html')

def forgot_pass(request):
    return render(request,'forgot_pass.html')

def send_otp(request):
    error_message = None
    otp = random.randint(11111,99999)
    email1 = request.POST.get('email')
    user_email=UserRegister.objects.filter(email=email1)
    if user_email:
        user = UserRegister.objects.get(email=email1)
        user.otp=user.save()
        request.session['email']= request.POST['email']
        html_msg= 'your one time password :- "+"' + str(otp)
        subject= 'welcom to python world'
        email_from = settings.EMAIL_HOST_USER
        email_to = ['email']
        message= (subject,html_msg,email_from,email_to)
        message.send()
        message.success(request,'otp send to your email')
        return redirect('enter_otp')
    else:
        error_message='invalid email pls enter correct email..'
        return render(request,'forgot_pass.html')


def enter_otp(request):
    error_msg = None
    if request.session.has_key('email'):
        email=request.session['email']
        user = UserRegister.objects.filter(email=email)
        for u in user:
            user_otp = u.otp
            if request.method == 'POST':
                otp = request.POST.get('otp')
                if not otp:
                    error_msg= 'otp requried..'
                elif not user_otp == otp:
                    error_msg = 'otp is invalid'
                if not error_msg:
                    return render(request, 'forgot_pass.html')
            return render(request, 'enter_otp.html',{'error':error_msg})
        else:
            return render(request,'forgot_pass.html')


import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

def buynow(request):
    if 'email' in request.session:
        a=UserRegister.objects.get(email=request.session['email'])
        if request.method=="POST":
            request.session['productid']=request.POST['id']
            request.session['quantity']="1"
            request.session['userid']=a.pk
            request.session['username']=a.name
            request.session['userEmail']=a.email
            request.session['userContact']=a.phone
            request.session['address']=a.address
            b=Product.objects.get(id=request.POST['id'])
            request.session['orderAmount']=b.price
            request.session['paymentMethod']="Razorpay"
            request.session['transactionId']=""
            return redirect('razorpayView') 
    else:
        return redirect('login1')


RAZOR_KEY_ID = 'rzp_test_GBYBpjUCvkNBYU'
RAZOR_KEY_SECRET = 'ovygwbvyLiGNUHFnPesOfqoC'
client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))

def razorpayView(request):
    currency = 'INR'
    amount = int(request.session['orderAmount'])*100
    # Create a Razorpay Order
    razorpay_order = client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'http://127.0.0.1:8000/paymenthandler/'    
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url    
    return render(request,'razorpayDemo.html',context=context)

@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = client.utility.verify_payment_signature(
                params_dict)
            
            amount = int(request.session['orderAmount'])*100  # Rs. 200
            # capture the payemt
            client.payment.capture(payment_id, amount)

            #Order Save Code
            orderModel = Ordermodel()
            print(123)
            orderModel.productid=request.session['productid']
            print(234)
            orderModel.productqty=request.session['quantity']
            print(345)
            orderModel.userId = request.session['userId']
            print(456)
            orderModel.userName = request.session['username']
            print(567)
            orderModel.userEmail = request.session['userEmail']
            print("io")
            orderModel.userContact = request.session['userContact']
            print("rty")
            orderModel.address = request.session['address']
            print("789")
            orderModel.orderAmount = request.session['orderAmount']
            print("777")
            orderModel.paymentMethod = request.session['paymentMethod']
            print(888)
            orderModel.transactionId = payment_id
            print(999)
            # productdata=Product.objects.get(id=request.session['productid'])
            # productdata.quantity=productdata.quantity-int(request.session['quantity'])
            # productdata.save()
            orderModel.save()
            orderdata=Ordermodel.objects.latest('id')
            print(orderdata.pk)
            cartdata=Cartmodel.objects.filter(userId=request.session['userId'])
            for i in cartdata:
                i.orderId=str(orderdata.pk)
                productdata=Product.objects.get(id=i.productId)
                productdata.quantity=productdata.quantity-int(i.quantity)
                productdata.save()
                i.save()
            del request.session['productid']
            del request.session['quantity']
            del request.session['userId']
            del request.session['username']
            del request.session['userEmail']
            del request.session['userContact']
            del request.session['address']
            del request.session['orderAmount']
            del request.session['paymentMethod']
            # render success page on successful caputre of payment
            return redirect('orderSuccessView')
        except:
            print("Hello")
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        print("Hello123")
       # if other than POST request is made.
        return HttpResponseBadRequest()

def successview(request):
    if 'email' in request.session:
        a=request.session['email']
        return render(request,'order_sucess.html',{'a':a})
    else:
        return HttpResponseBadRequest()
    
def orderview(request):
    if 'email' in request.session:
        a=request.session['email']
        data=Ordermodel.objects.filter(userEmail=a)
        prolist=[]
        for i in data:
            pro={}
            productdata=Product.objects.get(id=i.productid)
            pro['name']=productdata.name
            pro['img']=productdata.img
            pro['price']=i.orderAmount
            pro['quantity']=i.productqty
            pro['date']=i.orderDate
            pro['TransactionId']=i.transactionId
            prolist.append(pro)
        return render(request,'ordertable.html',{'a':a,'prolist':prolist})
    else:
        return HttpResponseBadRequest()
