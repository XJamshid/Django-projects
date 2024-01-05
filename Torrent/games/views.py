from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth import mixins
from categories.models import Category
from .models import Game,Screenshots
from comments.models import Comments
from comments.forms import CommentAddForm
from .forms import GameCreateForm
# Create your views here.
#Class-based views
class GameDetailView(generic.DetailView):
    template_name = 'game_detail.html'
    model = Game
   #context_object_name = 'game'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        game=self.get_object()
        form=CommentAddForm# form nomli byekt yaratdik
        comments=Comments.objects.filter(game__name=game.name).order_by('-date')
        screenshots=Game.objects.filter(name=game.name).values_list('screenshots__screenshots',flat=True)
        categories=Game.objects.filter(name=game.name).values_list('category__name',flat=True)
        categories=list(categories)
        screenshots=list(screenshots)
        likes = game.likes.count()
        liked = False
        if game.likes.filter(pk=self.request.user.pk).exists():
            liked=True
        p = Paginator(comments, 10)
        page = self.request.GET.get('page')
        comments_list = p.get_page(page)
        context['comments_list'] = comments_list
        context['liked']=liked
        context['likes']=likes
        context['game'] = game
        context['categories']=categories
        context['screenshots']=screenshots
        context['comments']=comments
        context['form']=form#Templatega yubordik
        return context
class GameCreateView(mixins.LoginRequiredMixin,mixins.UserPassesTestMixin,generic.CreateView):
    template_name = 'game_create.html'
    form_class = GameCreateForm
    success_url = reverse_lazy('home')
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            screenshots = request.FILES.getlist('screenshots')
            categories=request.POST.getlist('category')
            game_name=request.POST.get('name')
            form=GameCreateForm(request.POST,request.FILES)
            if form.is_valid():
                game=form.save(commit=False)
                game.save()
                for screenshot1 in screenshots:
                    screenshot2=Screenshots(
                        game_name=game_name,
                        screenshots=screenshot1
                    )
                    screenshot2.save()
                    game.screenshots.add(screenshot2)
                for category_pk in categories:
                    category=Category.objects.get(pk=category_pk)
                    game.category.add(category)
                return HttpResponseRedirect(reverse("game", args=[str(game.pk)]))
            else:
                return HttpResponse(form.errors)
    def  test_func(self):
        return self.request.user.is_superuser
class GameDeleteView(mixins.LoginRequiredMixin,mixins.UserPassesTestMixin,generic.DeleteView):
    model = Game
    template_name = 'game_delete.html'
    success_url = reverse_lazy('home')
    def  test_func(self):
        return self.request.user.is_superuser
class GameUpdateView(mixins.LoginRequiredMixin,mixins.UserPassesTestMixin,generic.UpdateView):
    model = Game
    template_name = 'game_update.html'
    success_url = reverse_lazy('home')
    fields = [
        'name',
        'release_date',
        'category',
        'poster',
        'trailer',
        'screenshots',
        'file',
    ]
    def  test_func(self):
        return self.request.user.is_superuser

#Function-based views
def LikeView(request,pk):
    #Like lar uchun view
    game=get_object_or_404(Game,pk=pk)#game ni olamiz
    user=request.user#like bosayotgan foydalanuvchi
    if user.is_authenticated:#ro'yxatdan o'tgan b'lishi kerak
        if game.likes.filter(pk=user.pk).exists():#agar game ning likelarining ichida user bo'lsa true qaytaradi
            game.likes.remove(user)#like n io'chiradi
        else:
            game.likes.add(user)#like qo'shadi
        return HttpResponseRedirect(reverse("game", args=[str(pk)]))#game urlga yo'naladi
    else:
        return HttpResponseRedirect(reverse('login'))