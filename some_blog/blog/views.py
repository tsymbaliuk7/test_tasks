from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.http import Http404
from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from .forms import PostCreateForm, CommentForm
from .models import Post, Comment


class CreatePostView(LoginRequiredMixin, View):
    template_name = 'blog/post_form.html'

    def get(self, request):
        form = PostCreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = PostCreateForm(request.POST, request.FILES)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        post = form.save(commit=False)
        post.owner = request.user
        post.save()
        return redirect(reverse_lazy('home:home'))


class DetailPostView(View):
    template_name = 'blog/post_detail.html'

    def get(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=post).order_by('-created_at')
        form = CommentForm()
        ctx = {'post': post, 'form': form, 'comments': comments}
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        User = apps.get_model('accounts', 'User')
        user = get_object_or_404(User, pk=request.user.id)
        if not form.is_valid():
            comments = Comment.objects.filter(post=post).order_by('-created_at')
            ctx = {'post': post, 'form': form, comments: 'comments'}
            return render(request, self.template_name, ctx)
        comment = form.save(commit=False)
        comment.post = post
        comment.owner = user
        comment.save()
        return redirect(reverse('blog:detail', args=[pk]))



class UpdatePostView(LoginRequiredMixin, View):
    template_name = 'blog/post_form.html'

    def get(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk, owner=request.user)
        form = PostCreateForm(instance=post)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk, owner=request.user)
        form = PostCreateForm(request.POST, request.FILES, instance=post)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        post = form.save(commit=False)
        post.save()
        return redirect(reverse('blog:detail', args=[pk]))


class DeletePostView(LoginRequiredMixin, View):

    def get(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        if request.user == post.owner or request.user.is_staff:
            ctx = {'post': post}
            return render(request, 'blog/post_delete.html', ctx)
        else:
            raise Http404()

    def post(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        if request.user == post.owner or request.user.is_staff:
            post.delete()
        else:
            raise Http404()
        return redirect(reverse_lazy('home:home'))


@method_decorator(staff_member_required, name='dispatch')
class DeleteAllCommentsView(View):
    def get(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        Comment.objects.filter(post=post).delete()
        return redirect(reverse_lazy('admin:index'))
