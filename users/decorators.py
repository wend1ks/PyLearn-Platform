from django.shortcuts import redirect

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "admin":
            return redirect("users:signin")
        return view_func(request, *args, **kwargs)
    return wrapper



