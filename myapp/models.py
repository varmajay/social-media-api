from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import datetime
# Create your models here.

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations  =  True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    GENDER = (
        (0,'Male'),
        (1,'Female'),
        )
    ACCOUNT = (
        ('private','Private'),
        ('public','Public')
    )
    account = models.CharField(max_length=10, choices=ACCOUNT, default='public', null=True, blank=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,default=None,blank=True,null=True)
    gender = models.IntegerField(choices=GENDER,default=None,null=True,blank=True)
    address = models.TextField(default=None,blank=True,null=True)
    profile = models.FileField(upload_to='user',default='profile.png')
    bio =  models.TextField(max_length=200,default=None, null=True,blank=True)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return  self.name +" "+ self.email




class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(null=True, max_length=500)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return str(self.user)




class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.FileField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    likes = models.IntegerField(default=0)

    def __int__(self):
        return self.user


class Follower(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name= "user")
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name= "follower")
    def __str__(self):
        return self.follower.name




class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='comment_user')
    post=models.ForeignKey(Post,on_delete=models.CASCADE, related_name='post')
    comment=models.CharField(max_length=100)
    date=models.DateTimeField(auto_now_add=True) 
    
     
    def __str__(self):
        return self.user.name +'   '+ self.post.user.name



class LikePost(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.name