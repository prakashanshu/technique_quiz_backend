import uuid
from django.db import models
from django.utils.text import slugify


class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Quiz.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = [
        ("mcq", "Multiple Choice"),
        ("true_false", "True / False"),
        ("text", "Text"),
    ]

    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Submission(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="submissions", on_delete=models.CASCADE)
    respondent_identifier = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission for {self.quiz.title}"


class Answer(models.Model):
    submission = models.ForeignKey(
        Submission, related_name="answers", on_delete=models.CASCADE
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(
        Choice, null=True, blank=True, on_delete=models.SET_NULL
    )
    text_answer = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer to {self.question.text[:30]}"
