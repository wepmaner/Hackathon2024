from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.utils import timezone
from .managers import CustomUserManager
# Create your models here.


class Team(AbstractBaseUser,PermissionsMixin):
    #user = models.OneToOneField(User,blank=True,null=False,on_delete=models.CASCADE)
    login = models.CharField(max_length=255,unique=True)
    email = models.EmailField(max_length=255,unique=True,blank=False, null=False)
    emailConfirm = models.BooleanField(default=False)
    team_name = models.CharField(max_length=20,blank=False,null=False)
    photo = models.ImageField(upload_to='team_photos/', null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    rating = models.FloatField(null=True, blank=True)
    USERNAME_FIELD = 'login'
    objects = CustomUserManager()

class TeamRating(models.Model):
    from_team = models.ForeignKey(Team, related_name='from_team_ratings', on_delete=models.CASCADE)
    to_team = models.ForeignKey(Team, related_name='to_team_ratings', on_delete=models.CASCADE)
    design = models.FloatField(blank=False,null=False)
    usability = models.FloatField(blank=False,null=False)
    layout = models.FloatField(blank=False,null=False)
    implementation = models.FloatField(blank=False,null=False)

    class Meta:
        unique_together = ('from_team', 'to_team')

class UserInfo(models.Model):
    team = models.ForeignKey(Team, blank=False,null=False,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=False)
    email = models.EmailField(max_length=255,unique=True,blank=False, null=False)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    about = models.CharField(max_length=255, null=True, blank=True)

class EmailConfirm(models.Model):
    team = models.ForeignKey(Team, blank=False, null=False, on_delete=models.CASCADE)
    code = models.IntegerField()
    
class Question(models.Model):
    user = models.ForeignKey(UserInfo, blank=True, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,blank=False, null=False)
    email = models.EmailField(max_length=255,blank=False, null=False)
    text = models.CharField(max_length=255,blank=False, null=False)
    answer = models.CharField(max_length=255,blank=True, null=True)

