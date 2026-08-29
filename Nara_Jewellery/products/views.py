from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product, Category, VisitRequest
from .gold_rate import get_gold_rate 
from django.core.paginator import Paginator         # ← add this import


# def home(request):
#     featured_products = Product.objects.filter(stock_quantity__gt=0)[:8]
#     categories        = Category.objects.all()
#     gold_data         = get_gold_rate()        # ← fetch gold rate
#     return render(request, 'products/home.html', {
#         'featured_products': featured_products,
#         'categories':        categories,
#         'gold_data':         gold_data,        # ← pass to template
#     })



def home(request):
    """
    Home page view.
    Fetches:
    - Featured products (top 8)
    - All categories for homepage display
    - Live gold rates
    - Static content for sections (how it works, features, testimonials, etc.)
    """
    featured_products = Product.objects.filter(stock_quantity__gt=0)[:8]
    categories        = Category.objects.all()
    gold_data         = get_gold_rate()

    # ── How It Works Steps ──
    # Shown in a 4-column grid below the hero
    how_it_works = [
        {
            'icon':  '🔍',
            'title': 'Browse Online',
            'desc':  'Explore our curated collection of certified gold jewellery from the comfort of your home.',
        },
        {
            'icon':  '💛',
            'title': 'Save Favourites',
            'desc':  'Add pieces you love to your wishlist. Share it with us when you request a visit.',
        },
        {
            'icon':  '📞',
            'title': 'Request Preview',
            'desc':  'Contact us via WhatsApp or call to schedule a time. We visit at YOUR convenience.',
        },
        {
            'icon':  '🏠',
            'title': 'We Visit You',
            'desc':  'Our expert arrives with the actual jewellery. You see, touch, and decide. No pressure.',
        },
    ]

    # ── Why Choose Nara Features ──
    # 6 trust pillars shown in cards
    why_choose_us = [
        {
            'icon':  '🏅',
            'title': 'BIS Hallmarked',
            'desc':  'Government of India guarantee. Every piece is certified pure — 24K, 22K, or 18K.',
        },
        {
            'icon':  '🏠',
            'title': 'Home Visit Service',
            'desc':  'We come to you. Zero hassle. Zero store visits. Our expert brings jewellery to your door.',
        },
        {
            'icon':  '🔒',
            'title': 'No Online Fraud',
            'desc':  'We NEVER process payments online. Every transaction happens in person — completely secure.',
        },
        {
            'icon':  '✅',
            'title': 'No Pressure Buying',
            'desc':  'You see the jewellery in real life. If you love it, great. If not, no problem at all.',
        },
        {
            'icon':  '📜',
            'title': 'Verified & Certified',
            'desc':  'All jewellery comes with authenticity certificates. Transparent. No hidden charges.',
        },
        {
            'icon':  '💰',
            'title': 'Live Market Pricing',
            'desc':  'Prices linked to live gold rates. Fair. No inflated MRP. Exactly what gold costs today.',
        },
    ]

    # ── Customer Testimonials ──
    testimonials = [
        {
            'text': 'I was nervous buying gold online, but Nara never asked for online payment. The expert visited my home with beautiful necklaces and the whole experience felt so personal and trustworthy.',
            'name': 'Priya Sharma',
            'city': 'Marathahalli, Bangalore',
        },
        {
            'text': 'Bought a wedding ring for my wife. The home visit was so convenient. The jewellery was exactly as shown, BIS hallmarked, and the price was completely fair.',
            'name': 'Sree Chowdary',
            'city': 'Whitefield, Bangalore',
        },
        {
            'text': 'Nara\'s service is unlike anything I\'ve experienced. They came home, showed me multiple designs, gave me all the time I needed, and there was absolutely zero pressure to buy.',
            'name': 'Sneha Reddy',
            'city': 'Koramangala, Bangalore',
        },
            {
        'text': 'My mother wanted gold bangles for my sister\'s wedding. Nara visited our home in Jayanagar with 10 different designs. Beautiful collection, certified pure gold.',
        'name': 'Karthik Rao',
        'city': 'Jayanagar, Bangalore',
    },
    {
        'text': 'Excellent service. They came to HSR Layout within 2 hours of my WhatsApp message. The jewellery quality is outstanding and price was exactly as shown on website.',
        'name': 'Divya Menon',
        'city': 'HSR Layout, Bangalore',
    },
    {
        'text': 'Bought a gold necklace for my wife\'s birthday. The home visit made it so special. Staff was very professional and patient. Will definitely buy again from Nara.',
        'name': 'Suresh Kumar',
        'city': 'Indiranagar, Bangalore',
    },
    ]

    # ── Trust Stats (shown in hero) ──
    trust_stats = [
        ('Happy Clients', '500+'),
        ('Home Visits', '1200+'),
        ('Cities Served', '8'),
        ('Years Trusted', '5+'),
    ]

    # ── Gold Rate Cards (if gold data available) ──
    gold_cards = []
    if gold_data:
        gold_cards = [
            {'label': '24K / gram', 'value': gold_data['rate_per_gram_24k'], 'id': 'home-rate-24k'},
            {'label': '22K / gram', 'value': gold_data['rate_per_gram_22k'], 'id': 'home-rate-22k'},
            {'label': '18K / gram', 'value': gold_data['rate_per_gram_18k'], 'id': 'home-rate-18k'},
            {'label': '10g / 24K',  'value': gold_data['rate_per_10gram_24k'], 'id': 'home-rate-10g'},
        ]

    return render(request, 'products/home.html', {
        'featured_products': featured_products,
        'categories':        categories,
        'gold_data':         gold_data,
        'how_it_works':      how_it_works,
        'why_choose_us':     why_choose_us,
        'testimonials':      testimonials,
        'trust_stats':       trust_stats,
        'gold_cards':        gold_cards,
        })


def product_list(request):
    all_products = Product.objects.filter(stock_quantity__gt=0)
    categories   = Category.objects.all()

    category_id = request.GET.get('category')
    if category_id:
        all_products = all_products.filter(category__id=category_id)

    query = request.GET.get('q', '').strip()
    if query:
        all_products = all_products.filter(
            product_name__icontains=query
        ) | all_products.filter(
            description__icontains=query)

    sort = request.GET.get('sort', 'newest')
    sort_options = {
        'newest':     '-created_at',
        'price_low':  'price',
        'price_high': '-price',
        'name':       'product_name',
    }
    all_products = all_products.order_by(
        sort_options.get(sort, '-created_at')
    )

    # Pagination — show 12 products per page
    paginator = Paginator(all_products, 12)
    page_num  = request.GET.get('page', 1)
    products  = paginator.get_page(page_num)

    return render(request, 'products/product_list.html', {
        'products':     products,
        'categories':   categories,
        'query':        query,
        'selected_cat': category_id,
        'sort':         sort,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(pk=pk)[:4]
    gold_data = get_gold_rate()               # ← fetch gold rate

    return render(request, 'products/product_detail.html', {
        'product':          product,
        'related_products': related_products,
        'gold_data':        gold_data,        # ← pass to template
    })



def request_visit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        VisitRequest.objects.create(
            product        = product,
            user           = request.user if request.user.is_authenticated else None,
            name           = request.POST.get('name', ''),
            phone          = request.POST.get('phone', ''),
            address        = request.POST.get('address', ''),
            preferred_date = request.POST.get('preferred_date') or None,
            preferred_time = request.POST.get('preferred_time', ''),
            message        = request.POST.get('message', ''),
        )
        return render(request, 'products/product_detail.html', {
            'product':          product,
            'related_products': Product.objects.filter(
                                  category=product.category
                                ).exclude(pk=pk)[:4],
            'gold_data':        get_gold_rate(),
            'request_sent':     True,
        })

        return redirect('products:product_detail', pk=pk)


def live_gold_rate(request):
    """AJAX endpoint — returns fresh gold rate as JSON."""
    gold_data = get_gold_rate()
    return JsonResponse(gold_data)

def error_404(request, exception):
    return render(request, '404.html', status=404)