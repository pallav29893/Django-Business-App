from django.db import models
from blog.models import User

STATUS_CHOICES = (
    ('Active', 'Active'),
    ('Inactive','Inactive'),
)
    
class Business(models.Model):
    teamMember = models.ManyToManyField(User)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=250, null=True, blank=True)
    logo = models.ImageField(upload_to='logo')
    created_at=models.DateTimeField(auto_now_add=True, editable=False)
    updated_at=models.DateTimeField(auto_now=True, editable=False)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='Inactive')

    def __str__(self):
        return self.name 
    
    
class FeedbackForm(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return self.name
    
class Feedback(models.Model):
    business = models.ForeignKey(Business,on_delete=models.CASCADE)
    form_type = models.ForeignKey(FeedbackForm,on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    rating = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.IntegerField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True, editable=False)
    updated_at=models.DateTimeField(auto_now=True, editable=False)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return self.name 
    
class TextQuestions(models.Model):
    form_type = models.ForeignKey(FeedbackForm,related_name='text_questions',on_delete=models.CASCADE)
    text = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True, editable=False)
    updated_at=models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.text 

class RateQuestions(models.Model):
    form_type = models.ForeignKey(FeedbackForm,related_name='rating_questions',on_delete=models.CASCADE)
    rating = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True, editable=False)
    updated_at=models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.rating