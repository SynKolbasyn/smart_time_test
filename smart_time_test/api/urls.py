from django.urls import path

from api.views import UserView


urlpatterns = [
    path("users/<int:id>/", UserView.as_view()),
]
