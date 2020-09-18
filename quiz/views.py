import re

from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from .models import Question, Answer, User, Subject
from .forms import RegisterForm

def filterCharacter(character):
    if character == '':
        return False
    if character == ' ':
        return False
    else:
        return True

class QuestionsListView(generic.ListView):
    template_name = 'quiz/questionslist.html'
    model = Question
    context_object_name = 'latest_question_list'

    # @login_required(login_url="/quiz/login")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        :return:
        """
        subject= get_object_or_404(Subject, pk=self.kwargs['pk'])

        questions=subject.question_set.all()
        #question_list=[int(s) for s in filter(filterCharacter,self.request.user.profile.questions_attempted.split(','))]

       # enable this later
       #
       #
       #  for id in question_list:
       #      questions=questions.exclude(pk=id)
       #

        return questions.order_by('timeout')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject']= get_object_or_404(Subject, pk=self.kwargs['pk'])
        return context

class IndexView(generic.ListView):
    template_name = 'quiz/index.html'

    context_object_name = 'subjects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['user']= 'Hi '+self.request.user.username
            context['register']='Sign Out'
        else:
            context['user']= 'Signin'
            context['register']='Register'
        return context

    def get_queryset(self):
         return  Subject.objects.all()




class QuestionView(generic.DetailView):
    model = Question
    template_name = 'quiz/question.html'

    # @login_required(login_url="/quiz/login")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        question = get_object_or_404(Question, pk=self.object.pk)
        question_info = question.answer_set.all()
        option_set = []
        for options in question_info:
            option_set.append(options.option1)
            option_set.append(options.option2)
            option_set.append(options.option3)
            option_set.append(options.option4)
        context['option_set'] = option_set
        context['points_allocated'] = question.points
        return context
        # points_allocated = question.points

    # return render(request, '',
    #               {'question': question, 'option_set': option_set,
    #                'points_allocated': points_allocated})


class ResultsView(generic.DetailView):
    model = User
    template_name = 'quiz/results.html'
    message = ''
    subject_id=''

    def get(self, request, *args, **kwargs):
        if len(self.request.GET) > 0:
            self.message = self.request.GET['message']
            self.subject_id = self.request.GET['subjectid']
        return super().get(request, *args, **kwargs)

    # @login_required(login_url="/quiz/login")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = self.message
        context['subject_id'] = self.subject_id
        return context


# class ResultMsgView(generic.DetailView):
#     model=User
#     template_name = 'quiz/results.html'
#
#     def get(self, request, *args, **kwargs):
#         return super().get(request,*args, **kwargs)


# # question_info=get_object_or_404(Answer,pk=question_id)
# return render(request, 'quiz/results.html',
#               {'user': get_object_or_404(User, pk=11), 'message': message})


# def ResultMsgView(request, message):
#     result = '4'
#     question_info = ''
#     # question_info=get_object_or_404(Answer,pk=question_id)
#     return render(request, 'quiz/results.html',
#                   {'user': get_object_or_404(User, pk=11), 'message': message})

@login_required(login_url="/login")
def selection(request, question_id):
    """
    Verification of selected answer.
    Improvements: Points stored in session instead of DB
    :param request:
    :param question_id:
    :return:
    """
    regex_query = re.compile("([a-zA-Z ]+)([0-9]+)")
    question = get_object_or_404(Question, pk=question_id)

    if request.user.is_authenticated:
        user = request.user


    question_info = question.answer_set.all()
    option_set = []
    for options in question_info:
        option_set.append(options.option1)
        option_set.append(options.option2)
        option_set.append(options.option3)
        option_set.append(options.option4)

    try:
        correct_option = question_info[0].correct_option
        correct_option = int(regex_query.match(correct_option).groups()[1])
        if len(request.POST)>1:
            selected = request.POST['selection']
        else:
            selected= ' '
    except (KeyError, Answer.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'quiz/404.html', {
            'question': question,
            'error_message': "Answer is not saved correct by Admin. "
                             "Contact technical support.",
        })
    except:
        return render(request, 'quiz/404.html',
                      {'question': question,
                       'error_message': "Answer is "
                                        "not saved "
                                        "correct "
                                        "by Admin. "
                                        "Contact "
                                        "technical "
                                        "support.",
                       })
    else:

        if selected == " ":
            message = "Correct Answer is " \
                      + str(option_set[correct_option - 1])
        elif selected == str(correct_option):
            user.profile.points_scored += int(question.points)
            message = "Correct Answer."

        else:

            message = "Incorrect. Correct Answer is " \
                      + str(option_set[correct_option - 1])
        user.profile.questions_attempted += str(question_id) + ', '
        user.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse('quiz:results',
                    kwargs={'pk': user.pk}) + '?message=' + message+'&'+'subjectid='+str(question.subject_id))


def logout_view(request):
    logout(request)

def register(request):
    user=None
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
        else:
            return render(request, "quiz/register.html", {"form": form})
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        # user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/quiz")
    else:
        form = RegisterForm()

        return render(request, "quiz/register.html", {"form": form})


def about(request):
    return render(request,'quiz/about.html');


# def login_view(request):
#     if request.method=='POST':
#         form =AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user =form.get_user()
#             login(request,user)
#             # if 'next' not in request.POST:
#                 # return  redirect(request.POST.get('next'))
#             return redirect('quiz')
#     else:
#         form = AuthenticationForm()
#     return render('quiz/login',{'form':form})







