# from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from users.forms import CreationForm
# from users.forms import ContactForm
from django.shortcuts import redirect
# from users.models import Contact


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


def authorized_only(func):
    # Функция-обёртка в декораторе может быть названа как угодно
    def check_user(request, *args, **kwargs):
        # В любую view-функции первым аргументом передаётся объект request,
        # в котором есть булева переменная is_authenticated,
        # определяющая, авторизован ли пользователь.
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return redirect('/auth/login/')
    return check_user


@authorized_only
def some_view(request):
    return 'Доступно только авторизованным!'
