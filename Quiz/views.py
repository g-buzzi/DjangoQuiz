from datetime import datetime
from urllib import response
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from .forms import *
import json

def home(request):
    quizzes = Quiz.objects.all()
    context = {'quizzes': quizzes}
    return render(request,'Quiz/home.html', context)

def quizDetails(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    leaderboard = []
    position = 1
    attempts = sorted(quiz.attempt_set.all(), key=lambda x: x.total_time(), reverse=True)
    attempts = sorted(attempts, key=lambda x: x.n_points(), reverse=True)
    for attempt in attempts:
        leaderboard.append({"position": position, "name": attempt.name, "score": attempt.n_points(), "time": attempt.total_time()})
    context = {'quiz': quiz, "n_questions": len(quiz.question_set.all()), "leaderboard": leaderboard}
    return render(request,'Quiz/details.html',context)

def start(request, quiz_id):
    quiz = Quiz.objects.get(pk= quiz_id)
    if request.method == 'POST':
        form = request.POST
        if form['name'] != "":
            attempt = Attempt(quiz = quiz, name = form['name'], start_time = datetime.now(), current_question = 0)
            attempt.save()
            return HttpResponseRedirect('/attempt/{}'.format(attempt.id))
    else:
        form = NameForm()
    return render(request, 'Quiz/start.html', {'form': form, "quiz": quiz})

def attempt(request, attempt_id):
    # if finished: show result.
    attempt = Attempt.objects.get(pk=attempt_id)
    quiz = attempt.quiz
    if attempt.current_question >= len(quiz.question_set.all()): #Show Results
        answers = []
        for answer in attempt.answer_set.all():
            answer_data = {"question": answer.question.question, "correct": answer.answer == answer.question.ans,
                           "answered": getattr(answer.question, "op" + str(answer.answer)), "correct_answer": getattr(answer.question, "op" + str(answer.question.ans))}
            answers.append(answer_data)
            context = {'attempt': attempt, 'answers': answers}
        return render(request, 'Quiz/result.html', context)
    else:
        context = {'question': quiz.question_set.all()[attempt.current_question], 'attempt': attempt}
        return render(request, 'Quiz/attempt.html', context)
        pass

def answer(request, attempt_id):
    if request.method == 'POST':
        attempt = Attempt.objects.get(pk=attempt_id)
        question = attempt.quiz.question_set.all()[attempt.current_question]
        answer = Answer(attempt= attempt, question= question, answer= int(request.POST["answer"]))
        answer.save()
        attempt.current_question = attempt.current_question + 1
        if(attempt.current_question == len(attempt.quiz.question_set.all())):
            attempt.end_time = datetime.now()
        attempt.save()
        return HttpResponseRedirect('/attempt/{}'.format(attempt.id))
        response = ({"answer":int(request.POST["answer"]), "correct answer": question.ans, "point": int(request.POST["answer"]) == question.ans})
        # return HttpResponse(json.dumps(response), content_type="application/json")

