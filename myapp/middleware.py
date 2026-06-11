import time
from django.http import HttpResponseForbidden

class LogRequestMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        #prcoess before
        print(f"[Middleware] Request Path:{request.path}")
        response = self.get_response(request)

        # process after view 
        print(f"[Middleware] Response Status:{response.status_code}")
        return response
    

class TimerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        end_time = time.time()
        total_time = end_time - start_time

        print(f"[Timer Middleware] {request.path} took {total_time:.4f} seconds")

        return response
    



# class BlockIPMiddleware:
#     BLOCKED_IPS = [
#         '127.0.0.1',
#         '192.168.1.100',
#     ]

#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         ip = request.META.get('REMOTE_ADDR')

#         if ip in self.BLOCKED_IPS:
#             return HttpResponseForbidden("Your IP address has been blocked.")

#         response = self.get_response(request)
#         return response