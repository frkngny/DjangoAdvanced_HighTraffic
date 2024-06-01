from django.http.response import HttpResponse
from django.template import loader

from .models import ProfilePage
from useraccount.models import UserAccount
from django.contrib.auth.models import User
from django.apps import apps

import datetime


def profile_detail(request, profilepage_id):
    template = loader.get_template('profilepage.html')
    profile = ProfilePage.objects.get(object_id=profilepage_id)
    print(profile.subject)
    posts = []
    own_profile = False
    if profile.content_type.model == 'useraccount':
        Post = apps.get_model('post', 'Post')
        #posts = Post.objects.filter(author=profile.subject.user)
        posts = Post.objects.all().filter(author=profile.user_account.user)
        posts = list(Post.objects.all()).filter(lambda p: p.author == profile.user_account.user)
        own_profile = request.user and (request.user.id == profile.subject.user.id)
    return HttpResponse(template.render({'profile': profile, 'posts': posts, 'own_profile': own_profile}, request))


