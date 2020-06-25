from django.urls import path
from . import views


urlpatterns = [
    path('class/<int:pkclass>/project/<int:pkproject>', views.view_project, name='view_project'),
    path('class/<int:pk>/project/all', views.all_project, name='all_project'),
]