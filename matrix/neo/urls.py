# each appliction will have its URL file which will be called by the project
from django.urls import path

from neo import views

app_name = 'neo'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_logout/',views.user_login,name='user_login'),
    path('upload/',views.file_upload,name='file_upload'),
    path('dashboard/',views.file_dashboard,name='file_dashboard'),
    path('show_file/<path:file_path>/', views.show_file, name='show_file'),
    path('download_file', views.download_file, name='download_file' )
]