from app1.models import Cart, Wishlist


def cart_wishlist_counts(request):
    cart_count = 0
    wishlist_count = 0
    if 'email' in request.session:
        email = request.session['email']
        cart_count = Cart.objects.filter(user_email=email).count()
        wishlist_count = Wishlist.objects.filter(user_email=email).count()
    return {'cart_count': cart_count, 'wishlist_count': wishlist_count}
