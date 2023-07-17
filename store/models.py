import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Create your models here.
class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated','-created')


class Product(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bar_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    cost = models.FloatField()
    price = models.FloatField()
    quantity = models.IntegerField()

    @property
    def total_cost(self):
        total = self.cost * float(self.quantity)
        return total

    def __str__(self):
        return self.name
    

class Customer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    contact = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class Order(TimeStampedModel):
    order_id = models.CharField(max_length=12, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.customer
    

# @receiver(pre_save, sender=Product)
# def product_pre_save(sender, instance, *args, **kwargs):
#     if instance.bar_code == "":
#         uuid_code = str(uuid.uuid4()).replace("-", "").upper()[:12]
#         instance.bar_code = uuid_code