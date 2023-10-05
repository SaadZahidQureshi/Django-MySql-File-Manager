from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('login', views.Login, name='login'),
    path('signup', views.SignUp, name='signup'),
    path('index', views.Index, name='index'),
    path('logout', views.Logout, name='logout'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    # path('uploadfile', views.UploadFile, name='uploadfile'),

]