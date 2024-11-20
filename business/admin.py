from django.contrib import admin
from .models import Business,Feedback,TextQuestions,RateQuestions,FeedbackForm

admin.site.register(Business)
admin.site.register(Feedback)
admin.site.register(TextQuestions)
admin.site.register(RateQuestions)
admin.site.register(FeedbackForm)