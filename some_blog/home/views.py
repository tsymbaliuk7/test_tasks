from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.apps import apps
from django.contrib.auth.forms import PasswordResetForm



class MainView(View):
    def get(self, request):
        Posts = apps.get_model('blog', 'Post')
        posts = Posts.objects.all().order_by('-created_at')
        ctx = {'posts': posts}
        return render(request, 'home/main.html', ctx)


class PasswordResetRequestView(View):
    def get(self, request):
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="home/password/password_reset.html",
                      context={"password_reset_form": password_reset_form})

    def post(self, request):
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            User = apps.get_model('accounts', 'User')
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "home/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Some_Blog',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
