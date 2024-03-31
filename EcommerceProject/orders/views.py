from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views import generic,View
from .models import Order,OrderItem
from products.models import Product,ProductImage
from django.contrib.auth import mixins
from django.contrib.auth.decorators import login_required
# Create your views here.
class CartDetailView(mixins.LoginRequiredMixin,View):
    login_url = 'log_in'
    template_name = 'cart.html'
    def get(self,request,*args, **kwargs):
        context= {}
        order=Order.objects.get(complete=False,customer__pk=request.user.pk)
        orderitem_pks=OrderItem.objects.filter(order=order).values_list('pk',flat=True)
        order_items=[]
        cart_total=0
        for pk in orderitem_pks:
            product_dict={}
            orderitem=OrderItem.objects.get(pk=pk)
            product=orderitem.product
            product_dict['name']=product.name
            if product.discount:
                price=product.discount_price
            else:
                price=product.price
            images=ProductImage.objects.filter(product=product).values_list('pk',flat=True)
            image=ProductImage.objects.get(pk=images[0])
            cart_total+=price*orderitem.quantity
            product_dict['price']=price
            product_dict['slug']=product.slug
            product_dict['count']=product.count
            product_dict['total_price']=price*orderitem.quantity
            product_dict['quantity']=orderitem.quantity
            product_dict['pk']=orderitem.pk
            product_dict['image']=image
            order_items.append(product_dict)
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
        is_empty=OrderItem.objects.filter(order=order).exists()
        context['order']=order
        context['is_empty']=is_empty
        context['order_items']=order_items
        context['cart_total']=cart_total
        return render(request, self.template_name, context=context)
class OrderItemCreateView(mixins.LoginRequiredMixin,generic.CreateView):
    login_url = 'log_in'
    model = OrderItem
    def post(self, request, *args, **kwargs):
        product = Product.objects.get(slug=kwargs.get('slug'))
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        if OrderItem.objects.filter(product=product, order=order).exists():
            orderitem = OrderItem.objects.get(product=product, order=order)
            orderitem.quantity += 1
            orderitem.save()
        else:
            OrderItem.objects.create(
                product=product,
                order=order,
                quantity=1
            )
        url = request.META['HTTP_REFERER']
        return HttpResponseRedirect(url)
class OrderItemUpdateView(mixins.LoginRequiredMixin,generic.UpdateView):
    login_url = 'log_in'
    model = OrderItem
    def post(self, request, *args, **kwargs):
        pk=kwargs.get('pk')
        orderitem_slugs=list(OrderItem.objects.filter(order__pk=pk).values_list('product__slug',flat=True))
        for slug in orderitem_slugs:
            orderitem=OrderItem.objects.get(order__pk=pk,product__slug=slug)
            quantity=request.POST.get(slug)
            orderitem.quantity=quantity
            orderitem.save()
        return HttpResponseRedirect(reverse('cart'))

@login_required(login_url='log_in')
def OrderItemDeleteView(request,pk):
    OrderItem.objects.filter(pk=pk).delete()
    return HttpResponseRedirect(reverse('cart'))
