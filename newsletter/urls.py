from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-user/', views.add_user, name='add_user'),
    path('send-newsletter/', views.send_newsletter, name='send_newsletter'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('newsletter-sent-callback/', views.newsletter_sent_callback, name='newsletter_sent_callback'),
    path('history/', views.newsletter_history, name='history'),
]