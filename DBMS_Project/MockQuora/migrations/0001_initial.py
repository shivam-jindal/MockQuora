# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('answer_id', models.AutoField(serialize=False, primary_key=True)),
                ('answer_text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to=b'MockQuora/static/MockQuora/images')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(serialize=False, primary_key=True)),
                ('comment_text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('answer', models.ForeignKey(related_name='comments', to='MockQuora.Answer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('followed_id', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('flag', models.SmallIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_id', models.AutoField(serialize=False, primary_key=True)),
                ('message_text', models.TextField()),
                ('is_seen', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notification_id', models.AutoField(serialize=False, primary_key=True)),
                ('notification_text', models.TextField()),
                ('url', models.URLField()),
                ('is_read', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.AutoField(unique=True, serialize=False, primary_key=True)),
                ('question_text', models.TextField()),
                ('is_anonymous', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('response', models.SmallIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('topic_id', models.AutoField(unique=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=63)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('date_of_birth', models.DateField()),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('about_me', models.TextField()),
                ('tagline', models.CharField(max_length=255)),
                ('university', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=255)),
                ('profile_pic', models.URLField()),
                ('interests', models.ManyToManyField(related_name='interested_users', verbose_name=b'list of interests', to='MockQuora.Topic')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote_type', models.BooleanField(default=True)),
                ('answer', models.ForeignKey(to='MockQuora.Answer')),
                ('comment', models.ForeignKey(default=-1, to='MockQuora.Comment')),
                ('question', models.ForeignKey(to='MockQuora.Question')),
                ('vote_by', models.ForeignKey(related_name='user_votes', to='MockQuora.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('question', 'answer', 'comment')]),
        ),
        migrations.AddField(
            model_name='tag',
            name='asked_by',
            field=models.ForeignKey(related_name='asked_tags', to='MockQuora.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tag',
            name='asked_to',
            field=models.ForeignKey(related_name='received_tags', to='MockQuora.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tag',
            name='question',
            field=models.ForeignKey(related_name='tags', to='MockQuora.Question'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('question', 'asked_to', 'asked_by')]),
        ),
        migrations.AddField(
            model_name='question',
            name='posted_by',
            field=models.ForeignKey(related_name='user_questions', to='MockQuora.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='topics',
            field=models.ManyToManyField(related_name='questions_on_topic', null=True, to='MockQuora.Topic', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='viewers',
            field=models.ManyToManyField(related_name='viewed_questions', to='MockQuora.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(related_name='notifications', to='MockQuora.UserProfile'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='notification',
            unique_together=set([('notification_id', 'user')]),
        ),
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(related_name='received_messages', to='MockQuora.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(related_name='sent_messages', to='MockQuora.UserProfile'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='message',
            unique_together=set([('message_id', 'sender', 'receiver')]),
        ),
        migrations.AddField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(related_name='user_follows', to='MockQuora.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_by',
            field=models.ForeignKey(related_name='user_comments', to='MockQuora.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(default=-1, to='MockQuora.Comment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='question',
            field=models.ForeignKey(related_name='comments', to='MockQuora.Question'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set([('comment_id', 'answer', 'question')]),
        ),
        migrations.AddField(
            model_name='answer',
            name='answer_by',
            field=models.ForeignKey(related_name='user_answers', to='MockQuora.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='bookmarks',
            field=models.ManyToManyField(related_name='bookmarks', to='MockQuora.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answers', to='MockQuora.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='viewers',
            field=models.ManyToManyField(related_name='viewed_answers', to='MockQuora.UserProfile'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([('answer_id', 'question')]),
        ),
    ]
