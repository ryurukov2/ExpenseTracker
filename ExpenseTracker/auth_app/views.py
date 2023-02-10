from django.contrib.auth import views as auth_views, login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.generic import UpdateView, DetailView

from ExpenseTracker.auth_app.forms import SignUpForm


class SignUpView(views.CreateView):
    template_name = 'auth_app/sign-up.html'
    form_class = SignUpForm

    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class SignInView(auth_views.LoginView):
    template_name = 'auth_app/login.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.request.POST.get('next'):
            return self.request.POST.get('next')
        elif self.success_url:
            return self.success_url

        return self.get_redirect_url() or self.get_default_redirect_url()


class SignOutView(auth_views.LogoutView):
    template_name = 'auth_app/sign-out.html'