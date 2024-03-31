from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from orders.models import Order,OrderItem
from .models import Comment,CommentImage
from products.models import Product
from django.views import generic
from .forms import CommentCreateForm
from django.contrib.auth import mixins
# Create your views here.

class CommentDetailView(mixins.LoginRequiredMixin,generic.DetailView):
    login_url = 'log_in'
    model = Comment
    template_name = 'comment_detail.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        pk=self.kwargs.get('pk')
        comment=Comment.objects.get(pk=pk)
        comment_images = list(comment.image.values_list('pk', flat=True))
        images = []
        for pk in comment_images:
            image = CommentImage.objects.get(pk=pk)
            images.append(image)
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
        context['comment']=comment
        context['images']=images
        return context
class CommentCreateView(mixins.LoginRequiredMixin,generic.CreateView):
    login_url = 'log_in'
    template_name = 'comment_create.html'
    form_class = CommentCreateForm
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
            slug=kwargs.get('slug')
            product=Product.objects.get(slug=slug)
            form = CommentCreateForm(request.POST, request.FILES)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.product=product
                comment.customer=request.user
                comment.save()
                for image1 in images:
                    image2 = CommentImage(
                        product_name=product.name,
                        image=image1
                    )
                    image2.save()
                    comment.image.add(image2)
                return HttpResponseRedirect(reverse("comment_detail", kwargs={'pk':comment.pk}))
            else:
                return render(request,self.template_name,context={'form':form})