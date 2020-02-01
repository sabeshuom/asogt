from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit_registration/', views.submit_registration, name="submit_registration"),
]
