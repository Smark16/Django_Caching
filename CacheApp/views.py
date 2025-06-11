from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.utils import timezone
from django.db.models import Q # create complex queries with logical operators like OR, AND, NOT
from django.db.models import F # used to compare two fields in a query
from django.db.models.functions import Upper, Length
from django.db.models import Count, Avg, Min, Max, Sum, When, Case, Value
from django.db import transaction
from functools import partial
import itertools
# Create your views here.
class ListReceipe(generics.ListAPIView):
    queryset = Receipe.objects.select_related('category').all()
    serializer_class = ReceipeSerializer
    
    @method_decorator(cache_page(60 * 60 * 2, key_prefix='recepe_list')) # cache for 2 hours
    def dispatch(self, *args, **kwargs): # works well for static data
        return super().dispatch(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()
    
# Filter based on category
class FilteredReceipe(generics.ListAPIView):

    # using Q Objects
    
    # using OR operator
    #  queryset = Receipe.objects.select_related('category').filter(
    #      Q(category=2) | Q(category=3))
    #  serializer_class = ReceipeSerializer

    # using NOT operator
    # queryset = Receipe.objects.select_related('category').filter(~Q(added_at__gt=timezone.now() - timezone.timedelta(days=40))) # not added in last 2 days
    # serializer_class = ReceipeSerializer


    # using LIKE operator (field_name__icontains='r', field_name__endswith='h')
    # queryset = Receipe.objects.select_related('category').filter(name__endswith='o')
    # serializer_class = ReceipeSerializer
    
    # using greater than
    # queryset = Receipe.objects.select_related('category').filter(added_at__gt=timezone.now() - timezone.timedelta(days=2)) #added in the last two days
    # serializer_class = ReceipeSerializer

    # using regex
    # queryset = Receipe.objects.select_related('category').filter(Q(category__name__regex=r'[0-9]+')) # check if category name contains a number or more
    # serializer_class = ReceipeSerializer

    # using values
    # queryset = Receipe.objects.select_related('category').all().first()
    # serializer_class = ReceipeSerializer

    #  To return first object use get
    # def get(self, request, *args, **kwargs):
    #     first_recipe = Receipe.objects.select_related('category').first()
    #     if not first_recipe:
    #         return Response(status=404)
    #     serializer = self.get_serializer(first_recipe)
    #     return Response(serializer.data)
    

    # get enables you work with objects or strings instead of querysets
    # def get(self, request, *args, **kwargs):
    #   receipe = Receipe.objects.select_related('category').values_list(Upper('name'), flat=True)
    #   return Response({'receipe': receipe})

    # def get(self, request, *args, **kwargs):
    #   receipe = Receipe.objects.select_related('category').filter(name__startswith='m').count()
    #   return Response({'receipe': receipe})

    # using Count
    # serializer_class = ReceipeSerializer
    # def get(self, request, *args, **kwargs):
    #   one_month_ago = timezone.now()  - timezone.timedelta(days=31)
    #   receipe = Receipe.objects.select_related('category').filter(added_at__gte=one_month_ago).aggregate(Count('id'))
    #   return Response({'receipe': receipe})

    # using annotate function ==> Adds additional information on the queryset

    # def get_queryset(self):
    #  return Receipe.objects.select_related('category').annotate(len_name=Length('name'))
    
    # serializer_class = ReceipeSerializer
    # def get(self, request, *args, **kwargs):
    #     leng_count = Receipe.objects.select_related('category').annotate(len_name=Length('name')).values('sales__profit', 'len_name')
    #     return Response(leng_count) 

    # using when and case
    # queryset = Receipe.objects.select_related('category').annotate(receipe_profit=Case(
    #     When(sales__profit__gte=50000, then=True),
    #     default=False
    # )).filter(receipe_profit=True)
    # serializer_class = ReceipeSerializer

    # getting last dates
    serializer_class = ReceipeSerializer
    queryset = Receipe.objects.select_related('category').all()

    def get(self, request, *args, **kwargs):
        # Single query to get both dates
        dates = Receipe.objects.aggregate(
            last_added=Max('added_at'),
            first_added=Min('added_at')
        )
        
        first_added = dates['first_added']
        last_added = dates['last_added']
        
        if not first_added or not last_added:
            return Response([])

        # Generate 10-day intervals
        dates = []
        count = itertools.count()
        
        while (dt := first_added + timezone.timedelta(days=10*next(count))) <= last_added:
            dates.append(dt)
            
        return Response(dates)


class SalesList(generics.ListAPIView):

    # using greater than
    # queryset = Sales.objects.filter(profit__gt = F('expenditure'))
    # serializer_class = SalesSerializer

    # using AVG
    # serializer_class = SalesSerializer

    # def get(self, request, *args, **kwargs):
    #     sales = Sales.objects.aggregate(
    #         avg=Avg('profit'),
    #         sum = Sum('profit'),
    #         min = Min('profit'),
    #         max = Max('profit'),
    #         count = Count('id')
    #         )
    #     return Response(sales)

    # serializer_class = SalesSerializer

    # def get(self, request, *args, **kwargs):
    #     leng_count = Sales.objects.annotate(total_profits=Sum('profit')).values('receipe__name', 'total_profits')
    #     return Response(leng_count) 

    # using when and Case
    serializer_class = SalesSerializer
    queryset = Sales.objects.annotate(better_profit=Case(
        When(profit__gte=50000, then=Value('high_profit')),
        default=Value('no_profit')
    )).filter(better_profit='high_profit')


def email_user(email):
    print(f'Dear {email} your order has been successfull')

# How to implement Transactions
class PostOrder(generics.CreateAPIView):
    serializer_class = OrderSerializer
    order = Order.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        
        if serializer.is_valid():
            try:
                with transaction.atomic():

                    product = serializer.validated_data['product']
                    number_of_items = serializer.validated_data['number_of_items']

                    if product.number_in_stock < number_of_items:
                        return Response({'msg': 'Item is out of stock'})
                    
                    order = serializer.save()
                    product.number_in_stock -= order.number_of_items
                    product.save()
                
                    transaction.on_commit(partial(email_user, 'sengendomark16@gmail.com'))
                return Response(serializer.data)

            except Exception as e:
                return Response({'msg': str(e)})





    

    