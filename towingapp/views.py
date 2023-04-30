from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from towingapp.decorators import admin_only, prevent_multiple_users
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
from .models import ReceiptPart1, ReceiptPart2, ReceiptPart3, ReceiptPart4
# from twilio.rest import Client
from .forms import ReceiptForm

@prevent_multiple_users
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

@prevent_multiple_users
@login_required
def submit(request):
    part1 = ReceiptPart1.objects.all()
    print(part1)
    part2 = ReceiptPart2.objects.all()
    print(part2)
    part3 = ReceiptPart3.objects.all()
    print(part3)
    part4 = ReceiptPart4.objects.all()
    print(part4)
    form = {
        'part1': part1,
        'part2': part2,
        'part3': part3,
        'part4': part4,
    }
    return render(request, 'submit.html', {'form': form})

def location_view(request):
    if request.method == 'POST':
        # Get the latitude and longitude from the form data and save it to the database
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        # Save the location data to the database

    # Render the location page template
    return render(request, 'location.html')

# def send_location_request(phone_number):
#     account_sid = 'YOUR_ACCOUNT_SID'
#     auth_token = 'YOUR_AUTH_TOKEN'
#     client = Client(account_sid, auth_token)

#     message = client.messages.create(
#         body='Please click this link to share your location: https://example.com/location',
#         from_='YOUR_TWILIO_PHONE_NUMBER',
#         to=phone_number
#     )

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

@prevent_multiple_users
@login_required
def home(request):
        posts = Clock_in.objects.filter(clock_status='clock-in').order_by('-clock_time')
        clock_out = Clock_in.objects.filter(clock_status='clock-out').order_by('-clock_time')
        return render(request, 'homepage.html', {'posts': posts, 'clock_out': clock_out })
