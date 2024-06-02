from django.http.response import HttpResponse
from django.template import loader, Template, Context

from dbtemplates.models import DBTemplate
from .models import ProfilePage
from post.forms import PostForm
from useraccount.models import UserAccount
from django.contrib.auth.models import User
from django.apps import apps

import datetime


def custom_content(request,profilepage_id):
    template = Template(DBTemplate.objects.get(author=request.user).content)
    profile = ProfilePage.objects.get(object_id=profilepage_id)
    context = Context({'profile': profile})
    return HttpResponse(template.render(context))
    

def profile_detail(request, profilepage_id):
    template = loader.get_template('profilepage.html')
    profile = ProfilePage.objects.get(object_id=profilepage_id)
    posts = []
    own_profile = False
    if profile.content_type.model == 'useraccount':
        Post = apps.get_model('post', 'Post')
        #posts = Post.objects.filter(author=profile.subject.user)
        posts = Post.objects.all().filter(author=profile.subject.user)
        #posts = list(Post.objects.all()).filter(lambda p: p.author == profile.user_account.user)
        own_profile = request.user and (request.user.id == profile.subject.user.id)
    return HttpResponse(template.render({'profile': profile, 'posts': posts, 'own_profile': own_profile, 'new_post_form': PostForm(), 'seconds_since': get_seconds_since(profile.subject.created_on.date())}, request))


def get_seconds_since(date):
    return (datetime.date.today() - date).total_seconds()
