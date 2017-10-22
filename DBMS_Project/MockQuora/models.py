from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    topic_id = models.AutoField(unique=True, primary_key=True)
    name = models.CharField(blank=False, max_length=63)

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user_id = models.AutoField(unique=True, primary_key=True)
    user = models.OneToOneField(User)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(blank=False)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    about_me = models.TextField()
    tagline = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    profile_pic = models.URLField(null=True)
    interests = models.ManyToManyField(Topic, verbose_name="list of interests", related_name="interested_users")

    def __unicode__(self):
        return self.user.username


class Message(models.Model):
    message_id = models.AutoField()
    sender = models.ForeignKey(UserProfile, related_name="sent_messages")
    receiver = models.ForeignKey(UserProfile, related_name="received_messages")
    message_text = models.TextField(blank=False)
    is_seen = models.BooleanField(default=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.message_text

    class Meta:
        unique_together = (('message_id', 'sender', 'receiver'),)


class Question(models.Model):
    question_id = models.AutoField(unique=True, primary_key=True)
    posted_by = models.ForeignKey(UserProfile, related_name="user_questions")
    question_text = models.TextField(blank=False)
    is_anonymous = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    viewers = models.ManyToManyField(UserProfile, related_name="viewed_questions")
    topic = models.ForeignKey(Topic, related_name="questions_on_topic")

    def __unicode__(self):
        return self.question_text


class Tag(models.Model):
    question = models.ForeignKey(Question, related_name="tags")
    asked_by = models.ForeignKey(UserProfile, related_name="asked_tags")
    asked_to = models.ForeignKey(UserProfile, related_name="received_tags")
    response = models.SmallIntegerField(default=0, blank=False)

    def __unicode__(self):
        return self.asked_by, " -> ", self.asked_to


class Answer(models.Model):
    answer_id = models.AutoField()
    question = models.ForeignKey(Question, related_name="answers")
    answer_by = models.ForeignKey(UserProfile, related_name="user_answers")
    answer_text = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    viewers = models.ManyToManyField(UserProfile, related_name="viewed_answers")
    bookmarks = models.ManyToManyField(UserProfile, related_name="bookmarks")

    def __unicode__(self):
        return "Answer by ", self.answer_by

    class Meta:
        unique_together = (('answer_id', 'question'),)


class Comment(models.Model):
    comment_id = models.AutoField()
    answer = models.ForeignKey(Answer, related_name="comments")
    question = models.ForeignKey(Question, related_name="comments")
    comment_text = models.TextField(blank=False)
    comment_by = models.ForeignKey(UserProfile, related_name="user_comments")
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', default=-1)

    def __unicode__(self):
        return self.comment_text

    class Meta:
        unique_together = (('comment_id', 'answer', 'question'),)


class Vote(models.Model):
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer)
    comment = models.ForeignKey(Comment, default=-1)
    vote_by = models.ForeignKey(UserProfile, related_name="user_votes")
    vote_type = models.BooleanField(blank=False, default=True)

    def __unicode__(self):
        return "Vote by ", self.vote_by, self.vote_type


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, related_name="user_follows")
    followed_user = models.ForeignKey(UserProfile, related_name="followed_by", default=-1)
    question = models.ForeignKey(Question, default=-1)
    topic = models.ForeignKey(Topic, default=-1)
    timestamp = models.DateTimeField(auto_now_add=True)
    # 0: user, 1: question, 2: topic
    flag = models.SmallIntegerField(blank=False, default=0)
