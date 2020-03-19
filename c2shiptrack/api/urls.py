from django.urls import path, include
from django.conf.urls import url
from .router import router
from . import viewsets

urlpatterns = [
    path(r'', include(router.urls)),
    url(r'login/(?P<username>.+)/(?P<password>.+)', viewsets.LoginViewset.login_by_email, name='login-by-email'),
    url(r'list_user/', viewsets.LoginViewset.list_user, name='list-all-user'),
    url(r'list_user/(?P<user_id>.+)', viewsets.LoginViewset.detail_user, name='list-all-user'),
    url(r'update_user/(?P<user_id>.+)', viewsets.LoginViewset.update_user, name='list-all-user'),
    # url(r'create_user/', viewsets.LoginViewset.create_user),
]
