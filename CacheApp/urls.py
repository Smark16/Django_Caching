from django.urls import path
from .views import *

urlpatterns = [
    path('receipe', ListReceipe.as_view()),
    path('filter', FilteredReceipe.as_view()),
    path('sales', SalesList.as_view()),
    path('post_order', PostOrder.as_view())
]