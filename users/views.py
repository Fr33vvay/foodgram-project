from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUpView(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")
    template_name = "reg.html"


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
