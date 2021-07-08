from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.utils.decorators import classonlymethod
# Create your models here.
class Admin(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=50)
    image = models.ImageField(upload_to="admins")
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name= models.CharField(max_length=200)
    email=models.EmailField(max_length=100)
    address= models.CharField(max_length=200,null=True,blank=True)
    mobile=models.CharField(max_length=10)
    joined_on= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name+" (" +str(self.joined_on) +")"

Quantity_unit=(
    ('Kg','Kg'),
    ('Packet','Packet'),
    ('Crate','Crate'),
    ('Liter','Liter'),
    ('Crate','Crate'),
    ('Whole','Whole'),
    ('Piece','Piece'),

)
class Product(models.Model):
    title = models.CharField(max_length=200)
    slug= models.SlugField(unique=True)
    image= models.ImageField(upload_to="productsf")
    quantity_unit=models.CharField(max_length=50,choices=Quantity_unit)
    marked_price= models.FloatField()
    selling_price =models.FloatField()
    description= models.TextField()
    view_count=models.PositiveIntegerField(default=0)
    

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/images/")

    def __str__(self):
        return self.product.title

class Cart(models.Model):
    customer =models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    total= models.FloatField(default=0)
    total_count=models.PositiveIntegerField(default=0)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return("Cart:")+str(self.id)

class CartProduct(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    rate=models.FloatField()
    quantity=models.FloatField()
    kg_quantity=models.PositiveIntegerField(default=0)
    count=models.PositiveIntegerField(default=0)
    subtotal=models.FloatField()

    def __str__(self):
        return "Cart:"+(self.cart.id)+"CartProduct"+(self.id)

# saved product



class SavedProduct(models.Model):
    customer =models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    rate=models.FloatField()
    created_at= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "SavedProduct"+(self.id)

ORDER_STATUS=(
    ("Order Received","Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way","On the way"),
    ("Order Delivered","Order Delivered"),
    ("Order Cancelled","Order Cancelled"),
)

METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("Payment with account number", "Payment with account number"),
    
)
class Order (models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    ordered_by= models.CharField(max_length=200)
    shipping_address=models.CharField(max_length=200)
    mobile=models.CharField(max_length=10)
    email=models.EmailField(null=True,blank=True)
    subtotal=models.FloatField()
    discount=models.FloatField()
    total=models.FloatField()
    order_status=models.CharField(max_length=50,choices=ORDER_STATUS)
    created_at=models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=50, choices=METHOD, default="Cash On Delivery")

    def __str__(self):
        return "Order:"+str(self.id)

class BusinessContact(models.Model):
    owner_name=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    phone_number=models.CharField(max_length=10)
    email=models.CharField(max_length=200)
    account_number=models.CharField(null=True, blank=True, max_length=200)
    location=models.TextField(null=True,blank=True)
    location_link=models.TextField(null=True,blank=True) 
    facebook=models.CharField(null=True,blank=True,  max_length=1000)
    youtube=models.CharField(null=True,blank=True, max_length=1000)
    twitter=models.CharField(null=True,blank=True, max_length=1000)
    instagram=models.CharField(null=True,blank=True, max_length=1000)

class BusinessTime(models.Model):
    sunday=models.CharField(max_length=200)
    monday=models.CharField(max_length=200)
    tuesday=models.CharField(max_length=200)
    wednesday=models.CharField(max_length=200)
    thursday=models.CharField(max_length=200)
    friday=models.CharField(max_length=200)
    saturday=models.CharField(max_length=200)
    
class Notice(models.Model):
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.message

class Update(models.Model):
    update=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.update

class About(models.Model):
    about=models.TextField()
    about_image=models.ImageField(upload_to="about_image")

    def __str__(self):
        return self.about

class Service(models.Model):
    service=models.TextField()
    about_image=models.ImageField(upload_to="about_image")

    def __str__(self):
        return self.service

class Help(models.Model):
    caption= models.CharField(max_length=100)
    video= models.FileField(upload_to="video/%y")

    def __str__(self):
        return self.caption

class YoutubeVideo(models.Model):
    desc=models.CharField(max_length=200)
    video_link=models.TextField()

class ContactUs(models.Model):
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    email= models.EmailField(max_length=50)
    subject= models.CharField(max_length=50)
    message= models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.first_name)+" "+(self.last_name)+" "+(self.created_at)


class Career(models.Model):
    title=models.CharField(max_length=200)
    location=models.CharField(max_length=200, null=True, blank=True)
    desc=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
