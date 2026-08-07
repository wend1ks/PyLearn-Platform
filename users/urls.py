from django.urls import path,include
from users.views import *
from .views import ProfileView


app_name = 'users'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", profile_edit, name="profile_edit"),

]
