from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, TextInput, SelectDateWidget, CheckboxInput
from django.forms.models import BaseInlineFormSet

from .middlewares import help_text
from .models import Profile, Question, Answer, Quiz, Comment


class ChangeQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description')


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {'quiz': forms.HiddenInput, 'author': forms.HiddenInput}


AnswersFormset = inlineformset_factory(Question, Answer, fields='__all__', extra=4,
                                       widgets={'text': TextInput(attrs={'required': True})})

AnswersEditFormset = inlineformset_factory(Question, Answer, fields=('text', 'is_correct'), extra=4)


class BaseChildrenFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseChildrenFormset, self).__init__(*args, **kwargs)

    def add_fields(self, form, index):
        super(BaseChildrenFormset, self).add_fields(form, index)

        # save the formset in the 'nested' property
        form.answer = AnswersEditFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='address-%s-%s' % (
                form.prefix,
                AnswersEditFormset.get_default_prefix()))


QuestionFormset = inlineformset_factory(Quiz, Question, fields='__all__', formset=BaseChildrenFormset,
                                        min_num=5, widgets={'text': TextInput(attrs={'required': False})})


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description')


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        widgets = {'quiz': forms.HiddenInput}


class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20, label='')


AIFormSet = inlineformset_factory(User, Profile, fields='__all__',
                                  widgets={'birth_date': SelectDateWidget(attrs={'required': True})})


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label="Логин**")
    first_name = forms.CharField(required=True, label="Имя**", widget=forms.TextInput)
    last_name = forms.CharField(required=True, label='Фамилия**', widget=forms.TextInput)
    password1 = forms.CharField(label='Пароль*', widget=forms.PasswordInput,
                                help_text=help_text())
    password2 = forms.CharField(label='Пароль (повторно)**', widget=forms.PasswordInput,
                                help_text='Повторите пароль')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        list_username = User.objects.filter(username=username)
        if list_username.count():
            raise ValidationError('Такой логин уже занят')
        return username

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data and \
                self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError("Введенные пароли не совпадают")
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'last_name', 'first_name')


class LoginForm(forms.ModelForm):
    username = forms.CharField(required=True, label='Логин', widget=forms.TextInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        password = self.cleaned_data['password'].lower()
        check_user = User.objects.filter(username=username, password=password)
        if not check_user:
            raise ValidationError('Вы ввели неверный логин либо пароль')
        return username, password
