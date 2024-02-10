from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CriarContaForm, HomePageForm

# Create your views here.
class Homepage(FormView):
    template_name = "homepage.html"
    form_class = HomePageForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        email = self.request.POST.get('email')
        usuarios = Usuario.objects.filter(email=email)

        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')


class Homefilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    model = Filme


class DetalhesFilme(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"
    model = Filme

    def get(self, request, *args, **kwargs):
        filme = self.get_object()
        filme.visualizacoes += 1
        filme.save()
        usuario = request.user
        usuario.filmes_vistos.add(filme)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetalhesFilme, self).get_context_data(**kwargs)
        context['filmes_relacionados'] = self.model.objects.filter(categoria=self.get_object().categoria)[0:5]
        return context


class PesquisaFilme(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme

    def get_queryset(self):
        termo = self.request.GET.get('q')
        if termo:
            object_list = self.model.objects.filter(titulo__icontains=termo)
            return object_list
        else:
            return None


class PaginaPerfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('filme:homefilmes')


class CriarConta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('filme:login')
