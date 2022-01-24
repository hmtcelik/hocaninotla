from django.urls import path
from . import views
from . import models

app_name = 'comment'

urlpatterns = [
    path('', views.UniView.as_view(), name='uni'),
    path('university/<int:pk>/', views.FacultyView.as_view(), name='faculty'),
    path('faculty/<int:pk>/', views.DepartView.as_view(), name='depart'),
    path('depart/<int:pk>/', views.DoctorView.as_view(), name='doctor'),
    path('doctor/<int:pk>/', views.CommentView.as_view(), name='comment'),
]


