from app1.views import *
from django.urls import path

urlpatterns = [
    path('first/',first),
    path('login/',login,name='login1'),
    path('logout/',logout,name='logout1'),
    path('register/',register,name='register1'),
    path('table_all/',table_all),
    path('table_filter/',table_filter),
    path('table_all_p/',table_all_p),
    path('table_filter_p/',table_filter_p),
    path('table_get/',table_get),
    path('',index,name='index'),
    path('productcall',productcall,name='productall'),
    path('product-filter/<int:id>/',productcategorywise,name='productfilter1'),
    path('productget1/<int:id>/',singleproduct,name='productget1'),
    path('change-pass/',changepass,name='change'),
    path('contact-us/',contact,name='contact'),
    path('forgot_pass/',forgot_pass,name='forgot_pass'),
    path('send_otp',send_otp,name='send_otp'),
    path('enter_otp',enter_otp,name='enter_otp'),
    path('but-now/',buynow,name='buy'),
    path('razorpayview/',razorpayView,name='razorpayView'),
    path('paymenthandler/',paymenthandler,name='paymenthandler'),
]