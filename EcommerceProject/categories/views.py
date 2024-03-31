from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.db.models import Avg, Sum
from django.views import generic
from categories.models import Category
from products.models import Product,ProductImage
from orders.models import Order,OrderItem
from .forms import CategoryCreateForm
from django.contrib.auth import mixins

# Create your views here.

class CategoryDetailView(mixins.LoginRequiredMixin,generic.DetailView):
    login_url = 'log_in'
    template_name = 'category.html'
    model = Category
    context_object_name = 'category'
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
            is_liked = product.likes.filter(pk=self.request.user.pk).exists()
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
        category = self.get_object()
        categories=Category.objects.all()
        discounts = Product.objects.filter(category=category).filter(discount=True).filter(count__gt=0)[:30]
        products=Product.objects.filter(category=category).filter(count__gt=0)
        ordering_field=self.request.GET.get('ordering')
        if ordering_field:
            if ordering_field == '-rating':
                products = products.annotate(rating=Avg("comment__rating"))
            if ordering_field == '-orders':
                products = products.filter(orderitem__order__complete=True).annotate(orders=Sum('orderitem__quantity'))
            products = products.order_by(ordering_field)
        count=products.count()
        products=self.get_product(products)
        p = Paginator(products, 12)
        page = self.request.GET.get('page')
        products = p.get_page(page)
        new_additions = Product.objects.filter(count__gt=0).order_by('-date_added')[:6]
        #new_additions = Product.objects.filter(category=category).filter(count__gt=0).order_by('-date_added')[:9]
        #Productlar kam bo'lgani uchun hozircha oxirgi qo'shilganlar sifatida umumiy oldim
        #Keyinchalik harbir kategoriya uchun alohida olaman
        new_additions = self.get_product(new_additions)
        p = Paginator(new_additions, 3)
        nums=list(range(p.num_pages))
        new_adds=[]
        for i in nums:
            new_adds.append(p.page(i+1).object_list)
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
        context['discounts']=self.get_product(discounts)
        context['categories']=categories
        context['products']=products
        context['new_additions'] = new_adds
        context['count']=count
        return context
class CategoryCreateView(mixins.LoginRequiredMixin,mixins.UserPassesTestMixin,generic.CreateView):
    login_url = 'log_in'
    form_class = CategoryCreateForm
    model = Category
    template_name = 'category_create.html'
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
class CategoryUpdateView(mixins.LoginRequiredMixin,mixins.UserPassesTestMixin,generic.UpdateView):
    login_url = 'log_in'
    model = Category
    template_name = 'category_update.html'
    fields = ['name','slug']
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
class CategoryDeleteView(mixins.LoginRequiredMixin,mixins.UserPassesTestMixin,generic.DeleteView):
    login_url = 'log_in'
    model = Category
    template_name = 'category_delete.html'
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