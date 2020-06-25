from django.urls import path
from . import views


urlpatterns = [
    path('class/enrollment/', views.enrollment, name='enrollment'),
]