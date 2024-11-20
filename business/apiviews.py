from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from business.models import Business, FeedbackForm
from .serializers import BusinessSerializer, FeedbackFormSerializer

class BusinessApiViews(viewsets.ModelViewSet):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all()
   

class FeedbackFormApiViews(viewsets.ModelViewSet):
    serializer_class = FeedbackFormSerializer
    queryset = FeedbackForm.objects.all()
   