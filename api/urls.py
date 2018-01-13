from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'api/users$', views.UserCreate.as_view(), name='user-create'),
    url(r'api/users/activate$', views.UserActivate.as_view(), name='user-activate'),
    url(r'api/users/forgot$', views.UserPasswordManagement.as_view(), name='user-forgot'),
]
