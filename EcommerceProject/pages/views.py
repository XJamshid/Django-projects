from django.db.models import Avg
from django.shortcuts import render
from orders.models import Order,OrderItem
from django.views import generic
from django.views import View
from categories.models import Category
from products.models import Product,ProductImage
from django.contrib.auth import mixins
# Create your views here.

class Home(View):
    template_name = 'home.html'
    def get_product(self,products):
        product_pks=list(products.values_list('pk',flat=True))
        product_list=[]
        for pk in product_pks:
            products = {}
            images = Product.objects.filter(pk=pk).values_list('image__pk', flat=True)
            images = list(images)
            image = ProductImage.objects.get(pk=images[0])
            product = Product.objects.get(pk=pk)
            sale_off=100-product.discount_price/product.price*100
            is_liked=product.likes.filter(pk=self.request.user.pk).exists()
            products['is_liked'] = is_liked
            products['name'] = product.name
            products['price'] = product.price
            products['image'] = image.image
            products['discount']=product.discount
            products['discount_price']=product.discount_price
            products['sale_off']=round(sale_off)
            products['slug']=product.slug
            product_list.append(products)
        return product_list
    def get(self, request, *args, **kwargs):
        context={}
        products = Product.objects.filter(count__gt=0).annotate(rating=Avg("comment__rating"))
        recommendations = products.order_by('-rating')[:4]
        recommendations=self.get_product(recommendations)
        low_price_products = []
        categories_pk = list(Category.objects.values_list('pk', flat=True))
        for pk in categories_pk:
            category = Category.objects.get(pk=pk)
            low_prices = products.filter(category=category)
            low_prices = low_prices.order_by('price').filter(rating__gt=4.0)[:1]
            low_price_products+=self.get_product(low_prices)
        new_additions=Product.objects.filter(count__gt=0).order_by('-date_added')[:4]
        new_additions=self.get_product(new_additions)
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
        context['categories']=Category.objects.order_by('name')
        context['recommendations']=recommendations
        context['low_prices']=low_price_products
        context['new_additions'] = new_additions
        return render(request, self.template_name, context=context)

class WishListView(mixins.LoginRequiredMixin,generic.ListView):
    login_url = 'log_in'
    model = Product
    template_name = 'wish_list.html'
    def get_product(self,products):
        product_pks=list(products.values_list('pk',flat=True))
        product_list=[]
        for pk in product_pks:
            products = {}
            images = Product.objects.filter(pk=pk).values_list('image__pk', flat=True)
            images = list(images)
            image = ProductImage.objects.get(pk=images[0])
            product = Product.objects.get(pk=pk)
            sale_off=100-product.discount_price/product.price*100
            is_liked=product.likes.filter(pk=self.request.user.pk).exists()
            products['is_liked'] = is_liked
            products['name'] = product.name
            products['price'] = product.price
            products['image'] = image.image
            products['discount']=product.discount
            products['discount_price']=product.discount_price
            products['sale_off']=round(sale_off)
            products['slug']=product.slug
            product_list.append(products)
        return product_list
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        wishlist=Product.objects.filter(likes__pk=self.request.user.pk)
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
        context['wishlist']=self.get_product(wishlist)
        return context
class SearchView(mixins.LoginRequiredMixin,View):
    login_url = 'log_in'
    template_name='search_result.html'
    def get_product(self,products):
        product_pks=list(products.values_list('pk',flat=True))
        product_list=[]
        for pk in product_pks:
            products = {}
            images = Product.objects.filter(pk=pk).values_list('image__pk', flat=True)
            images = list(images)
            image = ProductImage.objects.get(pk=images[0])
            product = Product.objects.get(pk=pk)
            sale_off=100-product.discount_price/product.price*100
            is_liked=product.likes.filter(pk=self.request.user.pk).exists()
            products['is_liked'] = is_liked
            products['name'] = product.name
            products['price'] = product.price
            products['image'] = image.image
            products['discount']=product.discount
            products['discount_price']=product.discount_price
            products['sale_off']=round(sale_off)
            products['slug']=product.slug
            product_list.append(products)
        return product_list
    def get(self,request,*args,**kwargs):
        search=request.GET.get('search')
        if self.request.user.is_authenticated:
            order = Order.objects.get(customer=self.request.user, complete=False)
            num_order_items = list(OrderItem.objects.filter(order=order).values_list('quantity', flat=True))
            num_order_items = sum(num_order_items)
            num_wishlist = Product.objects.filter(likes__pk=self.request.user.pk).count()
        else:
            num_order_items = 0
            num_wishlist = 0
        result=Product.objects.filter(name__icontains=search)
        result=self.get_product(result)
        return render(request,self.template_name,context={'num_order_items':num_order_items,'num_wishlist':num_wishlist,'result':result})

