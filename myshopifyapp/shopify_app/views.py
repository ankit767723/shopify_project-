from django.shortcuts import redirect, render, HttpResponse
from django.conf import settings
import shopify
import hashlib
import hmac
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'shopify_app/index.html')


def authenticate(request):
    shop_url = request.GET.get('shop')
    
    # Set up the Shopify API session with the specified version
    shopify.Session.setup(api_key=settings.SHOPIFY_API_KEY, secret=settings.SHOPIFY_API_SECRET)
    session = shopify.Session(shop_url, settings.SHOPIFY_API_VERSION)
    
    # Define the redirect URI
    redirect_uri = 'http://localhost:8000/shopify_authenticate/'
    
    # Create the permission URL
    permission_url = session.create_permission_url(['read_products', 'write_products'], redirect_uri=redirect_uri)
    return redirect(permission_url)

def shopify_authenticate(request):
    logger.debug(f"Request GET parameters: {request.GET}")
    
    required_params = ['shop', 'hmac', 'code']
    for param in required_params:
        if param not in request.GET:
            logger.error(f"Missing required parameter: {param}")
            return HttpResponse(f"Missing required parameter: {param}", status=400)
    
    params = request.GET.dict()
    hmac_received = params.pop('hmac')
    sorted_params = '&'.join(f'{key}={value}' for key, value in sorted(params.items()))
    
    calculated_hmac = hmac.new(
        settings.SHOPIFY_API_SECRET.encode('utf-8'),
        sorted_params.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(calculated_hmac, hmac_received):
        logger.error("Invalid HMAC: Possibly malicious login")
        return HttpResponse("Invalid HMAC: Possibly malicious login", status=403)

    shop_url = request.GET.get('shop')
    shopify.Session.setup(api_key=settings.SHOPIFY_API_KEY, secret=settings.SHOPIFY_API_SECRET)
    session = shopify.Session(shop_url, settings.SHOPIFY_API_VERSION)
    access_token = session.request_token(request.GET)

    # Store the access token in your database, associated with the shop_url
    # Here we're just rendering it for simplicity
    return render(request, 'shopify_authenticate.html', {'access_token': access_token})

def dashboard(request):
    return render(request, 'shopify_app/dashboard.html')



