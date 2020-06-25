from django.urls import path
from . import views


urlpatterns = [
    path('class/all/', views.all_schoolclass, name='all_schoolclass'),
    path('class/<int:pk>/', views.view_schoolclass, name='view_schoolclass'),
]