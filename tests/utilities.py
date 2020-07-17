from django.core.exceptions import ObjectDoesNotExist

from .models import PassedUserQuiz


def show_result(request, questions, quiz, questions_with_answers):
    count_questions = questions.count()
    score = 0
    for k, v in request.POST.items():
        v = v.split(',')
        v = v[0].replace('(', '')
        if v == 'True':
            score += 1
    percent_res = round((score / count_questions) * 100)
    quiz.counter_pass += 1
    try:
        passed = PassedUserQuiz.objects.get(user=request.user, quiz=quiz)
        passed.user = request.user
        passed.quiz = quiz
        passed.score = score
        passed.percent = percent_res
        passed.save()
    except ObjectDoesNotExist:
        passed = PassedUserQuiz(user=request.user, quiz=quiz, score=score, percent=percent_res)
        passed.save()
    quiz.save()
    context = {'quiz': quiz, 'questions': questions, 'answers': questions_with_answers, 'percent_res': percent_res,
               'score': score}
    return context
