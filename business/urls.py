from django.urls import path
from . import views

urlpatterns = [
    path('',views.business,name='business'),
    # path('feedback/',views.feedback,name='feedback'),
    path('logout/',views.logout_view,name='logout'),
    path('setup_feedback_form_details/<str:form_type>/',views.setupformdetails,name='setup_feedback_form_details'),
    path('addform/',views.addform,name='addform'),
    path('setup_feedback_form/',views.setupform,name='setup_feedback_form'),
    path('sign-up/', views.userSignUpViews, name='sign-up'),
    path('login/', views.login_view, name='login'),
    path('send-email/', views.send_email, name='send_email'),
    # path('customer_feedback/', views.customer_feedback, name='customer_feedback'),
    # path('customer_feedback/business/<int:business_id>/form/<int:form_id>/', views.customer_feedback, name='customer_feedback'),
    path('customer_feedback/business/<int:business_id>/form/<int:form_id>/<str:form_type>/', views.customer_feedback, name='customer_feedback'),
    path('business/download_feedbacks/', views.download_feedbacks_csv, name='download_feedbacks_csv'),
    path('team/',views.team,name='team'),
    # path('add-team-member/', views.add_team_member, name='add_team_member'),
    # path('delete-team-member/<int:member_id>/', views.delete_team_member, name='delete_team_member'),
    path('create-password/<str:uidb64>/<str:token>/', views.create_password, name='create_password'),
    # path('update-team-member/<int:member_id>/', views.update_team_member, name='update_team_member'),
    path('team/member/', views.manage_team_member, name='add_team_member'),  # View for adding a team member
    path('team/member/<int:member_id>/', views.manage_team_member, name='manage_team_member'),  # View for updating or deleting a team member
]

