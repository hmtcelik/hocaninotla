from django.urls import path
from . import views
from . import models

app_name = 'comment'

urlpatterns = [
    path('', views.HomeView.as_view(), name = 'home'),
    path('university/', views.UniView.as_view(), name='uni'),
    path('university/<int:pk>/', views.FacultyView.as_view(), name='faculty'),
    path('university/faculty/<int:pk>/', views.DepartView.as_view(), name='depart'),
    path('university/faculty/depart/<int:pk>/', views.DoctorView.as_view(), name='doctor'),
    path('university/faculty/depart/doctor/<int:pk>/', views.CommentView.as_view(), name='comment'),
    path("search/", views.searchbar, name="searchbar"),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),    
]


