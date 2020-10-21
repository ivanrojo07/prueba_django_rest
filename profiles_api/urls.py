from django.urls import path 
from django.views.decorators.csrf import csrf_exempt
from profiles_api.views import HelloApiView, get_token, RegisterView, LoginView, LogoutView,UserView
urlpatterns=[
    path("hello-view/",HelloApiView.as_view()),
    path('get-token/', csrf_exempt(get_token)),
    path("register/",RegisterView.as_view()),
    path("login/",LoginView.as_view()),
    path("logout/",LogoutView.as_view()),
    path("user/",UserView.as_view())

]