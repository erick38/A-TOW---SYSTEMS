from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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
from django.views import View
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from towingapp.forms import MessageForm
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
        return HttpResponseRedirect(reverse('page'))
    else:
        conversations = user.conversations.all()
        current_conversation = None
        messages = None

        if 'conversation_id' in request.GET:
            conversation_id = request.GET['conversation_id']
            try:
                current_conversation = Conversation.objects.get(id=conversation_id)
                messages = current_conversation.messages.all()
            except Conversation.DoesNotExist:
                messages = None
                current_conversation = None

        if request.method == 'POST':
            form = MessageForm(request.POST, user=user)
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = user
                message.conversation = current_conversation
                message.save()
        else:
            form = MessageForm(user=user)

        context = {
            'user': user,
            'conversations': conversations,
            'current_conversation': current_conversation,
            'messages': messages,
            'form': form,  # include the form in the context
        }

        return render(request, 'customertask.html', context)



class ConversationForm(forms.ModelForm):
    message = forms.CharField(max_length=1000, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        username = kwargs.pop('username', None)
        exclude_sender = kwargs.pop('exclude_sender', False)
        super().__init__(*args, **kwargs)
        if username is not None:
            user = get_object_or_404(MyUser, username=username)
            queryset = MyUser.objects.exclude(id=user.id)
            if exclude_sender:
                queryset = queryset.exclude(id=self.request.user.id)
            self.fields['participants'].queryset = queryset

    class Meta:
        model = Conversation
        fields = ['participants']

    def save(self, commit=True, request=None):
        conversation = super().save(commit=False)
        if commit:
            conversation.save()

        # create the message with the conversation and the sender
        if request is not None and request.user is not None:
            Message.objects.create(conversation=conversation, sender=request.user, message=self.cleaned_data['message'])

        return conversation


class ConversationView(LoginRequiredMixin, FormMixin, DetailView):
    model = Conversation
    template_name = 'conversation.html'
    form_class = MessageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversation = self.get_object()
        context['messages'] = conversation.messages.all().order_by('-created_at')
        context['message_form'] = self.get_form()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class CreateConversationView(LoginRequiredMixin, FormView):
    template_name = 'generic_form.html'
    form_class = ConversationForm

    def form_valid(self, form):
        conversation = form.save(commit=False)
        conversation.save()
        conversation.participants.add(self.request.user)
        form.save(commit=True, request=self.request)
        success_url = reverse_lazy('conversation', kwargs={'username': self.request.user.username, 'pk': conversation.pk})
        return HttpResponseRedirect(success_url)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Exclude sender user from the participants field choices
        form.fields['participants'].queryset = form.fields['participants'].queryset.exclude(id=self.request.user.id)
        return form
    

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
\
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