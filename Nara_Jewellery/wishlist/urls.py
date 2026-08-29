from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('',                        views.wishlist_page,   name='wishlist_page'),
    path('toggle/<int:pk>/',        views.toggle_wishlist, name='toggle'),
    path('count/',                  views.wishlist_count,  name='count'),
]