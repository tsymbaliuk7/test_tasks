from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import authenticate, login

from .forms import UserCreationForm


class RegisterView(View):
    template = 'accounts/register.html'

    def get(self, request):
        form = UserCreationForm()
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)
        user = form.save(commit=True)
        login(request, user=user)
        return redirect(reverse_lazy('home:home'))
