from django.urls import path
from . import views
urlpatterns = [
    path(r'p1/', views.p1),
    path(r'p2/', views.p2),
]
