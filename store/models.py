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


class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class Product(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bar_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
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
    
class OrderTransaction(models.Model):
    order_id = models.CharField(max_length=12, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.PositiveIntegerField()
    total_amount = models.FloatField()
    money_tender = models.FloatField(default=0.0)
    is_paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def get_cost(self):
        cost = self.price * self.quantity
        return cost
    
    @property
    def change(self):
        change = self.total_amount - self.money_tender
        return change

    def __str__(self):
        return self.customer
    

@receiver(post_save, sender=OrderTransaction)
def order_pro_save(sender, instance, created, *args, **kwargs):
    if created:
        uuid_code = str(uuid.uuid4()).replace("-", "").upper()[:8]
        instance.order_id = uuid_code
        instance.save()