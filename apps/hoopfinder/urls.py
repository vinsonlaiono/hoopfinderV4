from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^djan$', views.home),  
    url(r'^$', views.home),  
    url(r'^home$', views.home),  
    url(r'^home/test$', views.home_test),  
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
    # new routes after checkout
    url(r'^user/(?P<user_id>\d+)$', views.user_page),
    url(r'^user/(?P<user_id>\d+)/test$', views.user_page_test),
    url(r'^add_user_review$', views.add_user_review),
    url(r'^review/delete/(?P<id>\d+)/(?P<userid>\d+)$', views.delete_player_review),
    url(r'^user_dashboard$', views.userdashboard),
    url(r'^users/(?P<id>\d+)/messages$', views.chat_room),
    url(r'^reviews/(?P<user_id>\d+)/(?P<review_feed>\w+)$', views.ajaxReviews),
    url(r'^ajax_courts$', views.ajaxCourts),
    url(r'^updateUserInfo$', views.updateUser),
    url(r'^user/(?P<image_url>\w+)$', views.updateProfileImage),
    url(r'^followAPI/(?P<followed_id>\d+)/(?P<follower_id>\d+)$', views.follow_API),
] 