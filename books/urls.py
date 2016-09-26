from django.conf.urls import url

from . import views

urlpatterns = [
    # pattern, handler, name
    url(r'^$', views.index, name='index'),
    url(r'unread', views.unread, name='unread'),
]
