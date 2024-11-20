from django.urls import path
from . import views

urlpatterns = [
    path('category/<str:slug>/', views.category_post_list, name='category_post_list'),
    path('tag/<str:slug>/', views.tag_post_list, name='tag_post_list'),
    path('post/<str:slug>/edit/', views.post_edit, name='post_edit'),
    path('post/<str:slug>/', views.post_detail, name='post_detail'),
    path('profile-edit',views.profile_edit, name='profile_edit'),
    # path('sign-up/', views.userSignUpViews, name='sign-up'),
    path('profile/', views.profile_view, name='profile'),
    path('post-new/', views.post_new, name='post_new'),
    # path('logout/', views.logout_view, name='logout'),
    # path('login/', views.login_view, name='login'),
    path('', views.post_list, name='post_list'),
]