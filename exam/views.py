from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.sessions.models import Session
from exam.models import Solution,Question,Clock
from accounts.models import User


def Exam(request):
    return render(request,'accounts/login.html')


def online_mcq(request):
    current_user = request.user
    if current_user.is_staff == False:
        if request.method == 'GET':
            question = Question.objects.get(id=1)
            return render(request, 'exam/questions.html', {'question': question})
        if request.method == 'POST':
            if request.POST['id']:
                id = int(request.POST['id'])
                questions = Question.objects.all()
                flag = 0
                for question in questions:
                    try:
                        answer = request.POST[question.question]
                        solution = [question.question, answer]
                        flag = 1
                        break
                    except Exception:
                        pass
                if flag == 1:
                    # Use current_user instead of current_user.username
                    submit, created = Solution.objects.get_or_create(number=id, user=current_user)
                    submit.questions = solution[0]
                    submit.solution = solution[1]
                    submit.save()

                flag = 0
                try:
                    question = Question.objects.get(id=id + 1)
                    flag = 1
                except Exception:
                    pass

                if flag == 0:
                    submit = Solution.objects.filter(user=current_user)
                    # user_info = User.objects.get(username=current_user.username)
                    user_info = User.objects.get(email=current_user.email)

                    correct = 0
                    incorrect = 0
                    for i in range(len(submit)):
                        for j in range(len(questions)):
                            if submit[i].number == questions[j].id:
                                if submit[i].solution == questions[j].correct_answer:
                                    correct += 1
                                else:
                                    incorrect += 1

                    context = {
                        'email': user_info.email,
                        'contact_number': user_info.contact_number,
                        'first_name': user_info.first_name,
                        'last_name': user_info.last_name,
                        'correct': correct,
                        'incorrect': incorrect,
                        'unsolve': len(questions) - correct - incorrect
                    }
                    return render(request, 'exam/result.html', context)

                context = {
                    'question': question
                }
                return render(request, 'exam/questions.html', context)
    else:
        context = {
            'message': "Admin has made you out from Exam."
        }
        messages.add_message(request, messages.WARNING, "Admin has made you out from Exam.")
        return render(request,'accounts/login.html', context)
    

def MCQ(request):
    current_user = request.user
    if current_user.is_staff==False:
        if request.method == 'GET':
            question = Question.objects.get(id=1)
            return render(request,'exam/questions.html',{'question' : question})
        if request.method == 'POST':
            if request.POST['id']:
                id = int(request.POST['id'])
                questions = Question.objects.all()
                flag = 0
                for question in questions:
                    try:
                        answer = request.POST[question.question]
                        solution = [question.question,answer]
                        flag = 1
                        break
                    except Exception:
                        pass
                if flag==1:
                    submit = Solution.objects.filter(number=id, username=current_user.username)
                    if submit:
                        submit.update(questions=solution[0], solution=solution[1])
                    else:
                        user = Solution.objects.create(number=id,username=current_user.username,questions=solution[0],solution=solution[1])
                flag = 0
                try:
                    question = Question.objects.get(id=id+1)
                    flag = 1
                except Exception:
                    pass

                if flag==0:
                    submit = Solution.objects.filter(username=current_user.username)
                    user_info = User.objects.get(username=current_user.username)
                    correct = 0
                    incorrect = 0
                    for i in range(len(submit)):
                        for j in range(len(questions)):
                            if submit[i].number == questions[j].id:
                                if submit[i].solution == questions[j].correct_answer:
                                    correct+=1
                                else:
                                    incorrect+=1
                    context = {
                        'email':user_info.email,
                        'contact_number':user_info.contact_number,
                        'first_name':user_info.first_name,
                        'last_name':user_info.last_name,
                        'correct':correct,
                        'incorrect':incorrect,
                        'unsolve':len(questions)-correct-incorrect
                    }
                    return render(request,'exam/result.html', context)
                return render(request,'questions.html',{'question' : question})
    else:
         return render(request,'login.html',{'message' : "Admin has made you out from Exam."})


def Result(request):
    current_user = request.user
    if current_user.is_staff == False:
        questions = Question.objects.all()
        # submit = Solution.objects.filter(username=current_user.username)
        # user_info = User.objects.get(username=current_user.username)

        submit = Solution.objects.filter(user=current_user)
        user_info = User.objects.get(email=current_user)

        correct = 0
        incorrect = 0
        for i in range(len(submit)):
            for j in range(len(questions)):
                if submit[i].number == questions[j].id:
                    if submit[i].solution == questions[j].correct_answer:
                        correct+=1
                    else:
                        incorrect+=1
        context = {
            
            'email':user_info.email,
            'contact_number':user_info.contact_number,
            'first_name':user_info.first_name,
            'last_name':user_info.last_name,
            'correct':correct,
            'incorrect':incorrect,
            'unsolve':len(questions)-correct-incorrect
        }
        messages.add_message(request, messages.SUCCESS, "Check your result")
        return render(request,'exam/result.html',)
    else:
        messages.add_message(request, messages.WARNING, "Admin has disconnected you from exam!")
        return render(request,'accounts/login.html')


def Submit(request):
    current_user = request.user
    if current_user.is_staff == False:
        questions = Question.objects.all()
        solution =[]
        for item in questions:
            try:
                value = request.POST[item.question]
                solution.append([item.question,value])
            except Exception :
                pass
        submit = Solution.objects.filter(id=current_user.username)
        if submit:
            submit.update(questions=solution)
        else:
            user = Solution.objects.create(id=current_user.username,questions=solution)
        solutions = Solution.objects.get(id=current_user.username)
        user_info = User.objects.get(username=current_user.username)
        solution = solutions.questions
        correct = 0
        incorrect = 0
        for i in range(len(solution)):
            for j in range(len(questions)):
                if solution[i][0] == questions[j].question:
                    if solution[i][1] == questions[j].correct_answer:
                        correct+=1
                    else:
                        incorrect+=1
        
        return render(request,'result.html',{'username':user_info.username,
                    'email':user_info.email,'first_name':user_info.first_name,
                    'last_name':user_info.last_name,'correct':correct,
                    'incorrect':incorrect,'unsolve':len(questions)-correct-incorrect})
    else:
        return render(request,'accounts/login.html',{'message':'Admin has disconnected you from exam!'})
    


             