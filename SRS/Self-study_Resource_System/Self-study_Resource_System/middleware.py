# def restrict_admin_ips(get_response):
#     def middleware(request):
#         allowed_ips = ['127.0.0.1', '::1']  # Add trusted IPs
#         if request.path.startswith('/admin') and request.META['REMOTE_ADDR'] not in allowed_ips:
#             from django.http import HttpResponseForbidden
#             return HttpResponseForbidden("Access Denied")
#         return get_response(request)
#     return middleware
