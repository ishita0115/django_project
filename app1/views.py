from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from app1.models import *
import random
from django.conf import settings
from django.core.mail import send_mail
import razorpay
from django.views.decorators.csrf import csrf_exempt

# ─── Helpers ────────────────────────────────────────────────────────────────

def get_user_email(request):
    return request.session.get('email')


# ─── Basic / Debug ──────────────────────────────────────────────────────────

def first(request):
    return HttpResponse("<h1>my first web page....</h1>")


def table_all(request):
    a = UserRegister.objects.all()
    return render(request, 'table.html', {'data': a})

def table_filter(request):
    a = UserRegister.objects.filter(phone=9327058588)
    return render(request, 'table.html', {'data': a})

def table_all_p(request):
    a = Product.objects.all()
    return render(request, 'table.html', {'data': a})

def table_filter_p(request):
    a = Product.objects.filter(description="art")
    return render(request, 'table.html', {'data': a})

def table_get(request):
    a = Product.objects.get(price=2000)
    return render(request, 'table_get.html', {'data': a})


# ─── Authentication ──────────────────────────────────────────────────────────

def login(request):
    if request.method == 'POST':
        email1 = request.POST['email']
        password1 = request.POST['psw']
        try:
            data = UserRegister.objects.get(email=email1, password=password1)
            request.session['email'] = data.email
            return redirect('index')
        except UserRegister.DoesNotExist:
            return render(request, 'login.html', {'message': 'Invalid email or password'})
    return render(request, 'login.html')


def logout(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect('index')


def register(request):
    if request.method == "POST":
        name1 = request.POST['username']
        email1 = request.POST['email']
        password1 = request.POST['psw']
        phone1 = request.POST['phone']
        address1 = request.POST['Address']
        if UserRegister.objects.filter(email=email1).exists():
            return render(request, 'register.html', {'message': 'User already exists.'})
        UserRegister(name=name1, email=email1, password=password1, phone=phone1, address=address1).save()
        return redirect('login1')
    return render(request, 'register.html')


def changepass(request):
    if 'email' not in request.session:
        return redirect('login1')
    a = request.session['email']
    user = UserRegister.objects.get(email=a)
    if request.method == "POST":
        old = request.POST['oldpass']
        newpass = request.POST['newpass']
        newpass1 = request.POST['newpass1']
        if old == user.password:
            if newpass == newpass1:
                user.password = newpass
                user.save()
                return render(request, 'changepass.html', {'message': 'Password updated successfully.', 'a': a})
            else:
                return render(request, 'changepass.html', {'message': 'New passwords do not match.', 'a': a})
        else:
            return render(request, 'changepass.html', {'message': 'Old password is incorrect.', 'a': a})
    return render(request, 'changepass.html', {'a': a})


def forgot_pass(request):
    return render(request, 'forgot_pass.html')


def send_otp(request):
    otp = random.randint(11111, 99999)
    email1 = request.POST.get('email')
    if UserRegister.objects.filter(email=email1).exists():
        request.session['email'] = email1
        request.session['otp'] = str(otp)
        subject = 'ArtShopy - Password Reset OTP'
        html_msg = f'Your one-time password for ArtShopy is: {otp}'
        send_mail(subject, html_msg, settings.EMAIL_HOST_USER, [email1])
        return redirect('enter_otp')
    return render(request, 'forgot_pass.html', {'error': 'Email not found.'})


def enter_otp(request):
    if 'email' not in request.session:
        return redirect('forgot_pass')
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '')
        stored_otp = request.session.get('otp', '')
        if entered_otp == stored_otp:
            return redirect('change')
        return render(request, 'enter_otp.html', {'error': 'Invalid OTP. Please try again.'})
    return render(request, 'enter_otp.html')


# ─── Pages ───────────────────────────────────────────────────────────────────

def index(request):
    a = get_user_email(request)
    data = Category.objects.all()
    return render(request, 'base.html', {'data': data, 'a': a})


def contact(request):
    a = get_user_email(request)
    data = None
    if a:
        data = UserRegister.objects.get(email=a)
    if request.method == "POST":
        Contactus(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            message=request.POST['message'],
        ).save()
        return render(request, 'contactus.html', {'message': 'Message sent successfully!', 'a': a})
    return render(request, 'contactus.html', {'data': data, 'a': a})


# ─── Products ────────────────────────────────────────────────────────────────

def productcall(request):
    a = get_user_email(request)
    data = Product.objects.all()
    return render(request, 'productcall.html', {'data': data, 'a': a})


def productcategorywise(request, id):
    a = get_user_email(request)
    data = Product.objects.filter(Category=id)
    return render(request, 'productcall.html', {'data': data, 'a': a})


def singleproduct(request, id):
    a = get_user_email(request)
    data = Product.objects.get(pk=id)
    reviews = Review.objects.filter(product=data).order_by('-created_at')
    avg_rating = data.average_rating()
    user_review = None
    in_wishlist = False
    if a:
        user_review = Review.objects.filter(product=data, user_email=a).first()
        in_wishlist = Wishlist.objects.filter(user_email=a, product=data).exists()
    return render(request, 'singleproduct.html', {
        'data': data,
        'a': a,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'user_review': user_review,
        'in_wishlist': in_wishlist,
        'star_range': range(1, 6),
    })


def search_products(request):
    a = get_user_email(request)
    query = request.GET.get('q', '').strip()
    if query:
        data = (Product.objects.filter(name__icontains=query) |
                Product.objects.filter(description__icontains=query)).distinct()
    else:
        data = Product.objects.all()
    return render(request, 'productcall.html', {'data': data, 'a': a, 'query': query})


# ─── Reviews ─────────────────────────────────────────────────────────────────

def add_review(request, product_id):
    if 'email' not in request.session:
        return redirect('login1')
    if request.method == 'POST':
        email = request.session['email']
        user = UserRegister.objects.get(email=email)
        product = Product.objects.get(id=product_id)
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '').strip()
        if comment:
            Review.objects.update_or_create(
                user_email=email,
                product=product,
                defaults={'user_name': user.name, 'rating': rating, 'comment': comment}
            )
    return redirect('productget1', id=product_id)


# ─── Cart ────────────────────────────────────────────────────────────────────

def cart_view(request):
    if 'email' not in request.session:
        return redirect('login1')
    email = request.session['email']
    a = email
    cart_items = Cart.objects.filter(user_email=email).select_related('product')
    total = sum(item.get_subtotal() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total, 'a': a})


def add_to_cart(request, product_id):
    if 'email' not in request.session:
        return redirect('login1')
    if request.method == 'POST':
        email = request.session['email']
        product = Product.objects.get(id=product_id)
        qty = int(request.POST.get('quantity', 1))
        cart_item, created = Cart.objects.get_or_create(user_email=email, product=product)
        if not created:
            cart_item.quantity += qty
        else:
            cart_item.quantity = qty
        cart_item.save()
    return redirect('cart')


def remove_from_cart(request, item_id):
    if 'email' not in request.session:
        return redirect('login1')
    Cart.objects.filter(id=item_id, user_email=request.session['email']).delete()
    return redirect('cart')


def update_cart(request, item_id):
    if 'email' not in request.session:
        return redirect('login1')
    if request.method == 'POST':
        qty = int(request.POST.get('quantity', 1))
        try:
            item = Cart.objects.get(id=item_id, user_email=request.session['email'])
            if qty > 0:
                item.quantity = qty
                item.save()
            else:
                item.delete()
        except Cart.DoesNotExist:
            pass
    return redirect('cart')


def cart_checkout(request):
    if 'email' not in request.session:
        return redirect('login1')
    email = request.session['email']
    user = UserRegister.objects.get(email=email)
    cart_items = Cart.objects.filter(user_email=email).select_related('product')
    if not cart_items.exists():
        return redirect('cart')
    total = sum(item.get_subtotal() for item in cart_items)
    product_ids = ','.join(str(item.product.id) for item in cart_items)
    product_qtys = ','.join(str(item.quantity) for item in cart_items)
    request.session['productid'] = product_ids
    request.session['quantity'] = product_qtys
    request.session['userid'] = str(user.pk)
    request.session['username'] = user.name
    request.session['userEmail'] = user.email
    request.session['userContact'] = user.phone
    request.session['address'] = user.address
    request.session['orderAmount'] = total
    request.session['paymentMethod'] = 'Razorpay'
    return redirect('razorpayView')


# ─── Wishlist ─────────────────────────────────────────────────────────────────

def wishlist_view(request):
    if 'email' not in request.session:
        return redirect('login1')
    email = request.session['email']
    wishlist_items = Wishlist.objects.filter(user_email=email).select_related('product')
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items, 'a': email})


def add_to_wishlist(request, product_id):
    if 'email' not in request.session:
        return redirect('login1')
    email = request.session['email']
    product = Product.objects.get(id=product_id)
    Wishlist.objects.get_or_create(user_email=email, product=product)
    return redirect('productget1', id=product_id)


def remove_from_wishlist(request, product_id):
    if 'email' not in request.session:
        return redirect('login1')
    Wishlist.objects.filter(user_email=request.session['email'], product_id=product_id).delete()
    return redirect('wishlist')


# ─── Checkout / Payment ───────────────────────────────────────────────────────

def buynow(request):
    if 'email' not in request.session:
        return redirect('login1')
    a = UserRegister.objects.get(email=request.session['email'])
    if request.method == "POST":
        b = Product.objects.get(id=request.POST['id'])
        request.session['productid'] = request.POST['id']
        request.session['quantity'] = "1"
        request.session['userid'] = str(a.pk)
        request.session['username'] = a.name
        request.session['userEmail'] = a.email
        request.session['userContact'] = a.phone
        request.session['address'] = a.address
        request.session['orderAmount'] = b.price
        request.session['paymentMethod'] = "Razorpay"
        return redirect('razorpayView')
    return redirect('index')


RAZOR_KEY_ID = 'rzp_test_GBYBpjUCvkNBYU'
RAZOR_KEY_SECRET = 'ovygwbvyLiGNUHFnPesOfqoC'
client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))


def razorpayView(request):
    currency = 'INR'
    amount = int(request.session['orderAmount']) * 100
    razorpay_order = client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
    razorpay_order_id = razorpay_order['id']
    callback_url = 'http://127.0.0.1:8000/paymenthandler/'
    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url,
    }
    return render(request, 'razorpayDemo.html', context=context)


@csrf_exempt
def paymenthandler(request):
    if request.method != "POST":
        return HttpResponseBadRequest()
    try:
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature,
        }
        client.utility.verify_payment_signature(params_dict)
        amount = int(request.session['orderAmount']) * 100
        client.payment.capture(payment_id, amount)

        orderModel = Ordermodel()
        orderModel.productid = request.session['productid']
        orderModel.productqty = request.session['quantity']
        orderModel.userId = request.session['userid']
        orderModel.userName = request.session['username']
        orderModel.userEmail = request.session['userEmail']
        orderModel.userContact = request.session['userContact']
        orderModel.address = request.session['address']
        orderModel.orderAmount = request.session['orderAmount']
        orderModel.paymentMethod = request.session['paymentMethod']
        orderModel.transactionId = payment_id
        orderModel.save()

        # Update product stock and clear cart
        email = request.session['userEmail']
        cart_items = Cart.objects.filter(user_email=email)
        for item in cart_items:
            product = item.product
            product.quantity = max(0, product.quantity - item.quantity)
            product.save()
        cart_items.delete()

        # Clean up session
        for key in ['productid', 'quantity', 'userid', 'username', 'userEmail',
                    'userContact', 'address', 'orderAmount', 'paymentMethod']:
            request.session.pop(key, None)

        return redirect('orderSuccessView')
    except Exception:
        return HttpResponseBadRequest()


def successview(request):
    if 'email' not in request.session:
        return HttpResponseBadRequest()
    a = request.session['email']
    return render(request, 'order_sucess.html', {'a': a})


def orderview(request):
    if 'email' not in request.session:
        return redirect('login1')
    a = request.session['email']
    data = Ordermodel.objects.filter(userEmail=a).order_by('-orderDate')
    prolist = []
    for i in data:
        pro = {}
        try:
            # productid may be comma-separated for cart orders; use first id
            pid = str(i.productid).split(',')[0]
            productdata = Product.objects.get(id=pid)
            pro['name'] = productdata.name
            pro['img'] = productdata.img
        except Exception:
            pro['name'] = 'Unknown Product'
            pro['img'] = None
        pro['price'] = i.orderAmount
        pro['quantity'] = i.productqty
        pro['date'] = i.orderDate
        pro['TransactionId'] = i.transactionId
        prolist.append(pro)
    return render(request, 'ordertable.html', {'a': a, 'prolist': prolist})
