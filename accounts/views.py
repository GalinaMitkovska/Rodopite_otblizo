from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from .forms import AppUserRegistrationForm


class RegisterView(CreateView):
    form_class = AppUserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def form_invalid(self, form):
        # ТОВА ЩЕ ИЗПИШЕ ТОЧНАТА ГРЕШКА В ТВОЯ ТЕРМИНАЛ!
        print("--- ГРЕШКА ВЪВ ФОРМАТА ЗА РЕГИСТРАЦИЯ ---")
        print(form.errors)
        return super().form_invalid(form)