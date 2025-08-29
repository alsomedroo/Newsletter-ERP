from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
from .models import NewsletterUser, Newsletter
from .forms import UserCreationForm, NewsletterForm

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
def dashboard(request):
    users = User.objects.all().order_by('date_joined')
    newsletters = Newsletter.objects.all()[:5]  # Last 5 newsletters
    context = {
        'users': users,
        'newsletters': newsletters,
        'total_users': users.count(),
        'total_newsletters': Newsletter.objects.count(),
    }
    return render(request, 'newsletter/dashboard.html', context)

@user_passes_test(is_admin)
def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create NewsletterUser instance
            NewsletterUser.objects.create(user=user)
            messages.success(request, f'User {user.username} has been created successfully!')
            return redirect('newsletter:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'newsletter/add_user.html', {'form': form})

@user_passes_test(is_admin)
def send_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save()
            # Get all user emails
            users = User.objects.all()
            user_emails = []
            for user in users:
                if user.email:
                    user_emails.append({
                        'name': user.get_full_name() or user.username,
                        'email': user.email
                    })
            
            context = {
                'newsletter': newsletter,
                'user_emails': user_emails,
                'total_recipients': len(user_emails),
                'emailjs_service_id': settings.EMAILJS_SERVICE_ID,
                'emailjs_template_id': settings.EMAILJS_TEMPLATE_ID,
                'emailjs_public_key': settings.EMAILJS_PUBLIC_KEY,
            }
            return render(request, 'newsletter/send_newsletter.html', context)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NewsletterForm()
    
    return render(request, 'newsletter/create_newsletter.html', {'form': form})

@user_passes_test(is_admin)
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user.is_superuser:
            messages.error(request, 'Cannot delete superuser!')
        else:
            username = user.username
            user.delete()
            messages.success(request, f'User {username} has been deleted successfully!')
    return redirect('newsletter:dashboard')

@csrf_exempt
@require_http_methods(["POST"])
def newsletter_sent_callback(request):
    """Callback for when newsletter is successfully sent via EmailJS"""
    try:
        data = json.loads(request.body)
        newsletter_id = data.get('newsletter_id')
        if newsletter_id:
            newsletter = Newsletter.objects.get(id=newsletter_id)
            # Update sent timestamp or add any other logic
            messages.success(request, f'Newsletter "{newsletter.title}" sent successfully!')
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@user_passes_test(is_admin)
def newsletter_history(request):
    newsletters = Newsletter.objects.all()
    return render(request, 'newsletter/history.html', {'newsletters': newsletters})