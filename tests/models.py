from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, verbose_name="Тест", related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='authors')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Создан')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['-created_at']


class PassedUserQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, verbose_name='Пройденный тест',
                             related_name='passed_user_quizzes')
    score = models.IntegerField(default=0, verbose_name='Счет')
    percent = models.IntegerField(default=0, verbose_name='Процент')

    def __str__(self):
        return f"Пройденный тест '{self.quiz.title}' пользователя '{self.user.username}'"

    class Meta:
        verbose_name_plural = 'Пройденные тесты'
        verbose_name = 'Пройденный тест'


class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Заголовок', unique=True)
    description = models.TextField(default='', verbose_name='Описание теста')
    counter_pass = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Тест на тему '{self.title}'"

    class Meta:
        verbose_name_plural = 'Тесты'
        verbose_name = 'Тест'
        ordering = ['-created_at']


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Тест', related_name='questions')
    text = models.CharField(max_length=255, verbose_name='Вопрос')

    def __str__(self):
        return f"{self.text}"

    class Meta:
        verbose_name_plural = 'Вопросы'
        verbose_name = 'Вопрос'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос', related_name='answers')
    text = models.CharField(max_length=255, verbose_name='Вариант ответа')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ?')

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name_plural = 'Ответы'
        verbose_name = 'Ответ'
