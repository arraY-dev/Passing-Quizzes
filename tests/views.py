from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .utilities import show_result
from accounts.forms import SearchForm
from .forms import *


@login_required(login_url='accounts:login')
def comment_delete(request, quiz_pk, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Комментарий удалён')
        if request.user.pk == comment.quiz.user.pk:
            return redirect('tests:profile_quiz_detail', quiz_pk)
        else:
            return redirect('tests:detail_quiz', quiz_pk)
    else:
        context = {'comment': comment}
        return render(request, 'tests/comments/comment_delete.html', context)


@login_required(login_url='accounts:login')
def comment_change(request, quiz_pk, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = UserCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Комментарий исправлен')
            return redirect('tests:profile_quiz_detail', quiz_pk)
    else:
        form = UserCommentForm(instance=comment)
    context = {'comment': comment, 'form': form}
    return render(request, 'tests/comments/comment_change.html', context)


@login_required(login_url='accounts:login')
def passing_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = Question.objects.filter(quiz=quiz)
    questions_with_answers = dict()

    for question in questions:
        questions_with_answers[question] = question.answers.all().values_list('is_correct', 'text')

    if request.method == 'POST':
        context = show_result(request, questions, quiz, questions_with_answers)
        return render(request, 'tests/passing_result.html', context)

    context = {'quiz': quiz, 'questions': questions, 'answers': questions_with_answers}
    return render(request, 'tests/passing_quiz.html', context)


@login_required(login_url='accounts:login')
def detail_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = Question.objects.filter(quiz=quiz)
    last_res = PassedUserQuiz.objects.all().filter(user=request.user.pk, quiz=quiz).values('score')
    percent = PassedUserQuiz.objects.all().filter(user=request.user.pk, quiz=quiz).values('percent')
    questions_with_answers = dict()
    for question in questions:
        questions_with_answers[question] = question.answers.all().values_list('is_correct', 'text')
    comments = Comment.objects.filter(quiz=pk)
    initial = {'quiz': quiz.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.pk
        form_class = UserCommentForm
    form = form_class(initial=initial)
    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Комментарий добавлен')
            return redirect('tests:detail_quiz', pk)
        else:
            form = c_form
            messages.add_message(request, messages.WARNING, 'Комментарий не добавлен')
    context = {'quiz': quiz, 'questions': questions, 'answers': questions_with_answers, 'last_res': last_res,
               'percent': percent, 'comments': comments, 'form': form}
    return render(request, 'tests/detail_quiz.html', context)


@login_required(login_url='accounts:login')
def profile_quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = Question.objects.filter(quiz=quiz)
    questions_with_answers = dict()
    for question in questions:
        questions_with_answers[question] = question.answers.all().values_list('is_correct', 'text')
    comments = Comment.objects.filter(quiz=pk)
    initial = {'quiz': quiz.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.pk
        form_class = UserCommentForm
    form = form_class(initial=initial)
    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Комментарий добавлен')
            return redirect('tests:profile_quiz_detail', pk)
        else:
            form = c_form
            messages.add_message(request, messages.WARNING, 'Комментарий не добавлен')
    context = {'quiz': quiz, 'questions': questions, 'answers': questions_with_answers, 'comments': comments,
               'form': form}
    return render(request, 'tests/detail_user_quiz.html', context)


@login_required(login_url='accounts:login')
def question_add(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            formset = AnswersFormset(request.POST, instance=question)
            if formset.is_valid():
                question.save()
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Вопрос добавлен')
                return redirect('tests:profile_quiz_detail', pk)
    else:
        form = QuestionForm(initial={'quiz': quiz.pk})
        formset = AnswersFormset()
    context = {'form': form, 'formset': formset}
    return render(request, 'tests/add_user_question_answers.html', context)


@login_required(login_url='accounts:login')
def quiz_delete(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    if request.method == 'POST':
        quiz.delete()
        messages.add_message(request, messages.SUCCESS, 'Тест удалён')
        return redirect('tests:users_quizes')
    else:
        context = {'quiz': quiz}
        return render(request, 'tests/quiz_delete.html', context)


@login_required(login_url='accounts:login')
def users_quizes(request):
    quizes = Quiz.objects.filter(user=request.user)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword)
        quizes = quizes.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    context = {'form': form, 'quizes': quizes}
    return render(request, 'tests/user_quizes.html', context)


@login_required(login_url='accounts:login')
def quiz_change(request, quiz_pk):
    quiz = get_object_or_404(Quiz, id=quiz_pk)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        formset = QuestionFormset(request.POST, instance=quiz)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('tests:profile_quiz_detail', quiz.pk)
    else:
        form = QuizForm(instance=quiz)
        formset = QuestionFormset(instance=quiz)
    context = {'form': form, 'formset': formset}
    return render(request, 'tests/change_quiz.html', context)


@login_required(login_url='accounts:login')
def quiz_add(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            formset = QuestionFormset(request.POST, instance=quiz)
            if formset.is_valid():
                form.save()
                formset.save()
                return redirect('tests:users_quizes')
    else:
        form = QuizForm(initial={'user': request.user.pk})
        formset = QuestionFormset()
    context = {'form': form, 'formset': formset}
    return render(request, 'tests/create_user_quizes.html', context)
