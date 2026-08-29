from django import template
from wishlist.models import Wishlist

register = template.Library()


@register.filter
def is_in_wishlist(product_id, user):
    if not user or not user.is_authenticated:
        return False
    return Wishlist.objects.filter(
        user=user,
        product_id=product_id
    ).exists()