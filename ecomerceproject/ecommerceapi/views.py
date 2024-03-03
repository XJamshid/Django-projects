from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CategoryProductListFilter,ProductsOrderingFilter
from .paginations import Pagination
from rest_framework import filters, status
from rest_framework.views import APIView
from rest_framework import reverse, response, generics
from .models import Product,Customer,Category,Order,OrderItem,ShippingAddress,Shipment,Comment,CommentImage,ProductImage
from rest_framework.authtoken.models import Token
from .serializers import (
    ProductListSerializer,
    CategoryListSerializer,
    AccountDetailSerializer,
    CartDetailSerializer,
    ProductDetailSerializer,
    CartItemCreateSerializer,
    CartCreateSerializer,
    CartItemQuantityUpdateSerializer,
    ShippingAddressSerializer,
    ShipmentListSerializer,
    RegistrationSerializer,
    CommentAddSerializer,
    ProfileDetailSerializer,
    #ProductAddSerializer,
    #ProductImageAddSerializer,
    #CategoryAddSerializer,
)
class UrlsAPIView(APIView):
    def get(self,request,*args,**kwargs):
        home=reverse.reverse('home',request=request)
        products=reverse.reverse('products',request=request)
        categories=reverse.reverse('categories',request=request)
        #products_add=reverse.reverse('products_add',request=request)
        cart=reverse.reverse('cart',request=request)
        #product_image_add=reverse.reverse('product_image_add',request=request)
        account=reverse.reverse('account',request=request)
        #category_add=reverse.reverse('category_add',request=request)
        return response.Response({'home':home,'products':products,'categories':categories,'cart':cart,'account':account})

class HomeListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    def get_queryset(self):
        products = Product.objects.filter(count__gt=0)
        return products
    def get(self,request,*args,**kwargs):
        recommendations=reverse.reverse('recommendations',request=request)
        low_prices= reverse.reverse('low_prices', request=request)
        new_additions = reverse.reverse('new_additions', request=request)
        return response.Response({'recommendations':recommendations,'low_prices':low_prices,'new_additions':new_additions})
class RecommendationsListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    def get_queryset(self):
        products = Product.objects.annotate(rating=Avg("comment__rating"))
        products=products.order_by('-rating')[:50]
        return products
class LowPricesListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    def get_queryset(self):
        products=Product.objects.annotate(rating=Avg("comment__rating"))
        return products
    def get(self,request,*args,**kwargs):
        products=self.get_queryset()
        product_list = {}
        categories_pk = list(Category.objects.values_list('pk', flat=True))
        for pk in categories_pk:
            category=Category.objects.get(pk=pk)
            product = products.filter(category=category)
            product = product.order_by('price', '-rating')[:5]
            serializer = self.get_serializer(product, many=True).data
            product_list[f'{category.name}']=serializer
        return response.Response(product_list)

class NewAdditionsListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    def get_queryset(self):
        products = Product.objects.order_by('-date_added')[:50]
        return products
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    filterset_fields = ['name']
    def get(self,request,*args,**kwargs):
        categories=self.get_queryset().order_by('name')
        serializer=self.get_serializer(categories,many=True)
        return response.Response(serializer.data)
"""class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryAddSerializer"""
class CartDetailAPIView(APIView):
    def get(self,request,*args,**kwargs):
        cart,created=Order.objects.get_or_create(customer=request.user,complete=False)
        serializer = CartDetailSerializer(cart,many=False)
        return response.Response(serializer.data)
class AccountDetailAPIView(generics.RetrieveAPIView):
    serializer_class = AccountDetailSerializer
    def get(self,request,*args,**kwargs):
        customer=Customer.objects.get(username=request.user.username)
        serializer=self.get_serializer(customer)
        return response.Response(serializer.data)
class ProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProfileDetailSerializer
    lookup_field = 'pk'
    def get_queryset(self):
        return Customer.objects.filter(pk=self.request.user.pk)
class CategoryProductListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    def get_queryset(self):
        slug=self.kwargs.get('slug')
        products = Product.objects.filter(count__gt=0).filter(category__slug=slug)
        return products
    def get(self,request,*args,**kwargs):
        products=self.get_queryset()
        #Filtering jarayoni
        ordering=ProductsOrderingFilter()
        products=ordering.filter_queryset(request,products,'category')
        filterset = CategoryProductListFilter(request.GET, queryset=products)
        #requestda kiritilgan filterlash parametrlari va querysetdan foydalanib object yaratadi
        if filterset.is_valid():
            products = filterset.qs
            #objectning filterlangan querysetini oldik
            # Pagination jarayoni
            paginator = Pagination()
            result_page = paginator.paginate_queryset(products, request)
            serializer = self.get_serializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return response.Response(filterset.errors)

class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ProductsOrderingFilter]
    filterset_class = CategoryProductListFilter
    search_fields = ['name', 'price']
    ordering_fields = ['name', 'price','date_added','rating','orders']
    #filterset_fields = ['name', 'price']
    pagination_class = Pagination
    def get_queryset(self):
        products = Product.objects.filter(count__gt=0)
        return products
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class =ProductDetailSerializer
    lookup_field = 'slug'
"""class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductAddSerializer
class ProductImageCreateAPIView(generics.CreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageAddSerializer"""
class CartItemCreateAPIView(generics.CreateAPIView):
    serializer_class = CartItemCreateSerializer
    def create(self, request, *args, **kwargs):
        product = Product.objects.get(slug=kwargs.get('slug'))
        order,created = Order.objects.get_or_create(customer=request.user,complete=False)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            quantity = serializer.validated_data['quantity']
            if int(quantity) > 0 and product.count-int(quantity) > 0:
                if OrderItem.objects.filter(product=product,order=order).exists():
                    orderitem=OrderItem.objects.get(product=product,order=order)
                    orderitem.quantity+=quantity
                    orderitem.save()
                else:
                    OrderItem.objects.create(
                        product=product,
                        order=order,
                        quantity=quantity
                    )
                return response.Response({'cart': reverse.reverse('cart',request=request)})
            else:
                return response.Response({'Error': 'The quantity cannot be less than 0 or there are not many products'})
        else:
            return response.Response(serializer.errors)
class CartCreateAPIView(generics.CreateAPIView):
    serializer_class = CartCreateSerializer
class CartItemQuantityUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CartItemQuantityUpdateSerializer
    lookup_field = 'pk'
    def update(self,request,*args,**kwargs):
        instance=OrderItem.objects.get(pk=kwargs.get('pk'))
        serializer = self.get_serializer(data=request.data)
        cart={'cart': reverse.reverse('cart',request=request)}
        if serializer.is_valid():
            instance.quantity = serializer.validated_data['quantity']
            if int(instance.quantity) > 0 and instance.product.count-int(instance.quantity) > 0:
                instance.save()
                return response.Response(cart)
            else:
                if int(instance.quantity) == 0:
                    instance.delete()
                    return response.Response({'Detail': 'The cart item was deleted'})
                else:
                    return response.Response({'Error': 'The quantity cannot be less than 0 or there are not many products'})
        else:
            return response.Response(serializer.errors)
class ShippingAddressCreateAPIView(generics.CreateAPIView):
    serializer_class = ShippingAddressSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            region=serializer.validated_data['region']
            city_or_district = serializer.validated_data['city_or_district']
            neighborhood = serializer.validated_data['neighborhood']
            street = serializer.validated_data['street']
            home_number = serializer.validated_data['home_number']
            post_code = serializer.validated_data['post_code']
            ShippingAddress.objects.create(
                customer=request.user,
                region=region,
                city_or_district=city_or_district,
                neighborhood=neighborhood,
                street=street,
                home_number=home_number,
                post_code=post_code,
            )
            return response.Response({'Shipping address':serializer.data,'shipment':reverse.reverse('shipment',request=request)})
        else:
            return response.Response(serializer.errors)
class ShippingAddressListAPIView(generics.ListAPIView):
    serializer_class = ShippingAddressSerializer
    def get_queryset(self):
        shhipping_adress=ShippingAddress.objects.filter(customer=self.request.user)
        return shhipping_adress
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        pks=list(queryset.values_list('pk',flat=True))
        serializer = self.get_serializer(queryset, many=True)
        data=list(serializer.data)
        address_list=[]
        for i in list(range(len(data))):
            address=data[i]
            editting_url=f"{reverse.reverse('shipping_address_edit',kwargs={'pk':pks[i]},request=request)}"
            address_list.append(
                {
                    'region': address['region'],
                    'city_or_district': address['city_or_district'],
                    'neighborhood': address['neighborhood'],
                    'street': address['street'],
                    'home_number': address['home_number'],
                    'post_code':address['post_code'],
                    'edit_address':editting_url
                }
            )
        return response.Response({'Shipping address':address_list})
class ShippingAddressUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ShippingAddressSerializer
    queryset = ShippingAddress.objects.all()
    lookup_field = 'pk'

class ShipmentAPIView(generics.CreateAPIView):
    serializer_class = ShippingAddressSerializer#ShipmentSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        order,created = Order.objects.get_or_create(customer=request.user,complete=False)
        orderitems = OrderItem.objects.filter(order=order)
        if serializer.is_valid(raise_exception=True):
            if orderitems.exists():
                region=serializer.validated_data['region']
                city_or_district = serializer.validated_data['city_or_district']
                neighborhood = serializer.validated_data['neighborhood']
                street = serializer.validated_data['street']
                home_number = serializer.validated_data['home_number']
                post_code = serializer.validated_data['post_code']
                address,created=ShippingAddress.objects.get_or_create(
                    customer=request.user,
                    region=region,
                    city_or_district=city_or_district,
                    neighborhood=neighborhood,
                    street=street,
                    home_number=home_number,
                    post_code=post_code,
                )
                Shipment.objects.create(
                    customer=request.user,
                    order=order,
                    address=address
                )
                order.complete = True
                order.save()
                Order.objects.create(customer=request.user)
                for pk in list(orderitems.values_list('product',flat=True)):
                    product=Product.objects.get(pk=pk)
                    quantity=OrderItem.objects.get(product=product,order=order).quantity
                    product.count=product.count-quantity
                    product.save()
                return response.Response({'Detail':'Shipping was completed'})
            else:
                return response.Response({'Error': 'Product not selected'})
        else:
            return response.Response(serializer.errors)
class ShipmentListAPIView(generics.ListAPIView):
    serializer_class = ShipmentListSerializer
    queryset = Shipment.objects.all().order_by('-purchase_time')
class CustomerShipmentListAPIView(generics.ListAPIView):
    serializer_class = ShipmentListSerializer
    def get_queryset(self):
        shipments=Shipment.objects.filter(customer=self.request.user).order_by('-purchase_time')
        return shipments
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        orderitmes = []
        #order={}
        serializer = self.get_serializer(queryset, many=True)
        data=list(serializer.data)
        for i in list(range(len(data))):
            address=data[i]['address']
            address=f"{address['post_code']}, {address['region']}, {address['city_or_district']}, {address['neighborhood']}, {address['street']}, {address['home_number']}"
            for j in list(range(len(data[i]['order']['orderitems']))):
                orderitem=data[i]['order']['orderitems'][j]
                product=Product.objects.get(name=orderitem['product']['name'])
                orderitmes.append({
                    'product':orderitem['product'],
                    'quantity':orderitem['quantity'],
                    'total_cost':orderitem['total_cost'],
                    'purchase_time':data[i]['purchase_time'],
                    'address':address,
                    'comment':reverse.reverse('comment_create',kwargs={'slug':product.slug},request=request)
                })
        return response.Response({'shipments':orderitmes})
class RegistrationAPIVIew(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            data={}
            if serializer.is_valid():
                customer=serializer.save()
                data['response']='Successfully register a new customer'
                data['first_name'] = customer.email
                data['last_name'] = customer.last_name
                data['date_of_birth'] = customer.date_of_birth
                data['username'] = customer.username
                data['email'] = customer.email
                data['password'] = customer.password
                token=Token.objects.get(user=customer).key
                data['token']=token
                Order.objects.create(customer=customer)
            else:
                data=serializer.errors
            return response.Response(data)
class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentAddSerializer
    def create(self, request, *args, **kwargs):
        product = Product.objects.get(slug=kwargs.get('slug'))
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            body = serializer.validated_data['body']
            rating = serializer.validated_data['rating']
            images=serializer.validated_data['image']
            comment=Comment.objects.create(
                body=body,
                customer=request.user,
                product=product,
                rating=rating,
            )
            for image in images:
                comment.image.add(image)
            return response.Response({'product': reverse.reverse('product',kwargs={'slug':kwargs.get('slug')}, request=request)})
        else:
            return response.Response(serializer.errors)

class LikeAPIView(APIView):
    def post(self,request,*args,**kwargs):
        slug=kwargs.get('slug')
        product=Product.objects.get(slug=slug)
        user = request.user
        if product.likes.filter(pk=user.pk).exists():
            product.likes.remove(user)
        else:
            product.likes.add(user)
        return response.Response(
            {'product': reverse.reverse('product', kwargs={'slug': slug}, request=request)})
class WishListAPIView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    def get_queryset(self):
        products=Product.objects.filter(likes=self.request.user)
        return products
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)
class OrderItemDeleteView(APIView):
    def delete(self, request, *args, **kwargs):
        pk=kwargs.get('pk')
        instance = OrderItem.objects.get(pk=pk)
        instance.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)