from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import AutoSlugField

STATUS_CHOICES = (
    ('Active', 'Active'),
    ('Inactive','Inactive'),
)

ROLE_CHOICES =(
    ('Owner','Owner'),
    ('Member','Member'),
)

class User(AbstractUser):
    phone_number = models.IntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=250, null=True, blank=True)
    user_profile_image = models.ImageField(upload_to='user', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Inactive')
    Role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')
    password = models.CharField(max_length=255)
    password_confirm = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')
    timestamp=models.DateTimeField(auto_now_add=True, editable=False)
    utimestamp=models.DateTimeField(auto_now=True, editable=False)
    track=models.TextField(blank=True)
    utrack=models.TextField(blank=True)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='Inactive')

    def __str__(self):
        return self.name
    
    
class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    timestamp=models.DateTimeField(auto_now_add=True, editable=False)
    utimestamp=models.DateTimeField(auto_now=True, editable=False)
    track=models.TextField(blank=True)
    utrack=models.TextField(blank=True)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='Inactive')


    def __str__(self):
        return self.name 
    

class Post(models.Model):
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    slug = AutoSlugField(populate_from='title')
    timestamp=models.DateTimeField(auto_now_add=True, editable=False)
    utimestamp=models.DateTimeField(auto_now=True, editable=False)
    feature_image = models.ImageField(upload_to='post/feature_image')
    thumbnail_image = models.ImageField(upload_to='post/thumbnail_image')
    published_date = models.DateTimeField()
    track=models.TextField(blank=True)
    utrack=models.TextField(blank=True)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='Inactive')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments",on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name="replies", on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=False, null=True, blank=True)
    text = models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True, editable=False)
    utimestamp=models.DateTimeField(auto_now=True, editable=False)
    track=models.TextField(blank=True)
    utrack=models.TextField(blank=True)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='Inactive')

    def __str__(self):
        return  self.text
       

        
    




