from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic,View
from django.urls import reverse,reverse_lazy
from shipments.models import Shipment,ShippingAddress
from orders.models import Order,OrderItem
from categories.models import Category
from products.models import Product,ProductImage
from comments.models import Comment,CommentImage
from django.conf import settings
from .forms import CustomPayPalPaymentsForm,AddressForm
import uuid
from django.contrib.auth import mixins
from django.contrib.auth.decorators import login_required
# Create your views here.



class ShippingAddressView(mixins.LoginRequiredMixin,View):
    login_url = 'log_in'
    template_name = 'shipping_address.html'
    def get(self,request,*args,**kwargs):
        context = {}
        order = Order.objects.get(pk=kwargs.get('pk'))
        orderitem_pks = OrderItem.objects.filter(order=order).values_list('pk', flat=True)
        order_items = []
        cart_total = 0
        for pk in orderitem_pks:
            product_dict = {}
            orderitem = OrderItem.objects.get(pk=pk)
            product = orderitem.product
            product_dict['name'] = product.name
            if product.discount:
                price = product.discount_price
            else:
                price = product.price
            cart_total += price * orderitem.quantity
            product_dict['total_price'] = price * orderitem.quantity
            order_items.append(product_dict)
        cart_total = round(cart_total / 12000, 2)
        shipping_adds=ShippingAddress.objects.filter(customer=request.user)
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
        context['is_exists']=shipping_adds.exists()
        context['order']=order
        context['order_items'] = order_items
        context['cart_total'] = cart_total
        context['shipping_adds'] = shipping_adds
        context['categories'] = Category.objects.all()
        return render(request, self.template_name, context=context)
    def post(self,request,*args,**kwargs):
        #session=request.session
        if ShippingAddress.objects.filter(customer=request.user).exists():
            selected_address_pk=request.POST.get('selected_address')
            shipping_adds=ShippingAddress.objects.exclude(pk=selected_address_pk)
            shipping_adds.update(is_default=False)
            selected_address=ShippingAddress.objects.get(pk=selected_address_pk)
            selected_address.is_default=True
            selected_address.save()
        else:
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            phone=request.POST.get('phone')
            email=request.POST.get('email')
            region=request.POST.get('region')
            city_or_district=request.POST.get('city_or_district')
            neighborhood=request.POST.get('neighborhood')
            street=request.POST.get('street')
            home_number=request.POST.get('home_number')
            postcode=request.POST.get('postcode')
            shipping_address=ShippingAddress.objects.create(
                customer=request.user,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                region=region,
                city_or_district=city_or_district,
                neighborhood=neighborhood,
                street=street,
                home_number=home_number,
                post_code=postcode,
                is_default=True
            )
        return HttpResponseRedirect(reverse('checkout',kwargs={'pk':kwargs.get('pk')}))
@login_required(login_url = 'log_in')
def CheckoutView( request, *args, **kwargs):
    template_name = 'checkout_create.html'
    context = {}
    order = Order.objects.get(pk=kwargs.get('pk'))
    orderitem_pks = OrderItem.objects.filter(order=order).values_list('pk', flat=True)
    order_items = []
    cart_total = 0
    for pk in orderitem_pks:
        product_dict = {}
        orderitem = OrderItem.objects.get(pk=pk)
        product = orderitem.product
        product_dict['name'] = product.name
        if product.discount:
            price = product.discount_price
        else:
            price = product.price
        cart_total += price * orderitem.quantity
        product_dict['total_price'] = price * orderitem.quantity
        order_items.append(product_dict)
    cart_total=round(cart_total/12000,2)
    host = request.get_host()
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": str(cart_total),
        "item_name": f"{order.pk}",
        "invoice": str(uuid.uuid4()),
        'currency_code': 'USD',
        "notify_url": f"http://{host}{reverse('paypal-ipn')}",
        "return": f"http://{host}{reverse('checkout_success',kwargs={'pk':order.pk})}",
        "cancel_return": f"http://{host}{reverse('home')}",
    }
    form = CustomPayPalPaymentsForm(initial=paypal_dict)
    if request.user.is_authenticated:
        order = Order.objects.get(customer=request.user, complete=False)
        num_order_items = list(OrderItem.objects.filter(order=order).values_list('quantity', flat=True))
        num_order_items = sum(num_order_items)
        num_wishlist = Product.objects.filter(likes__pk=request.user.pk).count()
    else:
        num_order_items = 0
        num_wishlist = 0
    context['num_wishlist'] = num_wishlist
    context['num_order_items'] = num_order_items
    context['num_order_items'] = num_order_items
    context['order_items'] = order_items
    context['cart_total'] = cart_total
    context['categories'] = Category.objects.all()
    context['form'] = form
    return render(request, template_name, context=context)
@login_required(login_url = 'log_in')
def CheckoutReturnView(request,*args,**kwargs):
    order = Order.objects.get(pk=kwargs.get('pk'))
    orderitems = OrderItem.objects.filter(order=order)
    order.complete = True
    order.save()
    shipping_address = ShippingAddress.objects.get(customer=request.user, is_default=True)
    shipment = Shipment.objects.create(
        order=order,
        address=shipping_address
    )
    Order.objects.create(customer=request.user)
    for pk in list(orderitems.values_list('product', flat=True)):
        product = Product.objects.get(pk=pk)
        quantity = OrderItem.objects.get(product=product, order=order).quantity
        product.count = product.count - quantity
        product.save()
    return HttpResponseRedirect(reverse('home'))

class ShippingAddressListView(mixins.LoginRequiredMixin,generic.ListView):
    login_url = 'log_in'
    model = ShippingAddress
    template_name = 'shipping_address_list.html'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        customer=self.request.user
        shipping_address_list=ShippingAddress.objects.filter(customer=customer)
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
        context['shipping_address_list']=shipping_address_list
        return context
class ShippingAddressCreateView(mixins.LoginRequiredMixin,generic.CreateView):
    login_url = 'log_in'
    form_class = AddressForm
    model = ShippingAddress
    template_name = 'shipping_address_create.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        customer=self.request.user
        form=self.form_class(initial={
            'first_name':customer.first_name,
            'last_name':customer.last_name,
            'phone': customer.phone_number,
            'email': customer.email,
        })
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
        context['form']=form
        return context
    def post(self, request, *args, **kwargs):
        customer=request.user
        form=AddressForm(request.POST)
        if form.is_valid():
            address=form.save(commit=False)
            address.customer=customer
            address.save()
            return HttpResponseRedirect(reverse('shipping_address_list'))
        else:
            return render(request,self.get_template_names(),context={'form':form})
class ShippingAddressDetailView(mixins.LoginRequiredMixin,generic.DetailView):
    login_url = 'log_in'
    template_name='shipping_address_detail.html'
    model = ShippingAddress
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        address=ShippingAddress.objects.get(pk=self.kwargs.get('pk'))
        form=AddressForm(instance=address)
        shipment=Shipment.objects.filter(address=address)
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
        context['is_shipping_address']=shipment.exists()
        context['form']=form
        context['pk']=address.pk
        return context
    def post(self,request,*args,**kwargs):
        address=ShippingAddress.objects.get(pk=self.kwargs.get('pk'))
        shipment = Shipment.objects.filter(address=address)
        if shipment.exists():
            return HttpResponseRedirect(reverse('shipping_address_detail', kwargs={'pk': kwargs.get('pk')}))
        else:
            form = AddressForm(request.POST, instance=address)
            if form.is_valid():
                form.save()
            else:
                return render(request, self.template_name, {'form': form, 'pk': address.pk})
            return HttpResponseRedirect(reverse('shipping_address_list'))
@login_required(login_url = 'log_in')
def ShippingAddressDeleteView(request,pk):
    address=ShippingAddress.objects.get(pk=pk)
    shipment = Shipment.objects.filter(address=address)
    if shipment.exists():
        return HttpResponseRedirect(reverse('shipping_address_detail',kwargs={'pk':pk}))
    else:
        ShippingAddress.objects.filter(pk=pk).delete()
        return HttpResponseRedirect(reverse('shipping_address_list'))

class OrderListView(mixins.LoginRequiredMixin,generic.ListView):
    login_url = 'log_in'
    template_name = 'order_list.html'
    model = Shipment
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        shipment_pks=list(Shipment.objects.filter(order__customer__pk=self.request.user.pk).values_list('pk',flat=True))
        shipment_list=[]
        for pk in shipment_pks:
            shipping_address = ShippingAddress.objects.get(shipment__pk=pk)
            purchase_time=Shipment.objects.get(pk=pk).purchase_time
            orderitem_pks=list(OrderItem.objects.filter(order__shipment__pk=pk).values_list('pk',flat=True))
            for id in orderitem_pks:
                shipment = {}
                orderitem=OrderItem.objects.get(pk=id)
                shipment['orderitem']=orderitem
                shipment['address']=shipping_address
                shipment['purchase_time']=purchase_time
                shipment_list.append(shipment)
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
        context['shipment_list']=shipment_list
        return context

class ShipmentDetail(mixins.LoginRequiredMixin,generic.DetailView):
    login_url = 'log_in'
    template_name = 'shipment_detail.html'
    model = OrderItem
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        pk=self.kwargs.get('pk')
        orderitem=OrderItem.objects.get(pk=pk)
        images=list(orderitem.product.image.values_list('pk',flat=True))
        image=ProductImage.objects.get(pk=images[0])
        shipment=Shipment.objects.get(order__orderitem__pk=pk)
        shipping_address=ShippingAddress.objects.get(shipment=shipment)
        comment_list=Comment.objects.filter(product__pk=orderitem.product.pk)
        p = Paginator(comment_list, 10)
        page = self.request.GET.get('page')
        comments = p.get_page(page)
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
        context['orderitem']=orderitem
        context['purchase_time']=shipment.purchase_time
        context['shipping_address']=shipping_address
        context['image_url']=image.image.url
        context['comments']=comments
        return context
