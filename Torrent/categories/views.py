from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Category
from games.models import Game
# Create your views here.
class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        obj=self.get_object()
        games=Game.objects.filter(category__pk=obj.pk).order_by('-release_date')
        p = Paginator(games, 8)
        page = self.request.GET.get('page')
        games_list = p.get_page(page)
        #num_pages = games_list.paginator.num_pages
        #num_pages = list(range(1, num_pages + 1))
        context['games']=games
        context['games_list'] = games_list
        #context['num_pages'] = num_pages
        return context
class CategoryCreateView(LoginRequiredMixin,UserPassesTestMixin,generic.CreateView):
    model = Category
    fields = [
        'name',
    ]
    template_name = 'category_create.html'
    def  test_func(self):
        return self.request.user.is_superuser
class CategoryUpdateView(LoginRequiredMixin,UserPassesTestMixin,generic.UpdateView):
    model = Category
    fields = [
        'name',
    ]
    template_name = 'category_update.html'
    def  test_func(self):
        return self.request.user.is_superuser
class CategoryDeleteView(LoginRequiredMixin,UserPassesTestMixin,generic.DeleteView):
    model = Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy('home')
    def  test_func(self):
        return self.request.user.is_superuser