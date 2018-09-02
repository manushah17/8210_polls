
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import QuestionModelForm, ChoiceFormset, UserLoginForm
from .models import Question, Choice
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout


def index(request):
    polls = Question.objects.order_by('-pub_date')
    paginator = Paginator(polls, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        latest_question_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        latest_question_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        latest_question_list = paginator.page(paginator.num_pages)
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', {'page': page, 'latest_question_list': latest_question_list})
    #return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



def create_quest_with_choice(request):
    template_name = 'polls/create_quest_with_choice.html'
    if request.method == 'GET':
        questionform = QuestionModelForm(request.GET or None)
        formset = ChoiceFormset(queryset=Choice.objects.none())
    elif request.method == 'POST':
        questionform = QuestionModelForm(request.POST)
        formset = ChoiceFormset(request.POST)
        if questionform.is_valid() and formset.is_valid():
            # first save this book, as its reference will be used in `Author`
            question = questionform.save(commit=False)
            question.author = request.user
            question.save()
            for form in formset:
                # so that `book` instance can be attached.
               # print("choice text ", form.choice_text)
                choice = form.save(commit=False)
                choice.question = question
                choice.save()
            return redirect('polls:index')
    return render(request, template_name, {
        'questionform': questionform,
        'formset': formset,
    })


def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('polls:index')
    return render(request, 'registration/login_form.html', {'form': form, 'title': title})



def logout_view(request):
    logout(request)
    return redirect('polls:index')
