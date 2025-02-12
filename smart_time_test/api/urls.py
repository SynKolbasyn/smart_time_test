from django.urls import path

from api.views import ExamsRegisterView, RegisterView


urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("register_for_exams/", ExamsRegisterView.as_view()),
]
