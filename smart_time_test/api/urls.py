from django.urls import path

from api.views import ExamsRegisterView, RegisterView, UserView


urlpatterns = [
    path("users/<int:id>/", UserView.as_view()),
    path("register/", RegisterView.as_view()),
    path("register_for_exams/", ExamsRegisterView.as_view()),
]
