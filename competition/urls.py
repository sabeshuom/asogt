from django.conf.urls import url

from . import views, login
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login_ajax/', login.login_ajax, name="login_ajax"),
    url(r'^logout_ajax/', login.logout_ajax, name="logout_ajax"),
    url(r'^is_authenticated/', login.is_authenticated, name="authentication"),
    url(r'^students/$', views.students, name='stundetns'),
    url(r'^competitions/$', views.competitions, name='competitions'),
    url(r'^results/$', views.results, name='results'),
    url(r'^get_student_details/$', views.get_student_details, name='get_student_details'),
    url(r'^get_results/$', views.get_results, name='get_results'),
]
