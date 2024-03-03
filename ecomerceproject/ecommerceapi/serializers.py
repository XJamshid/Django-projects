
from django.db.models import Count, Avg
from rest_framework import serializers , reverse
from .models import Product,ProductImage,Category,Customer,Order,OrderItem,ShippingAddress,Shipment,Comment,CommentImage
class ProductListSerializer(serializers.ModelSerializer):
    image=serializers.SerializerMethodField(read_only=True)
    detail=serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    rating=serializers.SerializerMethodField(read_only=True)
    add_to_cart=serializers.HyperlinkedIdentityField(view_name='add_to_cart',lookup_field='slug')
    #orders=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Product
        fields=[
            'image',
            'rating',
            'count',
            'name',
            'price',
            'num_orders',
            'detail',
            'add_to_cart'
        ]
    def get_image(self,obj):
        images=Product.objects.filter(pk=obj.pk).values_list('image__pk',flat=True)
        images=list(images)
        image=ProductImage.objects.get(pk=images[0])
        return f"http://127.0.0.1:8000{image.image.url}"
    """def get_orders(self,obj):
        orders=OrderItem.objects.filter(product=obj).filter(order__complete=True).annotate(num_orders=Sum("quantity"))
        #Yuqorida OrderItemlar ichidan product i obj bo'lganlarining
        #Buyurtirilgan order larga kiruvchilarini quantity bo'yicha yi'gindilari bo'yciha ustun hosil qiladi
        orders=list(orders.values_list('num_orders',flat=True))
        #QuerySetni quantitylar ro'yxati ko'rinishida olish
        #[8,3,5]kabi
        num_orders=sum(orders)
        #va ro'yxatdagilarni yig'ib chiqish
        return num_orders"""
    def get_detail(self,obj):
        request=self.context.get('request')
        return reverse.reverse('product',kwargs={'slug':obj.slug},request=request)
    def get_rating(self,obj):
        product = Product.objects.filter(pk=obj.pk).annotate(rating=Avg("comment__rating")).get()
        if product.rating is not None:
            return round(product.rating,1)
        else:
            return 0
    def get_price(self,obj):
        price= {}
        if obj.discount:
            price['old_price']=obj.price
            price['discount_price']=obj.discount_price
            return price
        else:
            return obj.price
class CategoryListSerializer(serializers.ModelSerializer):
    products=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Category
        fields=[
            'name',
            'products'
        ]
    def get_products(self,obj):
        request = self.context.get('request')
        return reverse.reverse('category',kwargs={'slug':obj.slug},request=request)
"""class CategoryAddSerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=[
            'name',
            'slug'
        ]"""
class CartItemDetailSerializer(serializers.ModelSerializer):
    product=serializers.SerializerMethodField(read_only=True)
    total_cost=serializers.SerializerMethodField(read_only=True)
    update_quantity=serializers.SerializerMethodField(read_only=True)
    product_remove = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=OrderItem
        fields=[
            'product',
            'quantity',
            'update_quantity',
            'product_remove',
            'total_cost',
        ]
    def get_total_cost(self,obj):
        if obj.product.discount:
            return obj.product.discount_price*obj.quantity
        else:
            return obj.product.price*obj.quantity
    def get_update_quantity(self,obj):
        request = self.context.get('request')
        return f"http://127.0.0.1:8000{reverse.reverse('update_quantity',kwargs={'pk':obj.pk},request=request)}"
    def get_product_remove(self,obj):
        request = self.context.get('request')
        return f"http://127.0.0.1:8000{reverse.reverse('product_remove',kwargs={'pk':obj.pk},request=request)}"
    def get_product(self,obj):
        images = Product.objects.filter(pk=obj.product.pk).values_list('image__pk', flat=True)
        images = list(images)
        image = ProductImage.objects.get(pk=images[0])
        if obj.product.discount:
            price=obj.product.discount_price
        else:
            price=obj.product.price
        return {
            'image': f"http://127.0.0.1:8000{image.image.url}",
            'name':obj.product.name,
            'price':price
        }
class CartDetailSerializer(serializers.ModelSerializer):
    customer=serializers.SerializerMethodField(read_only=True)
    orderitems=serializers.SerializerMethodField(read_only=True)
    shipping_address = serializers.SerializerMethodField(read_only=True)
    shipment = serializers.SerializerMethodField(read_only=True)
    total_cost = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Order
        fields=[
            'customer',
            'date_ordered',
            'complete',
            'orderitems',
            'total_cost',
            'shipping_address',
            'shipment',
        ]
    def get_customer(self,obj):
        customer=obj.customer
        return customer.username
    def get_orderitems(self,obj):
        orderitems=OrderItem.objects.filter(order__pk=obj.pk)
        serializer=CartItemDetailSerializer(orderitems,many=True)
        return serializer.data
    def get_shipping_address(self,obj):
        request = self.context.get('request')
        return f"http://127.0.0.1:8000{reverse.reverse('shipping_address_create',request=request)}"
    def get_shipment(self,obj):
        request = self.context.get('request')
        return f"http://127.0.0.1:8000{reverse.reverse('shipment',request=request)}"
    def get_total_cost(self,obj):
        data=self.get_orderitems(obj)
        size=len(data)
        total_cost=0
        for i in list(range(size)):
            total_cost+=data[i]["total_cost"]
        return total_cost
class CartItemQuantityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=[
            'quantity'
        ]
class ImageSerializer(serializers.RelatedField):
    def to_representation(self,value):
        return f"http://127.0.0.1:8000{value.image.url}"

class CommentAddSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=[
            'body',
            'rating',
            'image'
        ]
class CommentDetailSerializer(serializers.ModelSerializer):
    customer=serializers.SerializerMethodField(read_only=True)
    images = ImageSerializer(source='image', many=True, read_only=True)
    #iamge desam xato beradi maydonlaridan farqli nom berish kerak
    class Meta:
        model=Comment
        fields=[
            'customer',
            'images',
            'body',
            'rating',
            'date'
        ]
    def get_customer(self,obj):
        return obj.customer.username
class ProductDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(source='image',many=True, read_only=True)
    category=serializers.SerializerMethodField(read_only=True)
    comment_create=serializers.HyperlinkedIdentityField(view_name='comment_create',lookup_field='slug')
    add_to_cart=serializers.HyperlinkedIdentityField(view_name='add_to_cart',lookup_field='slug')
    comments=serializers.SerializerMethodField(read_only=True)
    num_likes=serializers.SerializerMethodField(read_only=True)
    like=serializers.SerializerMethodField(read_only=True)
    related_products=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Product
        fields=[
            'images',
            'name',
            'brand',
            'category',
            'price',
            'description',
            'num_likes',
            'comments',
            'add_to_cart',
            'comment_create',
            'like',
            'related_products'
        ]
    def get_category(self,obj):
        request=self.context.get('request')
        slug=obj.category.slug
        return reverse.reverse('category',kwargs={'slug':slug},request=request)
    def get_comments(self,obj):
        comments=Comment.objects.filter(product=obj)
        return CommentDetailSerializer(comments,many=True).data
    def get_num_likes(self,obj):
        product = Product.objects.filter(pk=obj.pk).annotate(num_likes=Count("likes")).get()
        return product.num_likes
    def get_like(self,obj):
        request=self.context.get('request')
        slug = obj.slug
        return reverse.reverse('like', kwargs={'slug': slug}, request=request)
    def get_related_products(self,obj):
        request = self.context.get('request')
        category=obj.category
        related_products=Product.objects.filter(category=category).exclude(pk=obj.pk).annotate(rating=Avg("comment__rating"))
        related_products=related_products.order_by('-rating')[:10]
        return ProductListSerializer(related_products,many=True,context={'request':request}).data
"""class ProductImageAddSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields=[
            'image',
            'product_name'
        ]
class ProductAddSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=[
            'name',
            'brand',
            'category',
            'price',
            'count',
            'discount',
            'discount_price',
            'description',
            'image',
            'slug'
        ]"""
class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=[
            'quantity',
        ]
class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'customer',
        ]
class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShippingAddress
        fields=[
            'region',
            'city_or_district',
            'neighborhood',
            'street',
            'home_number',
            'post_code'
        ]
class ShipmentListSerializer(serializers.ModelSerializer):
    order=serializers.SerializerMethodField(read_only=True)
    total_cost=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Shipment
        depth=1
        fields=[
            'order',
            'address',
            'purchase_time',
            'total_cost'
        ]
    def get_order(self,obj):
        order=obj.order
        cart=Order.objects.get(pk=order.pk)
        serializer=CartDetailSerializer(cart)
        return serializer.data
    def get_total_cost(self,obj):
        cart=Order.objects.get(pk=obj.order.pk)
        serializer=CartDetailSerializer(cart)
        return serializer.data['total_cost']
class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=[
            'username',
            'first_name',
            'last_name',
            'email',
            'date_of_birth'
        ]
class AccountDetailSerializer(serializers.ModelSerializer):
    profile=serializers.SerializerMethodField(read_only=True)
    shipments=serializers.SerializerMethodField(read_only=True)
    create_shipping_address=serializers.SerializerMethodField(read_only=True)
    wishlist=serializers.SerializerMethodField(read_only=True)
    profile_edit = serializers.HyperlinkedIdentityField(view_name='profile_edit', lookup_field='pk')
    shipping_address = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Customer
        fields=[
            'profile',
            'profile_edit',
            'shipments',
            'wishlist',
            'shipping_address',
            'create_shipping_address',
        ]
    def get_profile(self,obj):
        profile=ProfileDetailSerializer(obj)
        return profile.data
    def get_shipments(self,obj):
        request = self.context.get('request')
        return reverse.reverse('customer_shipments', request=request)
    def get_create_shipping_address(self,obj):
        request=self.context.get('request')
        return reverse.reverse('shipping_address_create',request=request)
    def get_wishlist(self,obj):
        request=self.context.get('request')
        return reverse.reverse('wishlist',request=request)
    def get_shipping_address(self,obj):
        request = self.context.get('request')
        return reverse.reverse('shipping_address',request=request)
class RegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=Customer
        fields=[
            'first_name',
            'last_name',
            'date_of_birth',
            'username',
            'email',
            'password',
            'password2'
        ]
        extra_kwargs={
            'password':{'style':{'input_type':'password'},'write_only':True,}
        }
    def save(self):
        customer=Customer(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            date_of_birth=self.validated_data['date_of_birth'],
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match'})
        customer.password=password
        customer.save()
        return customer