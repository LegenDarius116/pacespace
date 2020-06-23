from django.urls import path
from . import views


urlpatterns = [
    path('schoolclass/all/', views.all_schoolclass, name='all_schoolclass'),
    path('schoolclass/<int:pk>/', views.view_schoolclass, name='view_schoolclass'),
]