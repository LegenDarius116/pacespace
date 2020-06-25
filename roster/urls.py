from django.urls import path
from . import views


urlpatterns = [
    path('class/<int:pk>/enrollment/', views.enrollment, name='enrollment'),
    path('class/<int:pk>/students/', views.students, name='students'),
]