from .models import Product, Contact, SocialLink, ProductPage, Category, CartItem, Cart

def categories_processor(request):
    categories = Category.objects.all()
    return {'categories': categories}
def common_data(request):
    # Получаем общие данные из базы данных
    products = Product.objects.all()
    contacts = Contact.objects.all()
    social_links = SocialLink.objects.all()
    product_pages = ProductPage.objects.all()
    categories = Category.objects.all()  # Fetch all categories


    # Возвращаем словарь с данными, которые будут доступны во всех шаблонах
    return {
        'products': products,
        'contacts': contacts,
        'social_links': social_links,
        'product_pages': product_pages,
        'categories': categories  # Pass categories to the context
    }


def categories_processor(request):
    categories = Category.objects.all()
    return {'categories': categories}

def wishlist_and_cart_count(request):
    # Get wishlist count
    wishlist = request.session.get('wishlist', [])
    wishlist_count = len(wishlist)

    # Get cart count
    cart_item_count = 0
    if request.session.session_key:
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
        if cart:
            cart_item_count = CartItem.objects.filter(cart=cart).count()

    return {
        'wishlist_count': wishlist_count,
        'cart_item_count': cart_item_count,
    }