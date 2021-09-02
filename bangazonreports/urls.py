from django.urls import path
from .views import expensive_products, inexpensive_products, favorited_sellers_by_customer_list

urlpatterns = [
    path('reports/expensiveproducts', expensive_products),
    path('reports/inexpensiveproducts', inexpensive_products),


    path('reports/favoritesbycustomers', favorited_sellers_by_customer_list),
]