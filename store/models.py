import uuid
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from PIL import Image
from io import BytesIO
from django.utils import timezone

# Create your models here.
class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated','-created')


class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

def image_directory_path(instance, filename):
    print(filename)
    return 'images_{0}/{1}'.format(instance, filename)

class Product(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bar_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    cost = models.FloatField()
    price = models.FloatField()
    quantity = models.IntegerField()
    image = models.ImageField(upload_to=image_directory_path, blank=True, null=True)
    on_display = models.BooleanField(default=True, verbose_name="this product is available?")

    @property
    def total_cost(self):
        total = self.cost * float(self.quantity)
        return total

    def __str__(self):
        return self.name
    

class Customer(models.Model):
    customer_id = models.CharField(max_length=12, unique=True, blank=True, null=True)
    name = models.CharField(max_length=200, unique=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name
    
class OrderTransaction(models.Model):
    order_id = models.CharField(max_length=12, unique=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.PositiveIntegerField()
    total_amount = models.FloatField()
    is_paid = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_accepted','-created']

    @property
    def get_cost(self):
        cost = self.price * self.quantity
        return cost
    
    @property
    def change(self):
        change = self.total_amount - self.money_tender
        return change
    
    @property
    def balance(self):
        if not self.is_paid:
            balance = self.get_cost
        else:
            balance = 0.0
        return balance
    
    @property
    def is_recent_orders(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created <= now

    def __str__(self):
        return self.customer.username

class CustomerOrder(TimeStampedModel):
    order_id = models.CharField(max_length=100, unique=True)
    orders = models.ForeignKey(OrderTransaction, on_delete=models.CASCADE)
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.order_id


class ItemRequest(models.Model):
    request_by = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=120)
    message = models.CharField(max_length=120, blank=True, null=True)
    is_noted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.request_by

@receiver(post_save, sender=OrderTransaction)
def order_pro_save(sender, instance, created, *args, **kwargs):
    if created:
        uuid_code = str(uuid.uuid4()).replace("-", "").upper()[:8]
        instance.order_id = uuid_code
        instance.save()

@receiver(pre_save, sender=Customer)
def customer_id_pre_save(sender, instance, *args, **kwargs):
    if instance.customer_id == None:
        uuid_code = str(uuid.uuid4()).replace("-", "").upper()[:12]
        instance.customer_id = uuid_code

@receiver(pre_save, sender=CustomerOrder)
def customer_order_id_pre_save(sender, instance, *args, **kwargs):
    if instance.order_id == None:
        uuid_code = str(uuid.uuid4()).replace("-", "").upper()[:12]
        instance.order_id = uuid_code

# def get_center_size(img):
#     im = Image.open(img)
#     w, h = im.width, im.height
#     wh = 200
#     ew, eh = w-wh, h-wh
#     left, top = ew/2, eh/2
#     right, bottom = left + wh, top + wh
#     im1 = im.crop((left, top, right, bottom))
#     output = BytesIO()
#     print(output)
#     return im1

# @receiver(post_save, sender=Product)
# def post_save_crop_image(sender, instance, created, *args, **kwargs):
#     if instance.image:
#         instance.image = get_center_size(instance.image.path).save('crop.jpg')
#         print(instance.image.path)
#         instance.save()