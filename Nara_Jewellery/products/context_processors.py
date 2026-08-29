from .models import Category

def nav_categories(request):
    """
    This function runs on every request.
    It adds 'nav_categories' to every template automatically.
    So we don't need to pass it manually from each view.
    """
    return {
        'nav_categories': Category.objects.all()
    }