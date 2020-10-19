from django.urls import path 

from profiles_api.views import HelloApiView, login, RegisterView

urlpatterns=[
    path("hello-view/",HelloApiView.as_view()),
    path('login/', login),
    path("register/",RegisterView.as_view()),

]