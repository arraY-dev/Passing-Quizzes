from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import RegisterUserForm, LoginForm, UserForm, AIFormSet, SearchForm
from tests.models import Quiz



def index(request):
    quizes = Quiz.objects.all().annotate(questions_count=Count('questions')).filter(questions_count__gte=5) \
        .order_by('-created_at')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword)
        quizes = quizes.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    if 'check' in request.GET:
        check = request.GET['check']
        if check is None:
            quizes = ''
        else:
            quizes = Quiz.objects.all().filter(passed_user_quizzes__user=request.user.pk)
            return render(request, 'accounts/layout/index.html', {'quizes': quizes, 'form': form})
    context = {'quizes': quizes, 'form': form}
    return render(request, 'accounts/layout/index.html', context)


@login_required(login_url='accounts:login')
def profile_change(request, pk):
    try:
        user = User.objects.get(id=pk)
        if request.method == "POST":
            form = UserForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                user = form.save()
                formset = AIFormSet(request.POST, request.FILES, instance=user)
                if formset.is_valid():
                    formset.save()
                    messages.add_message(request, messages.SUCCESS, 'Профиль исправлен')
                    return redirect('accounts:profile')
        else:
            form = UserForm(instance=user)
            formset = AIFormSet(instance=user)
        context = {'user': user, 'form': form, 'formset': formset}
        return render(request, 'change_user_info.html', context)
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>Профиль не найден</h2>")


@login_required(login_url='accounts:login')
def profileView(request):
    return render(request, 'profile.html')


def login_page(request):
    form = LoginForm
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return HttpResponseRedirect('../../admin/')
        elif user is not None:
            login(request, user)
            return redirect('accounts:profile')
        else:
            messages.info(request, 'Ви ввели невірний логін або пароль')

    context = {'form': form}
    return render(request, 'registration/login.html', context)


def registerView(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = RegisterUserForm()

    return render(request, 'registration/register.html', {'form': form})
