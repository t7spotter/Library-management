from django.urls import path

from lib_manage import views


urlpatterns = [
    path('get-post-person', views.GetPostPerson.as_view()),
    path('get-post-person/<int:pk>', views.GetPostPerson.as_view()),
    
    path('get-post-book', views.GetPostBook.as_view()),
    path('get-post-book/<int:pk>', views.GetPostBook.as_view()),
]
