from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from towingapp.decorators import admin_only
from towingapp.models import About, Category, Clock_in, Gallery, Home, Mensaje, MyUser, Profile
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render,HttpResponseRedirect, reverse
from towingapp.forms import AddmessageForm, add_AccountForm, addclockinform, login_form
from django.contrib.auth.models import Group
from django.contrib import messages

# Create your views here.
# @login_required
# def redirectpaypal(request):
#     # posts = post.objects.all()
#     return render(request, 'redirectpaypal.html')

@login_required
def page(request):
        return render(request, 'page.html')

def customer_task(request):
        return render(request, 'customertask.html')

@login_required
@admin_only
def home(request):
        posts = Clock_in.objects.filter(clock_status='clock-in')
        clock_out = Clock_in.objects.filter(clock_status='clock-out')
        return render(request, 'homepage.html', {'posts': posts, 'clock_out': clock_out })


def login_view(request):
    if request.method == "POST":
        form = login_form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect('homepage')
    form = login_form()
    return render(request, "generic_form.html", {'form': form})
    

def logout_view(request):
    if request.method == "POST":
        logout(request)
    return HttpResponseRedirect(reverse('login_view'))

@login_required
def profile_view(request, MyUser_id):
    my_user = MyUser.objects.get(username=MyUser_id)
    user_clockin = Clock_in.objects.filter(author=my_user)
    clock_in = user_clockin.filter(clock_status='clock-in')
    clock_out = user_clockin.filter(clock_status='clock-out')
    return render(request, "profile.html", {'user_clockin': user_clockin, 'clock_in':clock_in, 'clock_out':clock_out})


@login_required
def add_clockin(request):
    if request.method == 'POST':
        form = addclockinform(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # messages.error(request, 'you clocked in successfully')
            Clock_in.objects.create(
                 clock_status=data['clock_status'],
                #  author=MyUser.objects.all(),
                 )
            return HttpResponseRedirect(reverse('customertask'))
    form = addclockinform()
    return render(request, 'generic_form.html', {'form': form})

# @login_required
def add_AccountView(request):
    if request.method == 'POST':
        form = add_AccountForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user =  MyUser.objects.create_user(username=data['username'], password=data['password'])
            # group = Group.objects.get(name='customer')
            # user.groups.add(group)
            return HttpResponseRedirect(reverse('homepage'))
    form = add_AccountForm()
    return render(request, 'generic_form.html', {'form': form})


def add_message(request):
    if request.method == 'POST':
        form = AddmessageForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_post = Mensaje.objects.create(
                name=data['name'],
                 email=data['email'],
                message=data['message']
            )
            return HttpResponseRedirect(reverse('index'))

    form = AddmessageForm()
    return render(request, "generic_form.html", {'form': form})

def index(request):

    # Mensaje = Mensaje.objects.latest('date')
    # Home
    home = Home.objects.latest('updated')

    # About
    about = About.objects.latest('updated')
    profiles = Profile.objects.filter(about=about)

    # Skills
    categories = Category.objects.all()

    # Portfolio
    galleries = Gallery.objects.all()
    
    # mensajes = Mensaje
    # Mensajes = Mensaje.objects.all()


    context = {
        'home': home,
        'about': about,
        'profiles': profiles,
        'categories': categories,
        'galleries': galleries,
        # 'Mensaje': Mensaje,
    }
    return render(request, 'index.html', context)