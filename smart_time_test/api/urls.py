from django.urls import path

from api.views import (
    ExamRegisterView,
    ExamsView,
    ExamUnregisterView,
    RegisterView,
    UserView,
)


urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("register_for_exam/", ExamRegisterView.as_view()),
    path("unregister_for_exam/", ExamUnregisterView.as_view()),
    path("exams/", ExamsView.as_view()),
    path("users/<int:id>/", UserView.as_view()),
]
