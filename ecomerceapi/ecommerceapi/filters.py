import django_filters
from ecommerceapi.models import Product,OrderItem
from rest_framework import filters
from django.db.models import Count, Avg,Sum


class CategoryProductListFilter(django_filters.FilterSet):
    price=django_filters.RangeFilter()
    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],
            #'price': ['lt','gt'],
        }


class ProductsOrderingFilter(filters.OrderingFilter):
    allowed_custom_filters = ['name', 'price','date_added','rating','orders']
    """fields_related = {
        'user_city': 'user__city__name', # ForeignKey Field lookup for ordering
        'user_country': 'user__country__name'
    }"""
    def get_ordering(self, request, queryset, view):
        params = request.query_params.get(self.ordering_param)
        # http://127.0.0.1:8000/api/categories/elektronika/?ordering=nomi,narxi ni kiritsak
        #print(params) "nomi,narxi" ni qaytaradi
        if params:
            fields = [param.strip() for param in params.split(',')]
            #print(fields) ["nomi","narxi"] ni qaytaradi
            ordering = [f for f in fields if f.lstrip('-') in self.allowed_custom_filters]
            #ordering=[f for f in fields if f in self.allowed_custom_filters]
            if ordering:
                return ordering
        return self.get_default_ordering(view)

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            if ordering[0].lstrip('-')=='rating':
                queryset=queryset.annotate(rating=Avg("comment__rating"))
                #Yuqoridagi kodning mazmuni quyidagicha
                #Qabul qilingan querysetni commentlari reytingining o'rtacha qiymati bo'yicha
                #Bu yerda Productning comment nomli reletion maydoni yo'q
                #Ammo commentning product nomli Foregnkey maydoni bor
                #Yani __ teskarisiga o'rinli
            #return queryset.order_by(*ordering).reverse()
            if ordering[0].lstrip('-')=='orders':
                queryset=queryset.filter(orderitem__order__complete=True).annotate(orders=Sum('orderitem__quantity'))
                #orderitem foreignkey yordamida productga bog;langani uchun teskarisiga murojaat qilsak bo'ladi
                #querysetni tugallangan orderlar bo'yicah filter qilsak querysetdagi har bir productdan bir nechta qaytaradi
                #qaytgan qeurysetni orderitemlarining quanity maydonlarini yig'ib chiqib yangi orders nomli ustunga bersamiz
                #bunda bir xil obyektlarning quantitylari qo'shiladi
            return queryset.order_by(*ordering)
        else:
            return queryset