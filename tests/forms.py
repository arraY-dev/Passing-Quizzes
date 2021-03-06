from django import forms
from django.forms import inlineformset_factory, TextInput
from django.forms.models import BaseInlineFormSet

from .models import *


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {'quiz': forms.HiddenInput, 'author': forms.HiddenInput}


AnswersFormset = inlineformset_factory(Question, Answer, fields='__all__', extra=4,
                                       widgets={'text': TextInput(attrs={'required': True})})

AnswersEditFormset = inlineformset_factory(Question, Answer, fields=('text', 'is_correct'), extra=4, max_num=4)


class BaseChildrenFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseChildrenFormset, self).__init__(*args, **kwargs)

    def add_fields(self, form, index):
        super(BaseChildrenFormset, self).add_fields(form, index)

        # save the formset in the 'answer' property
        form.answer = AnswersEditFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='address-%s-%s' % (
                form.prefix,
                AnswersEditFormset.get_default_prefix()))

    def is_valid(self):
        result = super(BaseChildrenFormset, self).is_valid()
        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'answer'):
                    result = result and form.answer.is_valid()
        return result

    def save(self, commit=True):
        result = super(BaseChildrenFormset, self).save(commit=commit)
        for form in self.forms:
            if hasattr(form, 'answer'):
                if not self._should_delete_form(form):
                    form.answer.save(commit=commit)
        return result

    def clean(self):
        if any(self.errors):
            return

        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            question = form.cleaned_data.get('text')

            try:
                correct_answers = [correct.get('is_correct') for correct in form.answer.cleaned_data]
                for i in form.answer.cleaned_data:
                    if question and (len(i) < 5):
                        raise forms.ValidationError("Вопросы не могут быть без ответов.")
                    if question and not any(correct_answers):
                        raise forms.ValidationError("Вопрос должен иметь хоть один првильный ответ.")
            except AttributeError:
                raise forms.ValidationError("Вопросы не могут быть без ответов.")


QuestionFormset = inlineformset_factory(Quiz, Question, fields='__all__', formset=BaseChildrenFormset,
                                        min_num=5, widgets={'text': TextInput(attrs={'required': False})})


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('user', 'title', 'description')
        widgets = {'user': forms.HiddenInput}


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        widgets = {'quiz': forms.HiddenInput}
