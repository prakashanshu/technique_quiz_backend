from rest_framework import serializers
from .models import Quiz, Question, Choice, Submission, Answer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("id", "text")  # do NOT expose is_correct


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("id", "text", "question_type", "order", "choices")


class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ("id", "slug", "title", "description")


class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ("id", "slug", "title", "description", "questions")


class AnswerSubmitSerializer(serializers.Serializer):
    question_id = serializers.UUIDField()
    selected_choice_id = serializers.UUIDField(required=False, allow_null=True)
    text_answer = serializers.CharField(required=False, allow_blank=True)


class SubmissionRequestSerializer(serializers.Serializer):
    respondent_identifier = serializers.CharField(required=False, allow_blank=True)
    answers = AnswerSubmitSerializer(many=True)
