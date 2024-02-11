from django.http import JsonResponse


def health_check(request):
    """Health Check endpoint"""
    
    return JsonResponse({'status': 'ok'})
