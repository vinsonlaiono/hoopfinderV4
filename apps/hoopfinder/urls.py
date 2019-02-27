from django.conf.urls import url

from . import views           # This line is new!
urlpatterns = [
    url(r'^djan$', views.index),  
    url(r'^home$', views.home),  
    url(r'^courts$', views.courts),
    url(r'^map$', views.map),
    url(r'^user_dashboard$', views.userdashboard),
    url(r'^registration$', views.registration),
    url(r'^register$', views.register),
    url(r'^login_post$', views.login_post),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^new_court$', views.new_court),
    url(r'^add_court$', views.add_court),
    url(r'^review_court$', views.review_court),
    url(r'^checkin$', views.checkin),
    url(r'^courts/(?P<id>\d+)$', views.show_court),
    # new routes after
    url(r'^user/(?P<user_id>\d+)$', views.user_page),
    url(r'^add_user_review$', views.add_user_review),
    url(r'^review/delete/(?P<id>\d+)/(?P<userid>\d+)$', views.delete_player_review),
    url(r'^user_dashboard$', views.userdashboard),
] 