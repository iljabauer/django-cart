from cart import Cart
from django.views.decorators.cache import never_cache

@never_cache
def cart_processor(request):
    return {'cart' : Cart(request)}
