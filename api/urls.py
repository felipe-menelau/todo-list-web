from django.conf.urls import url
from .views import task_views, todo_views, user_views, pdf_views

urlpatterns = [
    url(r'api/users$', user_views.UserCreate.as_view(), name='user-create'),
    url(r'api/users/activate$', user_views.UserActivate.as_view(), name='user-activate'),
    url(r'api/users/forgot$', user_views.UserPasswordManagement.as_view(), name='user-forgot'),
    url(r'api/todo/(?P<pk>[0-9]+)/tasks/$', task_views.TaskCreation.as_view(), name='tasks'),
    url(r'api/todo/(?P<pk>[0-9]+)/tasks/(?P<pk_task>[0-9]+)/$', task_views.TaskManagement.as_view(), name='task-detail'),
    url(r'api/todo/(?P<pk>[0-9]+)/pdf$', pdf_views.PdfExport.as_view(), name='todo-pdf'),
]
