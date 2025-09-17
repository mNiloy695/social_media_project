from django.urls import path,include
from .views import RegistrationView,LoginView,ForgotPasswordView,ResetPasswordView,PasswordChangeView,LogoutView,UserDetailView


urlpatterns = [
    path('register/',RegistrationView.as_view()),
    path('<int:pk>/',UserDetailView),
    path('login/',LoginView.as_view()),
    path('forgot_password/',ForgotPasswordView.as_view()),
    path('reset_password/',ResetPasswordView.as_view()),
     path('passwordchange/<int:pk>/',PasswordChangeView.as_view()),
     path('logout/',LogoutView.as_view())
]
