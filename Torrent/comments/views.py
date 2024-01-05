from django.http import HttpResponseRedirect, HttpResponse
from  django.urls import reverse
from django.shortcuts import render
from .models import Comments
from .forms import CommentAddForm
from django.views import generic
from games.models import Game
# Create your views here.
class CommentCreateView(generic.CreateView):
    model = Comments
    def post(self,request,*args,**kwargs):
        #formadan malumot olib MO ga qo'shamiz
        pk=kwargs.get('pk')
        game=Game.objects.get(pk=pk)
        if request.method == 'POST':
            # HTML formamda faqat Comment ning body qismi kiritganda author va sana avtomat qo'shiladigan qilish kerak
            form=CommentAddForm(request.POST)#form nomli obyekt yaratamiz requestdagi malumotlardan foydalanib
            #requestda faqat body berilgan
            if form.is_valid():#form dagi malumotlar to'g'rimligini tekshiramiz
                comment=form.save(commit=False)#comment nomli Commentsning obyektini yaratadi lekin malumotlar bazasiga saqlamaydi
                comment.author=request.user #commentning authorini comment qoldirgan foydalanuvchi qilib qo'ydik
                comment.game=game#commentga berilgan o'yinni bog'ladik
                comment.save()
                #body=form.cleaned_data.get('body')formadan malumotni olish
                return HttpResponseRedirect(reverse("game", args=[str(pk)]))#Malumotlar MOga saqlanadi va 'game' urlga yo'naltiriladi
            else:
                return HttpResponse(form.errors.as_data())#forma invalid bo'lsa xatolarni ko'rsatadi