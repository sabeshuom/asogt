from django.conf.urls import url

from . import views, login
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login_ajax/', login.login_ajax, name="login_ajax"),
    url(r'^logout_ajax/', login.logout_ajax, name="logout_ajax"),
    url(r'^is_authenticated/', login.is_authenticated, name="authentication"),
    url(r'^students/$', views.students_page, name='stundetns'),
    url(r'^competitions/$', views.competitions_page, name='competitions'),
    url(r'^results/$', views.results_page, name='results'),
    url(r'^get_competition_details/$', views.get_competition_details, name='get_competition_details'),
    url(r'^export_competition_details/$', views.export_competition_details, name='export_competition_details'),
    url(r'^get_results/$', views.get_results, name='get_results'),
    url(r'^export_results/$', views.export_results, name='export_results'),
    url(r'^get_student_details/$', views.get_student_details, name='get_student_details'),
]
