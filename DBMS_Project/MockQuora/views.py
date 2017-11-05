from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import *
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum

BASE_URL = "http://127.0.0.1:8000"


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
                    return HttpResponseRedirect('/MockQuora/feed/')
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
            user.set_password(user.password)
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return HttpResponseRedirect('/MockQuora/add_details/')
        else:
            error_msg = form.errors

    form = RegisterUserForm()
    context = {
        'message': error_msg,
        'form': form
    }

    return render(request, 'MockQuora/register.html', context)


@login_required
def askto(request, question_id):
    try:
        user = UserProfile.objects.get(user=request.user)
        question = Question.objects.get(pk=question_id)
        username = request.GET.get('username', None)
        if username is not None:
            second_user = UserProfile.objects.get(user__username=username)
            tag = Tag(question=question, asked_by=user, asked_to=second_user)
            tag.save()
            notification = Notification(user=second_user,
                                        notification_text=str(user.user.username) + " asked you to answer " + str(
                                            question.question_text), url=BASE_URL + '/MockQuora/question/' + str(question_id))
            notification.save()
        return HttpResponseRedirect('/MockQuora/question' + str(question_id))
    except Exception as e:
        print "[Exception]: ", e
        raise Http404


@login_required
def add_profile_details(request):
    error_msg = ""
    if request.method == "POST":
        form = RegisterProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            user_profile.interests.add(*form.cleaned_data["interests"])
            user_profile.save()
            return HttpResponseRedirect('/MockQuora/feed/')
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
    query = request.GET.get('search_query', None)
    user = UserProfile.objects.get(user=request.user)
    notification = Notification.objects.filter(user=user).order_by('-timestamp')

    if query is not None:
        questions = Question.objects.filter(Q(question_text__contains=query)).order_by('-timestamp')
        popular_users = UserProfile.objects.filter(
            Q(user__username__contains=query) | Q(user__first_name__contains=query) | Q(
                user__last_name__contains=query))
        trending_topics = Topic.objects.filter(name__contains=query)

    else:
        followings = Follow.objects.filter(follower=user, flag=2)
        followed_topics_ids = [x.followed_id for x in followings]
        followed_topics = Topic.objects.filter(topic_id__in=followed_topics_ids)
        questions = Question.objects.filter(Q(topic__in=user.interests.all())
                                            | Q(topic__in=followed_topics)).order_by('-timestamp')
        # questions = questions.filter(~Q(posted_by=user))

        popular_answers = Answer.objects.annotate(viewer_count=Count('viewers')).order_by('-viewer_count')
        # popular_answers = popular_answers.filter(~Q(answer_by=user))
        popular_users = [ans.answer_by for ans in popular_answers]

        popular_questions = Question.objects.annotate(viewer_count=Count('viewers')).order_by('-viewer_count')
        trending_topics = []

        for ques in popular_questions:
            trending_topics.extend(ques.topic.all())

    answered_questions = []
    unanswered_questions = []
    for question in questions:
        if Follow.objects.filter(follower=user, followed_id=question.pk, flag=1).count() == 1:
            following_status = True
        else:
            following_status = False
        if question.answers.count() == 0:
            unanswered_questions.append((question, following_status))
        else:
            most_popular_answer = question.answers.annotate(viewer_count=Count('viewers')).order_by('-viewer_count')[:1]
            answered_questions.append((question, most_popular_answer[0], following_status))

    final_popular_users = []
    # for usr in set(popular_users):
    for usr in popular_users:
        if Follow.objects.filter(follower=user, followed_id=usr.pk, flag=0).count() == 1:
            final_popular_users.append((usr, True))
        else:
            final_popular_users.append((usr, False))

    final_trending_topics = []
    for topic in set(trending_topics):
        if Follow.objects.filter(follower=user, followed_id=topic.pk, flag=2).count() == 1:
            final_trending_topics.append((topic, True))
        else:
            final_trending_topics.append((topic, False))

    context = {
        'answered_questions': answered_questions,
        'unanswered_questions': unanswered_questions,
        'popular_users': final_popular_users,
        'trending_topics': final_trending_topics,
        'user': user,
        'notifications': notification
    }

    return render(request, 'MockQuora/feed.html', context)


@login_required
def follow(request, follow_id, followed_id):
    try:
        user = UserProfile.objects.get(user=request.user)
        follows, created = Follow.objects.get_or_create(follower=user, followed_id=followed_id, flag=follow_id)
        if created:
            follows.save()
            if int(follow_id) == 0:
                second_user = UserProfile.objects.get(pk=followed_id)
                notification = Notification(user=second_user,
                                            notification_text=str(user.user.username) + " started following you.",
                                            url=BASE_URL + '/MockQuora/profile/' + str(user.pk))
                notification.save()
        else:
            follows.delete()
        return HttpResponseRedirect('/MockQuora/feed')
    except Exception as e:
        print "[Exception]: ", e
        raise Http404


@login_required
def follow_profile(request, followed_id):
    try:
        user = UserProfile.objects.get(user=request.user)
        follows, created = Follow.objects.get_or_create(follower=user, followed_id=followed_id, flag=0)
        if created:
            follows.save()
            second_user = UserProfile.objects.get(pk=followed_id)
            notification = Notification(user=second_user,
                                        notification_text=str(user.user.username) + " started following you.",
                                        url=BASE_URL + '/MockQuora/profile/' + str(user.pk))
            notification.save()
        else:
            follows.delete()

        return HttpResponseRedirect('/MockQuora/profile/' + str(followed_id))

    except Exception as e:
        print "[Exception]: ", e
        raise Http404


@login_required
def bookmark(request, answer_id):
    try:
        user = UserProfile.objects.get(user=request.user)
        answer = Answer.objects.get(pk=answer_id)
        question = answer.question

        if user in answer.bookmarks.all():
            answer.bookmarks.remove(user)
        else:
            answer.bookmarks.add(user)
        return HttpResponseRedirect('/MockQuora/answer/' + str(question.pk) + '/' + str(answer_id))

    except Exception as e:
        print "[Exception]: ", e
        raise Http404


@login_required
def votes(request, vote_id, answer_id, comment_id, flag):
    try:
        user = UserProfile.objects.get(user=request.user)
        answer = Answer.objects.get(pk=answer_id)
        question = answer.question
        if int(comment_id) == 0:
            vote, created = Vote.objects.get_or_create(vote_by=user, vote_type=vote_id, answer=answer,
                                                       question=question)
        else:
            comment = Comment.objects.get(pk=comment_id)
            vote, created = Vote.objects.get_or_create(vote_by=user, vote_type=vote_id, answer=answer,
                                                       question=question, comment=comment)

        if created:
            vote.save()
            second_user = answer.answer_by
            notification = Notification(user=second_user,
                                        notification_text=str(user.user.username) + " left a vote on your answer.",
                                        url=BASE_URL + '/MockQuora/answer/' + str(question.pk) + '/' + str(answer_id))
            notification.save()
        else:
            vote.delete()
        if int(flag) == 1:
            return HttpResponseRedirect('/MockQuora/question/' + str(question.pk))
        else:
            return HttpResponseRedirect('/MockQuora/answer/' + str(question.pk) + '/' + str(answer_id))

    except Exception as e:
        print "[Exception]: ", e
        raise Http404


@login_required
def post_question(request):
    try:
        message = ""
        user = UserProfile.objects.get(user=request.user)
        notification = Notification.objects.filter(user=user).order_by('-timestamp')
        form = QuestionForm()

        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.posted_by = user
                question.save()
                print question.pk
                return HttpResponseRedirect('/MockQuora/question/' + str(question.question_id))
            else:
                message = form.errors

        context = {
            'form': form,
            'message': message,
            'user': user,
            'notifications': notification
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
        notification = Notification.objects.filter(user=user).order_by('-timestamp')
        form = AnswerForm()

        if user not in question.viewers.all():
            question.viewers.add(user)

        if request.method == 'POST':
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer_text = form.cleaned_data['answer_text']
                image = request.FILES['image']
                answer = Answer(question=question, answer_text=answer_text, answer_by=user, image=image)
                answer.save()
                second_user = question.posted_by
                notification = Notification(user=second_user,
                                            notification_text=str(user.user.username) + " answered your question.",
                                            url=BASE_URL + '/MockQuora/question/' + str(question.pk) )
                notification.save()
                message = "success"
            else:
                message = form.errors

        context = {
            'question': question,
            'answers': answers,
            'form': form,
            'message': message,
            'user': user,
            'notifications': notification
        }
        return render(request, 'MockQuora/question_details.html', context)

    except Exception as e:
        print "[Exception]: Some error in question_page view", e
        raise Http404


@login_required
def answer_page(request, question_id, answer_id):
    try:
        message = ""
        question = Question.objects.get(question_id=question_id)
        answer = Answer.objects.get(answer_id=answer_id)
        user = UserProfile.objects.get(user=request.user)
        notification = Notification.objects.filter(user=user).order_by('-timestamp')
        comments = answer.comments.all()
        form = CommentForm()

        if user not in answer.viewers.all():
            answer.viewers.add(user)

        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment_text = form.cleaned_data['comment_text']
                comment = Comment(question=question, answer=answer, comment_text=comment_text, comment_by=user)
                comment.save()
                second_user = answer.answer_by
                notification = Notification(user=second_user,
                                            notification_text=str(user.user.username) + " commented on your answer.",
                                            url=BASE_URL + '/MockQuora/answer/' + str(question.pk) + '/' + str(answer_id))
                notification.save()
                message = "success"
            else:
                message = form.errors

        context = {
            'question': question,
            'answer': answer,
            'comments': comments,
            'form': form,
            'message': message,
            'user': user,
            'notifications': notification
        }
        return render(request, 'MockQuora/answer.html', context)

    except Exception as e:
        print "[Exception]: ", e
        raise Http404


@login_required
def profile(request, user_id):
    try:
        user = UserProfile.objects.get(pk=user_id)
        profile_user = UserProfile.objects.get(user=request.user)
        bookmarks = user.bookmarks.all()
        follower = Follow.objects.filter(Q(flag=0, followed_id=user.pk))
        followers = [(i.follower, i.timestamp) for i in follower]
        following = Follow.objects.filter(flag=0, follower=user)
        followings = [(UserProfile.objects.get(pk=i.followed_id), i.timestamp) for i in following]
        question_count = Question.objects.filter(posted_by=user, is_anonymous=False).count()
        answers = Answer.objects.filter(answer_by=user)
        answer_count = answers.count()
        notification = Notification.objects.filter(user=profile_user).order_by('-timestamp')
        upvotes_count = 0
        for answer in answers:
            upvotes_count += Vote.objects.filter(answer=answer, comment=-1).count()

        if Follow.objects.filter(follower=user, followed_id=user_id, flag=0).count() == 1:
            follow_flag = True
        else:
            follow_flag = False

        context = {
            'user': user,
            'profile_user': profile_user,
            'follow_flag': follow_flag,
            'bookmarks': bookmarks,
            'follower': followers,
            'following': followings,
            'question_count': question_count,
            'answer_count': answer_count,
            'upvotes_count': upvotes_count,
            'notifications': notification
        }

        return render(request, "MockQuora/profile.html", context)

    except Exception as e:
        print "[Exception]: ", e
        raise Http404


@login_required
def chat(request):
    try:
        user = UserProfile.objects.get(user=request.user)
        recent_message = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-timestamp')[:1]

        if len(recent_message) == 0:
            second_id = 0
        else:
            if recent_message[0].sender == user:
                second_id = recent_message[0].receiver.pk
            else:
                second_id = recent_message[0].sender.pk
        return HttpResponseRedirect('/MockQuora/message/' + str(second_id))

    except Exception as e:
        print "[Exception]: ", e
        raise Http404


@login_required
def message(request, user_id):
    try:
        message = ""
        if int(user_id) == 0:
            message = "No chat history found!"
            context = {
                'message': message
            }
        else:
            user = UserProfile.objects.get(user=request.user)
            second_user = UserProfile.objects.get(pk=user_id)
            if request.method == 'POST':
                message_text = request.POST.get('message_text', None)
                if message_text is not None:
                    msg = Message(sender=user, receiver=second_user, message_text=message_text)
                    msg.save()

                    notification = Notification(user=second_user,
                                                notification_text=str(user.user.username) + " messaged you.",
                                                url=BASE_URL + '/MockQuora/message/' + str(user.pk))
                    notification.save()
                    print "message added"

            messages = Message.objects.filter(
                Q(sender=user, receiver=second_user) | Q(sender=second_user, receiver=user)).order_by('timestamp')
            all_messages = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-timestamp')
            connections = set()
            for msg in all_messages:
                if msg.sender == user:
                    connections.add(msg.receiver)
                else:
                    connections.add(msg.sender)

            connections = [i for i in connections]

            context = {
                'user': user,
                'chat_user': second_user,
                'messages': messages,
                'connections': connections,
                'message': message
            }
            m = context['messages']
            for i in m:
                print i.is_seen

            not_seen_messages = Message.objects.filter(receiver=user, sender=second_user, is_seen=False)
            for msg in not_seen_messages:
                msg.is_seen = True
                msg.save()
            m = context['messages']
            for i in m:
                print i.is_seen
        return render(request, "MockQuora/chat.html", context)
    except Exception as e:
        print "[Exception]: ", e
        raise Http404


@login_required
def notifications(request):
    try:
        user = UserProfile.objects.get(user=request.user)
        notification = Notification.objects.filter(user=user).order_by('-timestamp')

        context = {
            'user': user,
            'notifications': notification
        }
        print context
        return render(request, 'MockQuora/notification.html', context)
    except Exception as e:
        print "[Exception]: ", e
        raise Http404


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/MockQuora/')
