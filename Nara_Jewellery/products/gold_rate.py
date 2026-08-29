import requests
from django.core.cache import cache

CACHE_KEY     = 'live_gold_rate'
CACHE_TIMEOUT = 60 * 30  # cache for 30 minutes


def get_gold_rate():
    """
    Fetch live gold rate in INR per gram (24K).
    Uses metals-api (free tier). Falls back to a static rate if API fails.
    """

    # Return cached rate if available
    cached = cache.get(CACHE_KEY)
    if cached:
        return cached

    try:
        # Free gold rate API (no key needed)
        url      = "https://api.metals.live/v1/spot"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        # Find gold price in USD per troy ounce
        gold_usd_per_oz = None
        for item in data:
            if 'gold' in item:
                gold_usd_per_oz = item['gold']
                break

        if not gold_usd_per_oz:
            raise ValueError("Gold rate not found in response")

        # Convert: 1 troy oz = 31.1035 grams
        # USD to INR (approximate — we'll also fetch live rate)
        usd_to_inr      = get_usd_to_inr()
        gold_inr_per_gram = (gold_usd_per_oz / 31.1035) * usd_to_inr

        result = {
            'rate_per_gram_24k': round(gold_inr_per_gram, 2),
            'rate_per_gram_22k': round(gold_inr_per_gram * 0.9167, 2),
            'rate_per_gram_18k': round(gold_inr_per_gram * 0.75, 2),
            'rate_per_10gram_24k': round(gold_inr_per_gram * 10, 2),
            'usd_per_oz':        round(gold_usd_per_oz, 2),
            'usd_to_inr':        round(usd_to_inr, 2),
            'source':            'live',
        }

        # Cache the result
        cache.set(CACHE_KEY, result, CACHE_TIMEOUT)
        return result

    except Exception as e:
        print(f"Gold rate API error: {e}")
        return get_fallback_rate()


def get_usd_to_inr():
    """Fetch live USD to INR exchange rate."""
    try:
        url      = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=5)
        data     = response.json()
        return data['rates']['INR']
    except Exception:
        return 83.5   # fallback rate


def get_fallback_rate():
    """Static fallback if API is down."""
    return {
        'rate_per_gram_24k':   7200.00,
        'rate_per_gram_22k':   6600.00,
        'rate_per_gram_18k':   5400.00,
        'rate_per_10gram_24k': 72000.00,
        'usd_per_oz':          2300.00,
        'usd_to_inr':          83.50,
        'source':              'fallback',
    }