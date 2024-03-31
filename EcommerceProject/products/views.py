from django.core.paginator import Paginator
from django.urls import reverse,reverse_lazy
from django.db.models import Avg, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic,View
from .models import Product,ProductImage
from categories.models import Category
from orders.models import Order,OrderItem
from comments.models import Comment,CommentImage
from .forms import ProductCreateForm
from django.contrib.auth import mixins
# Create your views here.


class ProductDetailView(mixins.LoginRequiredMixin,generic.DetailView):
    login_url = 'log_in'
    template_name = 'product.html'
    model = Product
    def get_product(self,products):
        product_pks=list(products.values_list('pk',flat=True))
        customer=self.request.user
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
        product=self.get_object()
        images=ProductImage.objects.filter(product=product).values_list('pk',flat=True)
        image_urls=[]
        for pk in images:
            image_url=ProductImage.objects.get(pk=pk).image.url
            image_urls.append(image_url)
        product = Product.objects.filter(pk=product.pk).annotate(rating=Avg("comment__rating")).get()
        if product.rating is not None:
             rating=round(product.rating, 1)
        else:
            rating=0
        orders = OrderItem.objects.filter(product__pk=product.pk).filter(order__complete=True).annotate(
            num_orders=Sum("quantity"))
        orders = list(orders.values_list('num_orders', flat=True))
        num_orders = sum(orders)
        category = product.category
        related_products = Product.objects.filter(category=category).exclude(pk=product.pk).annotate(
            rating=Avg("comment__rating"))
        related_products = related_products.order_by('-rating')[:40]
        related_products=self.get_product(related_products)
        p = Paginator(related_products, 4)
        page = self.request.GET.get('page')
        related_products = p.get_page(page)
        comment_list = Comment.objects.filter(product__pk=product.pk)
        paginator = Paginator(comment_list, 5)
        page = self.request.GET.get('page1')
        comments = paginator.get_page(page)
        if self.request.user.is_authenticated:
            order = Order.objects.get(customer=self.request.user, complete=False)
            num_order_items = list(OrderItem.objects.filter(order=order).values_list('quantity', flat=True))
            num_order_items = sum(num_order_items)
            wishlist = Product.objects.filter(likes__pk=self.request.user.pk).count()
        else:
            num_order_items = 0
            wishlist = 0
        is_liked = product.likes.filter(pk=self.request.user.pk).exists()
        context['is_liked'] = is_liked
        context['categories'] = Category.objects.all()
        context['product']=product
        context['main_image']=image_urls[0]
        context['images']=image_urls
        context['rating']=rating
        context['orders']=num_orders
        context['related_products']=related_products
        context['num_order_items']=num_order_items
        context['num_wishlist'] = wishlist
        context['comments'] = comments
        return context

class ProductCreateView(mixins.LoginRequiredMixin,mixins.UserPassesTestMixin,generic.CreateView):
    login_url = 'log_in'
    template_name = 'product_create.html'
    form_class = ProductCreateForm
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
        context['num_wishlist'] = num_wishlist
        context['num_order_items'] = num_order_items
        return context
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            images = request.FILES.getlist('image')
            form = ProductCreateForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.save()
                for image1 in images:
                    image2 = ProductImage(
                        product_name=product.name,
                        image=image1
                    )
                    image2.save()
                    product.image.add(image2)
                return HttpResponseRedirect(reverse("product", kwargs={'slug':product.slug}))
            else:
                return render(request,self.template_name,context={'form':form})
    def  test_func(self):
        return self.request.user.is_superuser
class ProductDeleteView(mixins.LoginRequiredMixin,mixins.UserPassesTestMixin,generic.DeleteView):
    login_url = 'log_in'
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('home')
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
        context['num_wishlist'] = num_wishlist
        context['num_order_items'] = num_order_items
        return context
    def  test_func(self):
        return self.request.user.is_superuser
class ProductUpdateView(mixins.LoginRequiredMixin,mixins.UserPassesTestMixin,generic.UpdateView):
    login_url = 'log_in'
    model = Product
    template_name = 'product_update.html'
    success_url = reverse_lazy('home')
    fields = [
            'name',
            'brand',
            'description',
            'price',
            'count',
            'discount',
            'discount_price',
            'category',
            'image',
            'slug',
    ]
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            order=Order.objects.get(customer=self.request.user,complete=False)
            num_order_items=list(OrderItem.objects.filter(order=order).values_list('quantity',flat=True))
            num_order_items=sum(num_order_items)
            num_wishlist=Product.objects.filter(likes__pk=self.request.user.pk).count()
        else:
            num_order_items=0
            num_wishlist=0
        context['num_wishlist']=num_wishlist
        context['num_order_items'] = num_order_items
        return context
    def  test_func(self):
        return self.request.user.is_superuser
class LikeView(mixins.LoginRequiredMixin,View):
    login_url = 'log_in'
    def post(self,request,*args,**kwargs):
        slug=kwargs.get('slug')
        product=Product.objects.get(slug=slug)
        user = request.user
        if product.likes.filter(pk=user.pk).exists():
            product.likes.remove(user)
        else:
            product.likes.add(user)
        url=request.META['HTTP_REFERER'] # bu oldingi url ni qaytaradi
        return HttpResponseRedirect(url) # post qilingan urlga qaytaradi
