from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, News, ContactTicket, Banner, Service, ProductPage, Advantage, SingleBanner, BatteryCard, BatteryInfo, Cart, CartItem, Order, OrderItem, BannerShop, Category, ProductItem
from django.contrib import messages
from .forms import ContactForm, SearchForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .forms import OrderForm, SearchForm


def get_cart(request):
    """Get or create a cart for the current session."""
    session_key = request.session.session_key
    if not session_key:
        request.session.save()  # Сохраните сессию, чтобы создать session_key
    cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def main_page(request):
    banners = Banner.objects.filter(is_active=True)  # Получаем только активные баннеры
    services = Service.objects.all()  # Получаем все услуги из базы данных
    advantages = Advantage.objects.all()  # Получаем все преимущества из базы данных
    single_banners = SingleBanner.objects.all()  # Получаем одиночные баннеры
    battery_cards = BatteryCard.objects.all()

    context = {
        'current_page': 'main',
        'banners': banners,  # Передаем только баннеры, так как остальное доступно через контекстный процессор
        'services': services,  # Передаем услуги в шаблон
        'advantages': advantages,  # Передаем преимущества в шаблон
        'single_banners': single_banners,  # Передаем одиночные баннеры в шаблон
        'single_banner_1': single_banners[0] if len(single_banners) > 0 else None,
        'single_banner_2': single_banners[1] if len(single_banners) > 1 else None,
        'single_banner_3': single_banners[2] if len(single_banners) > 2 else None,
        'single_banner_4': single_banners[3] if len(single_banners) > 3 else None,
        'battery_cards': battery_cards,
    }

    return render(request, 'shop/main_page.html', context)

def shop_page(request):
    banners = BannerShop.objects.filter(is_active=True).order_by('order')  # Fetch active banners
    products = Product.objects.filter(available=True)  # Example of fetching available products
    categories = Category.objects.all()  # Fetch all categories
    categorized_products = {category: Product.objects.filter(category=category) for category in categories}

    context = {
        'current_page': 'shop',  # Pass the current page
        'banners': banners,  # Pass the banners to the template
        'products': products,  # Pass the products to the template
        'categories': categories,  # Pass categories to the context
        'categorized_products': categorized_products,
    }
    return render(request, 'shop/shop_page.html', context)

def produktsiya_page(request, slug):
    product_page = get_object_or_404(ProductPage, slug=slug)
    return render(request, 'shop/produktsiya.html', {'product_page': product_page})

def product_page(request, slug):
    # Получаем страницу продукта по slug
    page = get_object_or_404(ProductPage, slug=slug)
    
    # Получаем информацию о батареях, связанных с этой страницей продукта
    batteries = BatteryInfo.objects.filter(product_page=page)

    # Передаем данные в шаблон
    context = {
        'page': page,
        'batteries': batteries,
    }
    
    return render(request, 'shop/product_page.html', context)

def contact_page(request):
    # Обработка формы
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем тикет в базу данных
            messages.success(request, 'Ваше сообщение было отправлено.')
            return redirect('contact')  # Перенаправляем пользователя обратно на страницу контактов
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'shop/contact.html', context)

def news_list(request):
    news_items = News.objects.all().order_by('-created_at')  # Список новостей
    return render(request, 'shop/news_list.html', {'news_items': news_items})

def news_detail(request, slug):
    news_item = get_object_or_404(News, slug=slug)  # Полная статья новости
    return render(request, 'shop/news_detail.html', {'news_item': news_item})

def map_page(request):
    return render(request, 'shop/map.html')  # Контакты теперь передаются через контекстный процессор


def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(name__icontains=query) | Q(name__icontains=query.lower())) if query else Product.objects.all()

    paginator = Paginator(products, 10)  # Пагинация
    page_number = request.GET.get('page')
    results = paginator.get_page(page_number)

    form = SearchForm(initial={'query': query})  # Создаем форму поиска

    return render(request, 'shop/search_results.html', {'form': form, 'results': results, 'query': query})


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)  # Get products of the selected category

    # Pagination for products
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    products_page = paginator.get_page(page_number)

    return render(request, 'shop/category_products.html', {
        'category': category,
        'products': products_page,
    })

def product_detail(request, pk):
    # Получаем продукт по его первичному ключу (pk)
    product = get_object_or_404(Product, pk=pk)
    
    # Контекст для шаблона
    context = {
        'product': product,
        'images': product.images.all()  # Получаем все изображения для продукта
    }
    
    return render(request, 'shop/product_detail.html', context)

def add_to_cart(request, product_id):
    cart = get_cart(request)  # Получите или создайте корзину
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key  # Получите session_key
    
    # Проверьте, есть ли уже товар в корзине
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{product.name} успешно добавлен в корзину.")
    return redirect('cart_detail')


def remove_from_cart(request, product_id):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
    return redirect('cart_detail')

def update_cart(request):
    if request.method == 'POST':
        cart = get_object_or_404(Cart, session_key=request.session.session_key)

        if 'product_id' in request.POST:
            # Handle quantity changes
            product_id = request.POST.get('product_id')
            action = request.POST.get('action')
            cart_item = get_object_or_404(cart.items, product_id=product_id)

            if action == 'add':
                if cart_item.quantity < cart_item.product.stock:
                    cart_item.quantity += 1
                    cart_item.save()
            elif action == 'remove':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
        elif 'delivery_method' in request.POST:
            # Handle delivery method change
            delivery_method = request.POST.get('delivery_method')
            cart.delivery_method = delivery_method
            cart.save()

        # Update cart totals
        cart.update_totals()

        # Prepare updated data
        response_data = {
            'quantity': cart_item.quantity if 'product_id' in request.POST else None,
            'total_price': cart_item.get_total_price() if 'product_id' in request.POST else None,
            'total_cost': cart.get_total_price(),
            'total_discount': cart.get_total_discount(),
            'shipping_cost': cart.get_shipping_cost(),
            'final_total': cart.get_final_total(),
        }
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def order_success(request):
    return render(request, 'shop/order_success.html')

def cart_detail(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.save()  # Создает session_key, если его нет
    cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    context = {
        'cart_items': cart.items.all(),
        'total_price': cart.get_total_price(),
        'total_discount': cart.get_total_discount(),
        'shipping_cost': cart.get_shipping_cost(),
        'final_total': cart.get_final_total(),
    }
    return render(request, 'shop/cart_detail.html', context)

def checkout(request):
    cart = get_cart(request)  # Функция получения корзины
    cart_items = cart.items.all()  # Товары в корзине

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            # Очищаем корзину после оформления заказа
            cart.items.all().delete()
            return redirect('order_success')  # Перенаправляем на страницу успешного оформления заказа
    else:
        form = OrderForm()

    return render(request, 'shop/checkout.html', {'form': form, 'cart_items': cart_items, 'total_price': cart.get_total_price()})


def order_success(request):
    return render(request, 'shop/order_success.html')


def banners_view(request):
    banners = BannerShop.objects.filter(is_active=True).order_by('order')
    return render(request, 'shop/banners_slider.html', {'banners': banners})

def get_wishlist(request):
    wishlist = request.session.get('wishlist', [])
    return wishlist

def remove_from_wishlist(request, product_id):
    wishlist = get_wishlist(request)
    if product_id in wishlist:
        wishlist.remove(product_id)
        request.session['wishlist'] = wishlist
        messages.success(request, 'Товар удален из избранного.')
    else:
        messages.info(request, 'Товар не в избранном.')
    return redirect('wishlist')


def add_to_wishlist(request, product_id):
    wishlist = get_wishlist(request)
    if product_id not in wishlist:
        wishlist.append(product_id)
        request.session['wishlist'] = wishlist
        messages.success(request, 'Товар добавлен в избранное.')
    else:
        messages.info(request, 'Товар уже в избранном.')
    return redirect('product_detail', pk=product_id)


def wishlist_view(request):
    wishlist = get_wishlist(request)
    products = Product.objects.filter(id__in=wishlist)
    return render(request, 'shop/wishlist.html', {'products': products})


def category_products(request, category_id):
    # Get the selected category
    category = get_object_or_404(Category, id=category_id)
    
    # Get all products for the selected category
    products = Product.objects.filter(category=category)

    # Context to pass to the template
    context = {
        'category': category,
        'products': products,
    }

    return render(request, 'shop/category_products.html', context)


def produktsiya_page(request):
    products = ProductItem.objects.all()
    return render(request, 'shop/products.html', {'products': products})