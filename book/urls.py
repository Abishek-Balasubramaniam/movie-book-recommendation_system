from django.urls import path
from . import views

app_name = 'book'

urlpatterns = [
    path('', views.recommend_book, name="recommend_book"),
    path('/about', views.about, name = "about"),
]