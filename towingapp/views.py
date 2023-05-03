from urllib import response
import uuid
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import Group
from towingapp.decorators import admin_only, prevent_multiple_users
from django.contrib.auth.models import Group
from django.test import Client
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render,HttpResponseRedirect, get_object_or_404, redirect, reverse
from towingapp.forms import add_AccountForm, addclockinform, login_form
from django.utils import timezone
from .models import MyUser, Conversation, Message, Clock_in
from django.views.generic.edit import FormView
from django import forms
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from towingapp.forms import MessageForm, ConversationForm
from towingapp.models import Message, Conversation
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Conversation, MyUser
from .forms import MessageForm
from .models import Receipt
from .forms import ReceiptForm
from django.http import JsonResponse
from .models import Coordinates

def save_location(request):
    if request.method == 'POST':
        # Generate UUID for the customer
        identifier = uuid.uuid4().hex
        # Get latitude and longitude from the browser geolocation API
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        # Check if latitude and longitude values are valid
        if not latitude or not longitude:
            return HttpResponseBadRequest('Latitude or longitude is missing')
        
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            return HttpResponseBadRequest('Latitude or longitude is not a valid number')
        # Create a new Coordinates object and save it to the database
        coordinates = Coordinates.objects.create(
            identifier=identifier,
            latitude=latitude,
            longitude=longitude
        )
        coordinates.save()
        # Redirect the customer to the success page
        print(coordinates.identifier,coordinates.latitude, coordinates.longitude, 'coordinates after saved')
        return redirect('success', identifier=identifier)
    
    # Render the page with a button to save the location
    print('coordinates here')
    return render(request, 'save_location.html')

def success(request, identifier):
    # Retrieve the Coordinates object using the provided identifier
    coordinates = Coordinates.objects.get(identifier=identifier)

    # Create the Google Maps URL
    maps_url = "https://www.google.com/maps/search/?api=1&query={},{}".format(coordinates.latitude, coordinates.longitude)

    # Render the success page with the Coordinates object and the maps_url variable
    return render(request, 'success.html', {'coordinates': coordinates, 'maps_url': maps_url})


@login_required
def combined_form(request):
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('submit')
    else:
        form = ReceiptForm()
    return render(request, 'generic_form.html', {'form': form})

@login_required
def submit(request):
    forms = Receipt.objects.all().order_by('-created_at')
    context = {'forms': forms}
    return render(request, 'submit.html', context)

@prevent_multiple_users
@login_required
def customer_task(request, username):
    user = get_object_or_404(MyUser, username=username)
    if request.user != user:
        return redirect('home')
    
    conversations = Conversation.objects.filter(participants=user)
    
    if request.method == 'POST':
        conversation_id = request.POST.get('conversation_id')
        message = request.POST.get('message')
        if conversation_id and message:
            conversation = get_object_or_404(Conversation, id=conversation_id, participants=user)
            message = Message.objects.create(sender=user, conversation=conversation, message=message)
            message.save()
    
    current_conversation_id = request.GET.get('conversation_id')
    current_conversation = None
    messages = None
    
    if current_conversation_id:
        current_conversation = get_object_or_404(Conversation, id=current_conversation_id, participants=user)
        messages = Message.objects.filter(conversation=current_conversation).order_by('-created_at')
    
    return render(request, 'customertask.html', {
        'user': user,
        'conversations': conversations,
        'current_conversation': current_conversation,
        'messages': messages
    })
@prevent_multiple_users
@login_required
def CreateConversationView(request):
    if request.method == 'POST':
        form = ConversationForm(request, request.POST)
        if form.is_valid():
            conversation = form.save()
            return redirect(reverse('customertask', args=[request.user.username]))
    else:
        form = ConversationForm(request)
    return render(request, 'generic_form.html', {'form': form})

@prevent_multiple_users
@login_required
class SendMessageView(LoginRequiredMixin, FormView):
    template_name = 'generic_form.html'
    form_class = MessageForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['conversation'] = Conversation.objects.get(title=self.request.GET['title'])
        kwargs['sender'] = self.request.user
        return kwargs

    def form_valid(self, form):
        message = form.save(commit=False)
        message.conversation = form.conversation
        message.sender = self.request.user
        message.save()
        return super().form_valid(form)


def login_view(request):
    if request.method == "POST":
        form = login_form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                     login(request, user)
                     return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
    form = login_form()
    return render(request, "genericform_login.html", {'form': form})
    

def logout_view(request):
    if request.method == "POST":
        logout(request)
    return HttpResponseRedirect(reverse('login_view'))

@prevent_multiple_users
@login_required
def profile_view(request, MyUser_str):
    user = get_object_or_404(MyUser, username=MyUser_str)
    if request.user != user:
        return HttpResponseRedirect(reverse('page'))
    else:
        my_user = MyUser.objects.get(username=MyUser_str)
        user_clockin = Clock_in.objects.filter(author=my_user)
        clock_in = user_clockin.filter(clock_status='clock-in').order_by('-clock_time')
        clock_out = user_clockin.filter(clock_status='clock-out').order_by('-clock_time')
        return render(request, "profile.html", {'user_clockin': user_clockin, 'clock_in':clock_in, 'clock_out':clock_out})

@prevent_multiple_users
@login_required
def add_clockin(request):
    timezone.activate('America/Chicago')
    if request.method == 'POST':
        form = addclockinform(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            clock_in = Clock_in.objects.create(
                clock_status=data['clock_status'],
                author=request.user,
                clock_time=timezone.now(),
            )
            username = request.user.username  # Get the username from the current user object
            return HttpResponseRedirect(reverse('profile', args=[username]))  # Pass the username as an argument
    else:
        form = addclockinform()
    return render(request, 'clock_statusform.html', {'form': form})
@prevent_multiple_users
@login_required
@admin_only
def add_AccountView(request):
    if request.method == 'POST':
        form = add_AccountForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = MyUser.objects.create_user(username=data['username'], password=data['password'])
            user.save()  # Save the user object
            # Add the user to the 'customer' group
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
    else:
        form = add_AccountForm()
    return render(request, 'generic_form.html', {'form': form})
    
def index(request):
    return render(request, 'index.html')
    
@admin_only
def home(request):
    posts = Clock_in.objects.filter(clock_status='clock-in').order_by('-clock_time')
    clock_out = Clock_in.objects.filter(clock_status='clock-out').order_by('-clock_time')
    # Get the most recent saved location for the current user
    coordinates = Coordinates.objects.filter().order_by('-created_at').all()
    if coordinates:
        maps_url = "https://www.google.com/maps/search/?api=1&query={},{}".format(coordinates[0].latitude, coordinates[0].longitude)
    else:
        maps_url = None
    return render(request, 'homepage.html', {'posts': posts, 'clock_out': clock_out, 'coordinates': coordinates, 'maps_url': maps_url })