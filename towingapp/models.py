from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.me

class MyUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

class Clock_in(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)
    STATUS_CHOICES = (
            ('clock-in', 'clock-in'),
            ('clock-out', 'clock-out'),
            )
    clock_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='clock-in', null=False)

    clock_time = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.clock_status


class Home(models.Model):
    name = models.CharField(max_length=25)
    greetings_0 = models.CharField(max_length=20)
    greetings_1 = models.CharField(max_length=20)
    greetings_2 = models.CharField(max_length=24)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# ABOUT SECTION

class About(models.Model):
    heading = models.CharField(max_length=50)
    career = models.CharField(max_length=20)
    description = models.TextField(blank=False)
    profile_img = models.ImageField(upload_to='profile/')
    
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.career


class Profile(models.Model):
    about = models.ForeignKey(About,
                                on_delete=models.CASCADE)
    social_name = models.CharField(max_length=10)
    link = models.URLField(max_length=200)



# SKILLS SECTION

class Category(models.Model):
    name = models.CharField(max_length=20)

    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return self.name

class Skills(models.Model):
    category = models.ForeignKey(Category,
                                on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=60)

    

# PORTFOLIO SECTION

class Gallery(models.Model):
    image = models.ImageField(upload_to='portfolio/')
    link = models.URLField(max_length=200)

    def __str__(self):
        return f'Portfolio {self.id}'


class Mensaje(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=40)
    message = models.TextField(blank=False)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name