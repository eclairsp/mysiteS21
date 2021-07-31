from django.urls import path
from myapp import views

app_name = 'myapp'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about', views.about, name='about'),
    path(r'findcourses', views.findcourses, name='find_courses'),
    path(r'place_order', views.place_order, name='place_order'),
    path(r'review', views.review, name='review'),
    path(r'login', views.user_login, name='login'),
    path(r'logout', views.user_logout, name='logout'),
    path(r'myaccount', views.myaccount, name='myaccount'),
    path(r'<topic_id>', views.details, name='details'),
]
