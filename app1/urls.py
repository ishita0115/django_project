from app1.views import *
from django.urls import path

urlpatterns = [
    # Debug / utility
    path('first/', first),
    path('table_all/', table_all),
    path('table_filter/', table_filter),
    path('table_all_p/', table_all_p),
    path('table_filter_p/', table_filter_p),
    path('table_get/', table_get),

    # Core pages
    path('', index, name='index'),
    path('contact-us/', contact, name='contact'),

    # Auth
    path('login/', login, name='login1'),
    path('logout/', logout, name='logout1'),
    path('register/', register, name='register1'),
    path('change-pass/', changepass, name='change'),
    path('forgot_pass/', forgot_pass, name='forgot_pass'),
    path('send_otp', send_otp, name='send_otp'),
    path('enter_otp', enter_otp, name='enter_otp'),

    # Products
    path('productcall', productcall, name='productall'),
    path('product-filter/<int:id>/', productcategorywise, name='productfilter1'),
    path('productget1/<int:id>/', singleproduct, name='productget1'),
    path('search/', search_products, name='search'),

    # Reviews
    path('review/add/<int:product_id>/', add_review, name='add_review'),

    # Cart
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', update_cart, name='update_cart'),
    path('cart/checkout/', cart_checkout, name='cart_checkout'),

    # Wishlist
    path('wishlist/', wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),

    # Checkout / Orders
    path('but-now/', buynow, name='buy'),
    path('razorpayview/', razorpayView, name='razorpayView'),
    path('paymenthandler/', paymenthandler, name='paymenthandler'),
    path('order-success/', successview, name='orderSuccessView'),
    path('my-orders/', orderview, name='orderview'),
]
