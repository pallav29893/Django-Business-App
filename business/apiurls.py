from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .apiviews import BusinessApiViews, FeedbackFormApiViews

router = SimpleRouter()
router.register('get-businesses', BusinessApiViews)
router.register('get-feedbackforms', FeedbackFormApiViews)


urlpatterns = [
    # path('', include(router.urls)),
]
urlpatterns = router.urls
