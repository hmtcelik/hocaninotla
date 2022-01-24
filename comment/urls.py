from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('', views.UniView.as_view(), name='uni'),
    path('<int:pk>/', views.FacultyView.as_view(), name='faculty'), 
]

