from django.shortcuts import render
from django.views import View
from django.apps import apps

class MainView(View):
    def get(self, request):
        Posts = apps.get_model('blog', 'Post')
        posts = Posts.objects.all()
        ctx = {'posts': posts}
        return render(request, 'home/main.html', ctx)
