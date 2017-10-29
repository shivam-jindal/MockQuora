from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import *
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum


def index(request):
    return render(request, 'MockQuora/index.html', {})


def user_login(request):
    error_msg = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('feed/')
                else:
                    error_msg = "Your account is disabled!"
            else:
                error_msg = "Invalid Login Details."
                print error_msg
        else:
            error_msg = form.errors

    form = LoginForm()
    context = {
        'message': error_msg,
        'form': form
    }
    return render(request, 'MockQuora/login.html', context)


def register_user(request):
    error_msg = ""
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return HttpResponseRedirect('/add_details/')
        else:
            error_msg = form.errors

    form = RegisterUserForm()
    context = {
        'message': error_msg,
        'form': form
    }

    return render(request, 'MockQuora/register.html', context)


@login_required
def add_profile_details(request):
    error_msg = ""
    if request.method == "POST":
        form = RegisterProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.add(*form.cleaned_data["interests"])
            user_profile.user = request.user
            user_profile.save()
            return HttpResponseRedirect('/feed/')
        else:
            error_msg = form.errors

    form = RegisterProfileForm()
    context = {
        'message': error_msg,
        'form': form
    }

    return render(request, 'MockQuora/register_profile.html', context)


@login_required
def feed(request):
    if request.method == "POST":
        pass

    user = UserProfile.objects.get(user=request.user)
    followings = Follow.objects.filter(follower=user, flag=2)
    followed_topics_ids = [x.followed_id for x in followings]
    followed_topics = Topic.objects.filter(topic_id__in=followed_topics_ids)
    questions = Question.objects.filter(Q(topic__in=user.interests.all())
                                        | Q(topic__in=followed_topics)).order_by('timestamp')
    questions = questions.filter(~Q(posted_by=user))

    answered_questions = []
    unanswered_questions = []
    for question in questions:
        if question.answers.count() == 0:
            unanswered_questions.append(question)
        else:
            most_popular_answer = question.answers.annotate(viewer_count=Count('viewers')).order_by('-viewer_count')[:1]
            answered_questions.append((question, most_popular_answer))

    popular_answers = Answer.objects.annotate(viewer_count=Count('viewers')).order_by('-viewer_count')
    popular_users = [ans.answer_by for ans in popular_answers]

    popular_questions = Question.objects.annotate(viewer_count=Count('viewers')).order_by('-viewer_count')
    trending_topics = [ques.topic for ques in popular_questions]

    context = {
        'answered_questions': answered_questions,
        'unanswered_questions': unanswered_questions,
        'popular_users': popular_users,
        'trending_topics': trending_topics
    }

    return render(request, 'MockQuora/feed.html', context)


@login_required
def post_question(request):
    try:
        message = ""
        user = UserProfile.objects.get(user=request.user)
        form = QuestionForm()

        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.posted_by = user
                question.save()
                message = "success"
            else:
                message = form.errors

        context = {
            'form': form,
            'message': message,
        }

        return render(request, 'MockQuora/post_question.html', context)

    except Exception as e:
        print "[Exception]: ", e
        raise Http404


@login_required
def question_page(request, question_id):
    try:
        message = ""
        question = Question.objects.get(question_id=question_id)
        answers = question.answers.order_by('-timestamp')
        user = UserProfile.objects.get(user=request.user)
        form = AnswerForm()

        if request.method == 'POST':
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer_text = form.cleaned_data['answer_text']
                answer = Answer(question=question, answer_text=answer_text, answer_by=user)
                answer.save()
                message = "success"
            else:
                message = form.errors

        context = {
            'question': question,
            'answers': answers,
            'form': form,
            'message': message
        }
        return render(request, 'MockQuora/question_details.html', context)

    except Exception as e:
        print "[Exception]: ", e
        raise Http404


@login_required
def answer_page(request, question_id, answer_id):
    try:
        message = ""
        question = Question.objects.get(question_id=question_id)
        answer = Answer.objects.get(answer_id=answer_id)
        user = UserProfile.objects.get(user=request.user)
        comments = answer.comments.all()
        form = CommentForm()

        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                pass
                message = "success"
            else:
                message = form.errors

        context = {
            'question': question,
            'answer': answer,
            'comments': comments,
            'form': form,
            'message': message
        }
        return render(request, 'MockQuora/answer_details.html', context)

    except Exception as e:
        print "[Exception]: ", e
        raise Http404


@login_required
def profile(request, user_id):
    try:
        user = UserProfile(pk=user_id)
        bookmarks = user.bookmarks.all()
        follower_count = Follow.objects.filter(Q(flag=0, followed_id=user.pk)).count()
        question_count = Question.objects.filter(posted_by=user, is_anonymous=False).count()
        answers = Answer.objects.filter(answer_by=user)
        answer_count = answers.count()
        upvotes_count = 0
        for answer in answers:
            upvotes_count += Vote.objects.filter(answer=answer, comment=-1).count()

        context = {
            'user': user,
            'bookmarks': bookmarks,
            'follower_count': follower_count,
            'question_count': question_count,
            'answer_count': answer_count,
            'upvotes_count': upvotes_count
        }

        return render(request, "MockQuora/profile.html", context)

    except Exception as e:
        print "[Exception]: ", e
        raise Http404

