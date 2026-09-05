from django.urls import path
from . import views

urlpatterns = [
    path("",views.Home,name='Home'),
    path("all_heart_view/",views.all_heart_view,name='all_heart_view'),
    path("report/<int:pk>/",views.download_report,name='download_report'),
    path("About/",views.About,name='About'),
    path("register/",views.register,name='register'),
]
