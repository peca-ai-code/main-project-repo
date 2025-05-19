from django.http import JsonResponse
from django.shortcuts import redirect

def health_check(request):
    """Health check endpoint for API."""
    return JsonResponse({"status": "ok", "message": "API is running"})

def redirect_to_admin(request):
    """Redirect root URL to admin interface."""
    return redirect('admin:index')
