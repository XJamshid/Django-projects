from django.db.models import Count
from django.views import generic
from categories.models import Category
from games.models import Screenshots,Game
from django.core.paginator import  Paginator
# Create your views here.

class HomePageView(generic.ListView):
    template_name = 'home.html'
    model = Game
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        games = Game.objects.annotate(num_likes=Count("likes"))
        filter = self.request.GET.get('filter')
        # request ichida selectning optionidagi valueni olamiz
        if filter != 'None' and filter is not None:
            #filter 'None' bo'lmasa yoki None bo'masa gamesni filterlaymiz
            if filter=='name':
                games = games.order_by(filter)
            else:
                #querysetni filter bo'yicha teskarisiga order qilamiz
                games = games.order_by(filter).reverse()
        else:
            #Agar filter tanlanmasa sana bo'yich teskarisiga order qilamiz
            games = games.order_by('-release_date')
        #Pagination jarayoni
        p = Paginator(games, 8)
        page = self.request.GET.get('page')
        games_list = p.get_page(page)
        context['games_list'] = games_list
        return context
class CategoriesView(generic.ListView):
    template_name = 'categories.html'
    model = Category
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        categories=Category.objects.all().order_by('name')
        context['categories']=categories
        return context
class PopularGamesListView(generic.ListView):
    template_name = 'home.html'
    model=Game
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        games = Game.objects.annotate(num_likes=Count("likes"))
        filter = self.request.GET.get('filter')
        games_pk = games.order_by('-num_likes').values_list('pk', flat=True)[:32]
        #o'yinlarni likelar soni bo'yicha tartiblaganda eng ko'p like bo'lgan 32 o'yinning idlar ro'yxatini olamiz
        games = games.filter(pk__in=games_pk)#Shu o'yinlarning querysetini olamiz
        #annotate methodi ichida
        #Count funksiyasi yordamida num_likes nomli qo'shimcha ustun yaratdik
        #djangoproject.com ning Query Expressions bo'limida to'liq malumot bor
        if filter != 'None' and filter is not None:
            if filter == 'name':
                games = games.order_by(filter)
            else:
                games = games.order_by(filter).reverse()
        else:
            games=games.order_by('-num_likes')
        #o'yinlarni like lar soni(num_likes ustunida beriladi ) bo'yicha kamayish bo'yicha tartibladik
        #va 32 ta sini oldik
        p = Paginator(games, 8)
        page = self.request.GET.get('page')
        games_list = p.get_page(page)
        context['games_list'] = games_list
        return context
class NewGamesListView(generic.ListView):
    template_name = 'home.html'
    model = Game
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        games = Game.objects.annotate(num_likes=Count("likes"))
        games_pk = games.order_by('-release_date').values_list('pk', flat=True)[:32]
        games = games.filter(pk__in=games_pk)
        filter = self.request.GET.get('filter')
        if filter != 'None' and filter is not None:
            if filter == 'name':
                games = games.order_by(filter)
            else:
                games = games.order_by(filter).reverse()
        else:
            games=games.order_by('-release_date')
        p = Paginator(games, 8)
        page = self.request.GET.get('page')
        games_list = p.get_page(page)
        context['games_list'] = games_list
        return context
class SearchView(generic.ListView):
    template_name = 'search.html'
    model=Game
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        name=self.request.GET.get('name')
        games=Game.objects.filter(name__icontains=name).order_by('-release_date')
        context['games'] = games
        return context