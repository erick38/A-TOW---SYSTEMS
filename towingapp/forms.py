from django import forms
from towingapp.models import Message, Conversation, MyUser
from django.shortcuts import render,HttpResponseRedirect, get_object_or_404
from datetime import datetime
from .models import ReceiptPart1, ReceiptPart2, ReceiptPart3, ReceiptPart4
from django.utils import timezone


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        conversation_id = self.data.get('conversation_id')
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=self.user)
        cleaned_data['conversation'] = conversation
        cleaned_data['sender'] = self.user
        return cleaned_data

class ConversationForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.fields['participants'] = forms.ModelMultipleChoiceField(
            queryset=MyUser.objects.exclude(id=request.user.id),
            widget=forms.CheckboxSelectMultiple
    )
    def save(self):
        participants = list(self.cleaned_data['participants'])
        participants.append(self.request.user)  # add sender back to the list of participants
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        message = Message.objects.create(
            conversation=conversation,
            sender=self.request.user,
            message=self.cleaned_data['message']
        )
        return conversation


class login_form(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class addclockinform(forms.Form):    
    STATUS_CHOICES = (
            ('clock-in', 'clock-in'),
            ('clock-out', 'clock-out'),
            )
    clock_status = forms.ChoiceField(choices=STATUS_CHOICES )

class add_AccountForm(forms.Form):
    username = forms.CharField(max_length=38)
    password = forms.CharField(widget=forms.PasswordInput)


class ReceiptForm(forms.Form):
    # Fields from ReceiptPart1 model
    customer_initial = forms.CharField(max_length=2, required=True)
    damage_type = forms.ChoiceField(choices=ReceiptPart1.DAMAGE_CHOICES)
    description = forms.CharField(widget=forms.Textarea)

    # Fields from ReceiptPart2 model
    time_of_call = forms.CharField(max_length=100)
    date_in = forms.DateField(widget=forms.DateInput)
    date_out = forms.DateField(widget=forms.DateInput)
    time_start = forms.TimeField(widget=forms.TimeInput)
    time_finish = forms.TimeField(widget=forms.TimeInput)
    name = forms.CharField(max_length=100)
    customer_address = forms.CharField(max_length=200)
    pickup_address = forms.CharField(max_length=200)
    dropoff_address = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=20)
    dl = forms.CharField(max_length=20)
    jumpstart = forms.BooleanField(required=False)
    tow = forms.BooleanField(required=False)
    tirechange = forms.BooleanField(required=False)
    lockout = forms.BooleanField(required=False)
    year = forms.CharField(max_length=20)
    make = forms.CharField(max_length=50)
    color = forms.CharField(max_length=50)
    model = forms.CharField(max_length=50)
    license_no = forms.CharField(max_length=20)

    # Fields from ReceiptPart3 model
    vin_number = forms.CharField(max_length=20)
    policy_number = forms.CharField(max_length=20)
    hook_up = forms.BooleanField(required=False)
    winch = forms.BooleanField(required=False)
    flares = forms.BooleanField(required=False)
    dollies = forms.BooleanField(required=False)
    scotch_blocks = forms.BooleanField(required=False)
    ramps = forms.BooleanField(required=False)
    snatch_blocks = forms.BooleanField(required=False)
    signature = forms.CharField(max_length=255)

    # Fields from ReceiptPart4 model
    mileage_start = forms.IntegerField()
    mileage_finish = forms.IntegerField()
    mileage_total = forms.IntegerField()
    labor_time_start = forms.TimeField(widget=forms.TimeInput)
    labor_time_finish = forms.TimeField(widget=forms.TimeInput)
    labor_time_total = forms.TimeField(widget=forms.TimeInput)
    extra_person_start = forms.TimeField(widget=forms.TimeInput)
    extra_person_finish = forms.TimeField(widget=forms.TimeInput)
    extra_person_total = forms.TimeField(widget=forms.TimeInput)
    towing_charge = forms.DecimalField(max_digits=8, decimal_places=2)
    mileage_charge = forms.DecimalField(max_digits=8, decimal_places=2)
    labor_charge = forms.DecimalField(max_digits=8, decimal_places=2)
    extra_person_charge = forms.DecimalField(max_digits=8, decimal_places=2)
    special_equipment_charge = forms.DecimalField(max_digits=8, decimal_places=2)
    storage_charge = forms.DecimalField(max_digits=8, decimal_places=2)
    subtotal = forms.DecimalField(max_digits=8, decimal_places=2)
    tax = forms.DecimalField(max_digits=8, decimal_places=2)
    total = forms.DecimalField(max_digits=8, decimal_places=2)

    def save(self):
        part1 = ReceiptPart1.objects.create(
            customer_initial=self.cleaned_data['customer_initial'],
            damage_type=self.cleaned_data['damage_type'],
            description=self.cleaned_data['description'],
        )

        part2 = ReceiptPart2.objects.create(
            time_of_call=self.cleaned_data['time_of_call'],
            date_in=self.cleaned_data['date_in'],
            date_out=self.cleaned_data['date_out'],
            time_start=self.cleaned_data['time_start'],
            time_finish=self.cleaned_data['time_finish'],
            name=self.cleaned_data['name'],
            customer_address=self.cleaned_data['customer_address'],
            pickup_address=self.cleaned_data['pickup_address'],
            dropoff_address=self.cleaned_data['dropoff_address'],
            phone=self.cleaned_data['phone'],
            dl=self.cleaned_data['dl'],
            jumpstart=self.cleaned_data['jumpstart'],
            tow=self.cleaned_data['tow'],
            tirechange=self.cleaned_data['tirechange'],
            lockout=self.cleaned_data['lockout'],
            year=self.cleaned_data['year'],
            make=self.cleaned_data['make'],
            color=self.cleaned_data['color'],
            model=self.cleaned_data['model'],
            license_no=self.cleaned_data['license_no']
        )

        part3 = ReceiptPart3.objects.create(
            vin_number=self.cleaned_data['vin_number'],
            policy_number=self.cleaned_data['policy_number'],
            hook_up=self.cleaned_data['hook_up'],
            winch=self.cleaned_data['winch'],
            flares=self.cleaned_data['flares'],
            dollies=self.cleaned_data['dollies'],
            scotch_blocks=self.cleaned_data['scotch_blocks'],
            ramps=self.cleaned_data['ramps'],
            snatch_blocks=self.cleaned_data['snatch_blocks'],
            signature=self.cleaned_data['signature']
        )

        part4 = ReceiptPart4.objects.create(
            mileage_start=self.cleaned_data['mileage_start'],
            mileage_finish=self.cleaned_data['mileage_finish'],
            mileage_total=self.cleaned_data['mileage_total'],
            labor_time_start=self.cleaned_data['labor_time_start'],
            labor_time_finish=self.cleaned_data['labor_time_finish'],
            labor_time_total=self.cleaned_data['labor_time_total'],
            extra_person_start=self.cleaned_data['extra_person_start'],
            extra_person_finish=self.cleaned_data['extra_person_finish'],
            extra_person_total=self.cleaned_data['extra_person_total'],
            towing_charge=self.cleaned_data['towing_charge'],
            mileage_charge=self.cleaned_data['mileage_charge'],
            labor_charge=self.cleaned_data['labor_charge'],
            extra_person_charge=self.cleaned_data['extra_person_charge'],
            special_equipment_charge=self.cleaned_data['special_equipment_charge'],
            storage_charge=self.cleaned_data['storage_charge'],
            subtotal=self.cleaned_data['subtotal'],
            tax=self.cleaned_data['tax'],
            total=self.cleaned_data['total'],
            created_at=timezone.now()
        )

        return [part1, part2, part3, part4]
