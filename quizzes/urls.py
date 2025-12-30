from django.urls import path
from .views import QuizListView, QuizDetailView, QuizSubmitView

urlpatterns = [
    path("quizzes/", QuizListView.as_view()),
    path("quizzes/<slug:slug>/", QuizDetailView.as_view()),
    path("quizzes/<slug:slug>/submit/", QuizSubmitView.as_view()),
]
