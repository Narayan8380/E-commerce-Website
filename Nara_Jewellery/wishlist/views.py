from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import Product
from .models import Wishlist
# Create your views here.

@login_required
def wishlist_page(request):
    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related('product', 'product__category')

    return render(request, 'wishlist/wishlist.html', {
        'wishlist_items': wishlist_items,
    })


@login_required
@require_POST
def toggle_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        # Already in wishlist → remove it
        wishlist_item.delete()
        in_wishlist = False
    else:
        in_wishlist = True

    # Total wishlist count for navbar badge
    count = Wishlist.objects.filter(user=request.user).count()

    return JsonResponse({
        'in_wishlist': in_wishlist,
        'count':       count,
        'message':     'Added to wishlist' if in_wishlist else 'Removed from wishlist',
    })


@login_required
def wishlist_count(request):
    count = Wishlist.objects.filter(user=request.user).count()
    return JsonResponse({'count': count})