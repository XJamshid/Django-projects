from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy,reverse
from django.views import generic,View
from .forms import CustomerCreationForm,LoginForm,CustomerChangeForm
from orders.models import Order,OrderItem
from products.models import Product,ProductImage
from django.contrib.auth import login, authenticate, logout
from .models import Customer
from django.contrib.auth import mixins
from django.contrib.auth.decorators import login_required

# Create your views here.

class AccountDetailView(mixins.LoginRequiredMixin,View):
    login_url = 'log_in'
    template_name = 'account_detail.html'
    def get(self,request,*args,**kwargs):
        context={}
        if self.request.user.is_authenticated:
            order = Order.objects.get(customer=self.request.user, complete=False)
            num_order_items = list(OrderItem.objects.filter(order=order).values_list('quantity', flat=True))
            num_order_items = sum(num_order_items)
            num_wishlist = Product.objects.filter(likes__pk=self.request.user.pk).count()
        else:
            num_order_items = 0
            num_wishlist = 0
        context['num_wishlist'] = num_wishlist
        context['num_order_items'] = num_order_items
        context['customer']=request.user
        return render(request,self.template_name,context=context)
class ProfieDetailView(mixins.LoginRequiredMixin,View):
    login_url = "log_in"
    template_name='profile.html'
    def get(self, request, *args, **kwargs):
        context = {}
        customer=Customer.objects.get(pk=request.user.pk)
        if self.request.user.is_authenticated:
            order = Order.objects.get(customer=self.request.user, complete=False)
            num_order_items = list(OrderItem.objects.filter(order=order).values_list('quantity', flat=True))
            num_order_items = sum(num_order_items)
            num_wishlist = Product.objects.filter(likes__pk=self.request.user.pk).count()
        else:
            num_order_items = 0
            num_wishlist = 0
        context['num_wishlist'] = num_wishlist
        context['num_order_items'] = num_order_items
        form=CustomerChangeForm(instance=customer)
        context['customer'] = customer
        context['form']=form
        return render(request, self.template_name, context=context)
    def post(self,request,*args,**kwargs):
        customer=Customer.objects.get(pk=request.user.pk)
        form=CustomerChangeForm(request.POST,instance=customer)
        #instance berilgan bo'lsa save() methodi bu objectni yangilaydi aks holda yangi obyekt yaratadi
        if form.is_valid():
            form.save()
        else:
            return render(request,self.template_name,{'form':form})
        return HttpResponseRedirect(reverse('home'))
class SignUpView(generic.CreateView):
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('log_in')
    form_class = CustomerCreationForm
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            order = Order.objects.get(customer=self.request.user, complete=False)
            num_order_items = list(OrderItem.objects.filter(order=order).values_list('quantity', flat=True))
            num_order_items = sum(num_order_items)
            num_wishlist = Product.objects.filter(likes__pk=self.request.user.pk).count()
        else:
            num_order_items = 0
            num_wishlist = 0
        context['num_wishlist']=num_wishlist
        context['num_order_items'] = num_order_items
        return context
def LoginView(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                order,created=Order.objects.get_or_create(customer=user,complete=False)
                return HttpResponseRedirect(reverse("home"))
            else:
                message = 'Please enter a correct username and password. Note that both fields may be case-sensitive.'
    num_order_items = 0
    num_wishlist = 0
    return render(request, 'registration/login.html', context={'form': form, 'message': message,'num_order_items':num_order_items,'num_wishlist':num_wishlist})

@login_required(login_url='log_in')
def LogoutView(request):
    order = Order.objects.get(customer=request.user, complete=False)
    wishlist=Product.objects.filter(likes__pk=request.user.pk)
    order.delete()
    wishlist.delete()
    logout(request)
    return HttpResponseRedirect(reverse('home'))
