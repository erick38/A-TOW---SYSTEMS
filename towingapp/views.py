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
from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from towingapp.forms import MessageForm, ConversationForm
from towingapp.models import Message, Conversation
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Conversation, MyUser
from .forms import MessageForm

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


def CreateConversationView(request):
    if request.method == 'POST':
        form = ConversationForm(request, request.POST)
        if form.is_valid():
            conversation = form.save()
            return redirect(reverse('customertask', args=[request.user.username]))
    else:
        form = ConversationForm(request)
    return render(request, 'generic_form.html', {'form': form})


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

@admin_only
@login_required
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
@admin_only
@login_required
def page(request):
    sent_messages = Message.objects.filter(sender=request.user)
    return render(request, 'page.html', {'sent_messages': sent_messages})

@prevent_multiple_users
@login_required
@admin_only
def home(request):
        posts = Clock_in.objects.filter(clock_status='clock-in').order_by('-clock_time')
        clock_out = Clock_in.objects.filter(clock_status='clock-out').order_by('-clock_time')
        return render(request, 'homepage.html', {'posts': posts, 'clock_out': clock_out })