from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
import datetime



# Create your models here.me

class MyUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

class Session(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

class Clock_in(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('clock-in', 'Clock-in'),
        ('clock-out', 'Clock-out'),
    )
    clock_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='clock-in', null=False)
    clock_time = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.clock_status

    
class Conversation(models.Model):
    participants = models.ManyToManyField(MyUser, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Conversation',
        null=False
    )
    sender = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='Sender',
        null=False
    )
    message = models.TextField(blank=False, verbose_name='Message')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Created At')

# def get_first_user_id():
#     return MyUser.objects.first().id
class ReceiptPart1(models.Model):
    SCRATCHED = 'scratched'
    DAMAGED = 'damaged'
    ACCIDENT = 'accident'
    BROKEN = 'broken'
    DAMAGE_CHOICES = [
        (SCRATCHED, 'Scratched'),
        (DAMAGED, 'Damaged'),
        (ACCIDENT, 'Accident'),
        (BROKEN, 'Broken'),
    ]
    
    damage_type = models.CharField(max_length=20, choices=DAMAGE_CHOICES)
    description = models.TextField(blank=True, default='', null=False)
    customer_initial = models.CharField(max_length=2, default='', null=False)
    
    def __str__(self):
        return f'ReceiptPart1 - {self.pk}'

class ReceiptPart2(models.Model):
    time_of_call = models.CharField(max_length=100, blank=True, default="")
    date_in = models.DateField(blank=True, null=True)
    date_out = models.DateField(blank=True, null=True)
    time_start = models.TimeField(blank=True, null=True)
    time_finish = models.TimeField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, default="")
    customer_address = models.CharField(max_length=200, blank=True, default="")
    pickup_address = models.CharField(max_length=200, blank=True, default="")
    dropoff_address = models.CharField(max_length=200, blank=True, default="")
    phone = models.CharField(max_length=20, blank=True, default="")
    dl = models.CharField(max_length=20, blank=True, default="")
    jumpstart = models.BooleanField(default=False)
    tow = models.BooleanField(default=False)
    tirechange = models.BooleanField(default=False)
    lockout = models.BooleanField(default=False)
    year = models.CharField(max_length=20, blank=True, default="")
    make = models.CharField(max_length=50, blank=True, default="")
    color = models.CharField(max_length=50, blank=True, default="")
    model = models.CharField(max_length=50, blank=True, default="")
    license_no = models.CharField(max_length=20, blank=True, default="")
 


    def __str__(self):
        return f'ReceiptPart2 - {self.pk}'

class ReceiptPart3(models.Model):
    vin_number = models.CharField(max_length=20, blank=True, default='')
    policy_number = models.CharField(max_length=20, blank=True, default='')
    hook_up = models.BooleanField(blank=True, null=True, default=None)
    winch = models.BooleanField(blank=True, null=True, default=None)
    flares = models.BooleanField(blank=True, null=True, default=None)
    dollies = models.BooleanField(blank=True, null=True, default=None)
    scotch_blocks = models.BooleanField(blank=True, null=True, default=None)
    ramps = models.BooleanField(blank=True, null=True, default=None)
    snatch_blocks = models.BooleanField(blank=True, null=True, default=None)
    signature = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f'ReceiptPart3 - {self.pk}'
    


class ReceiptPart4(models.Model):
    mileage_start =  models.IntegerField(blank=True, null=True, default=0)
    mileage_finish = models.IntegerField(blank=True, null=True, default=0)
    mileage_total = models.IntegerField(blank=True, null=True, default=0)
    labor_time_start = models.TimeField(blank=True, null=True, default=datetime.time(0, 0))
    labor_time_finish = models.TimeField(blank=True, null=True, default=datetime.time(0, 0))
    labor_time_total = models.TimeField(blank=True, null=True, default=datetime.time(0, 0))
    extra_person_start = models.TimeField(blank=True, null=True, default=datetime.time(0, 0))
    extra_person_finish = models.TimeField(blank=True, null=True, default=datetime.time(0, 0))
    extra_person_total = models.TimeField(blank=True, null=True, default=datetime.time(0, 0))
    towing_charge = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=0)
    mileage_charge = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=0)
    labor_charge = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=0)
    extra_person_charge = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=0)
    special_equipment_charge = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=0)
    storage_charge = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=0)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=0)
    tax = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default=0)
    created_at = models.DateTimeField(default=timezone.now,)

    def __str__(self):
        return f'ReceiptPart4 - {self.pk}'
    
class Coordinates(models.Model):
    identifier = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)