from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [ 
    path('', views.UniView.as_view(), name='university'),
    path('<int:pk>/', views.FacultyView.as_view(), name='faculty'),
    path('<int:pk>/', views.DepartmantView.as_view(), name='departmant'),      
       
]
