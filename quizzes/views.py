from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Quiz, Question, Choice, Submission, Answer
from .serializers import (
    QuizListSerializer,
    QuizDetailSerializer,
    SubmissionRequestSerializer,
)


class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.filter(is_active=True)
    serializer_class = QuizListSerializer


class QuizDetailView(generics.RetrieveAPIView):
    lookup_field = "slug"
    queryset = Quiz.objects.filter(is_active=True)
    serializer_class = QuizDetailSerializer


class QuizSubmitView(APIView):
    def post(self, request, slug):
        quiz = get_object_or_404(Quiz, slug=slug, is_active=True)

        serializer = SubmissionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        submission = Submission.objects.create(
            quiz=quiz, respondent_identifier=data.get("respondent_identifier", "")
        )

        score = 0
        total = quiz.questions.count()

        for item in data["answers"]:
            question = get_object_or_404(Question, id=item["question_id"], quiz=quiz)

            selected_choice = None
            is_correct = False

            if item.get("selected_choice_id"):
                selected_choice = get_object_or_404(
                    Choice,
                    id=item["selected_choice_id"],
                    question=question,
                )
                is_correct = selected_choice.is_correct

            Answer.objects.create(
                submission=submission,
                question=question,
                selected_choice=selected_choice,
                text_answer=item.get("text_answer", ""),
                is_correct=is_correct,
            )

            if is_correct:
                score += 1

        return Response(
            {
                "submission_id": str(submission.id),
                "score": score,
                "total_questions": total,
            },
            status=status.HTTP_201_CREATED,
        )
