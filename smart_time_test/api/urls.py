from django.urls import path

from api.views import (
    ExamRegisterView,
    ExamsView,
    ExamUnregisterView,
    RegisterView,
)


urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("register_for_exam/", ExamRegisterView.as_view()),
    path("unregister_for_exam/", ExamUnregisterView.as_view()),
    path("exams/", ExamsView.as_view()),
]
