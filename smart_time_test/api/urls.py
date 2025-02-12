from django.urls import path

from api.views import RegisterView, UserView


urlpatterns = [
    path("users/<int:id>/", UserView.as_view()),
    path("register/", RegisterView.as_view()),
]
