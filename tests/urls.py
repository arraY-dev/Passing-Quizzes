from django.urls import path, include

from . import views

app_name = 'tests'
urlpatterns = [
    # CRUD for quizzes
    path('', views.users_quizes, name='users_quizes'),
    path('quiz/<int:pk>/', views.detail_quiz, name='detail_quiz'),
    path('quiz/add/', views.quiz_add, name='quiz_add'),
    path('quiz/<int:pk>/question/add/', views.question_add, name='question_add'),
    path('quiz/<int:quiz_pk>/delete/', views.quiz_delete, name='quiz_delete'),
    path('quiz/<int:quiz_pk>/change/', views.quiz_change, name='quiz_change'),
    path('quiz/<int:pk>/passing', views.passing_quiz, name='passing_quiz'),
    path('profile/quiz/<int:pk>/', views.profile_quiz_detail, name='profile_quiz_detail'),

    # CRUD for comments
    path('quiz/<int:quiz_pk>/delete_comment/<int:pk>/', views.comment_delete, name='comment_delete'),
    path('quiz/<int:quiz_pk>/change_comment/<int:pk>/', views.comment_change, name='comment_change'),

]
