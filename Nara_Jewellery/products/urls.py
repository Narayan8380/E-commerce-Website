from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('',                    views.home,           name='home'),
    path('shop/',               views.product_list,   name='product_list'),
    path('product/<int:pk>/',   views.product_detail, name='product_detail'),
    path('product/<int:pk>/visit/',  views.request_visit,  name='request_visit'),
    path('gold-rate/',         views.live_gold_rate, name='gold_rate'),
]