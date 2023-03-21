from pdb import post_mortem
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.dispatch import receiver #add this
from django.db.models.signals import post_save #add this
# from django_extensions.db.fields import AutoSlugfield
from django_extensions.db.fields import AutoSlugField
# from taggit.managers import TaggableManager



gender = (
    ('Male','Male'),
    ('Female', 'Female'),
    ('Others','Others')
)
class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True, null=True, blank=True)

    def __str__(self):
        return self.title
    
class Tags(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True, null=True, blank=True)

    def __str__(self):
        return self.title
    


class User(AbstractUser):
    email = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=gender, default='Male')
    mobile_no = models.CharField(max_length=14)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=200)
    image = models.ImageField(upload_to='profile/')
    # slug=AutoSlugField(populate_form= 'user', unique=True, null=True, default=None)

    def __str__(self):
        return self.email


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True, null=True, default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # body = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags)
    text = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    featured_image = models.ImageField(upload_to='featured_image/%Y/%m/%d/', null=True, blank=True) #this
    thumbnail_image = models.ImageField(upload_to='thumbnail_image/%Y/%m/%d/', null=True, blank=True)
  

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255,  null=True, blank=True)
    text = models.TextField(max_length=255,  null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete= models.CASCADE, related_name='replies')


    class Meta:
      ordering=('-created_date',)
    
    def __str__(self):
        return self.name
    
    
    @property
    def children(self):
        return Comments.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    




