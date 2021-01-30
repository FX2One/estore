from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#null If True, Django will store empty values as NULL in the database. Default is false

#blank If True, the field is allowed to be blank. Default is False.
#Note that this is different than null. null is purely database-related, whereas blank is validation-related.
#If a field has blank=True, form validation will allow entry of an empty value.
#If a field has blank=False, the field will be required.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)  # install Pillow

    def __str__(self):
        return self.name

    #model URL method for image field (default picture)
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    #setting FK to Customer ,if customer gets deleted it does not delete the order, it sets customer value to NULL
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])  #calculate the sum of item.get_total value, to calculate all items
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems]) #total is going to be set to quantity, to know how many items are in the cart
        return total

#orderItem with Many to One Relationship, Order Item within our Cart which have multiple items in it
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

#customer information
class ShippingAddress(models.Model):
    #FK set to Customer. If Order gets deleted, still have shipping address for customer to validate data
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zip = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address




