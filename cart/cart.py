import datetime
import models
import decimal

CART_ID = 'CART-ID'

class ItemAlreadyExists(Exception):
    pass

class ItemDoesNotExist(Exception):
    pass

class Cart:
    def __init__(self, request):
        self.__request = request
        cart_id = request.session.get(CART_ID)
        if cart_id:
            try:
                cart = models.Cart.objects.get(id=cart_id, checked_out=False)
            except models.Cart.DoesNotExist:
                cart = self.new(request)
        else:
            cart = self.new(request)
        self.cart = cart

    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item

    def new(self, request):
        cart = models.Cart(creation_date=datetime.datetime.now())
        # cart.save()
        # request.session[CART_ID] = cart.id
        return cart

    def create_cart(self):
        if not self.cart.id:
            self.cart.save()
            self.__request.session[CART_ID] = self.cart.id

    def add(self, product, unit_price, quantity=1):
        self.create_cart()
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            item = models.Item()
            item.cart = self.cart
            item.product = product
            item.unit_price = unit_price
            item.quantity = quantity
            item.save()
        else: #ItemAlreadyExists
            item.unit_price = unit_price
            item.quantity = item.quantity + int(quantity)
            item.save()

    def remove(self, product):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    def update(self, product, quantity):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
            item.quantity = int(quantity)
            item.save()
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist

    def count(self):
        return self.cart.summary()

    def summary(self):
        return self.cart.summary()

    def clear(self):
        for item in self.cart.item_set.all():
            item.delete()

    def check_out(self):
        cart = models.Cart.objects.get(pk=self.cart.id)
        cart.checked_out = True
        cart.save()

    def venda_valor(self, cart_pk):
        result = 0
        for item in self.cart.item_set.filter(cart=cart_pk):
            result += item.total_price
        return result

