from django.db import models
from django.urls import reverse
from decimal import Decimal
from django.utils.translation import gettext_lazy as _  # Ensure this is imported
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя товара")
    description = models.TextField(verbose_name="Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена товара")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Цена скидки товара")
    stock = models.PositiveIntegerField(verbose_name="Количество (шт)")
    available = models.BooleanField(default=True, verbose_name="В наличии")
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True, related_name='products', verbose_name="Бренд товара")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='products', verbose_name="Категория товара")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано в")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class Cart(models.Model):  # Ensure Cart inherits from models.Model
    session_key = models.CharField(max_length=40, unique=True, verbose_name=_("Ключ сессии"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    def get_total_price(self):
        total = sum(item.get_total_price() for item in self.items.all())
        return total

    def get_total_quantity(self):
        total_quantity = sum(item.quantity for item in self.items.all())
        return total_quantity
    
    def get_total_discount(self):
        # Assuming each product has a discount field, calculate the total discount
        total_discount = sum((item.product.price - item.product.discount_price) * item.quantity for item in self.items.all() if item.product.discount_price)
        return total_discount
    
    delivery_method = models.CharField(max_length=20, choices=[
        ('courier', 'Доставка курьером'),
        ('pickup', 'Самовывоз')
    ], default='courier', verbose_name="Способ доставки")
    
    def get_shipping_cost(self):
        if self.delivery_method == 'pickup':
            return 0  # Free shipping for pickup
        return 500 if self.items.count() > 0 else 0  # Shipping cost for courier delivery
    
    def get_final_total(self):
        return self.get_total_price() - self.get_total_discount() + self.get_shipping_cost()
    
    def update_totals(self):
        self.total_price = sum(item.get_total_price() for item in self.items.all())
        self.total_discount = self.get_total_discount()
        self.shipping_cost = self.get_shipping_cost()
        self.final_total = self.get_final_total()
        self.save()
    
    def __str__(self):
        return f"Корзина {self.session_key}"
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, verbose_name=_("Корзина"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Товар"))
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name=_("Количество"))

    def get_total_price(self):
        if self.product.discount_price:
            return self.product.discount_price * self.quantity
        return self.product.price * self.quantity
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cart.update_totals()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Order(models.Model):
    DELIVERY_METHOD_CHOICES = (
        ('pickup', 'Самовывоз'),
        ('delivery', 'Доставка'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Наличные'),
        ('card', 'Карта'),
    )

    full_name = models.CharField(max_length=100, verbose_name="Полное имя")
    email = models.EmailField(verbose_name="Электронная почта")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=255, verbose_name="Адрес", default="Не указан")
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, verbose_name="Метод оплаты")
    delivery_method = models.CharField(max_length=50, choices=DELIVERY_METHOD_CHOICES, verbose_name="Метод доставки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"Заказ {self.id} от {self.full_name}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    class Meta:
        verbose_name = 'Детали заказа'
        verbose_name_plural = 'Детали заказов'
    

    

class Contact(models.Model):
    CONTACT_TYPES = (
        ('phone', 'Телефон'),
        ('address', 'Адрес'),
        ('email', 'Email'),
    )
    
    contact_type = models.CharField(max_length=10, choices=CONTACT_TYPES, verbose_name='Тип контакта')
    value = models.CharField(max_length=255, verbose_name='Контактные данные')
    icon_class = models.CharField(max_length=50, blank=True, verbose_name='Класс иконки (для Bootstrap Icons)')

    def __str__(self):
        return f"{self.get_contact_type_display()}: {self.value}"

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class SocialLink(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название социальной сети')
    url = models.URLField(verbose_name='Ссылка на социальную сеть')
    icon_image = models.ImageField(upload_to='social_icons/', verbose_name='Иконка социальной сети')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальные сети'

class ProductPage(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название страницы')  # Название страницы
    slug = models.SlugField(unique=True, verbose_name='Slug (часть URL)')  # URL slug
    content = models.TextField(blank=True, verbose_name='Содержание страницы')  # Содержание страницы

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_page', args=[self.slug])

    class Meta:
        verbose_name = 'Страница продукции'
        verbose_name_plural = 'Страницы продукции'


class ContactTicket(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Электронная почта')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Тикет от {self.name} ({self.email})"

    class Meta:
        verbose_name = 'Тикет'
        verbose_name_plural = 'Тикеты'

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='Slug (часть URL)')
    image = models.ImageField(upload_to='news_images/', verbose_name='Изображение')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class Banner(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True, null=True)  # Поле для ссылки
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title if self.title else "Banner"

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"

class Service(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание услуги")
    icon = models.ImageField(upload_to='services/icons/', verbose_name="Иконка")
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class Advantage(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    subtitle = models.TextField(verbose_name="Подзаголовок")
    icon = models.FileField(upload_to='advantages/icons/', verbose_name="Иконка")  # Используем FileField вместо ImageField

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"

class SingleBanner(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок баннера", blank=True, null=True)
    description = models.TextField(verbose_name="Описание баннера", blank=True, null=True)
    image = models.ImageField(upload_to='banners/single/', verbose_name="Изображение баннера")
    link = models.URLField(max_length=255, verbose_name="Ссылка", blank=True, null=True)
    order = models.PositiveIntegerField(verbose_name="Порядок", default=0, help_text="Порядок отображения баннеров")

    class Meta:
        verbose_name = "Одиночный баннер"
        verbose_name_plural = "Одиночные баннеры"
        ordering = ['order']

    def __str__(self):
        return self.title if self.title else "Без названия"
    

class BatteryCard(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    link = models.URLField(verbose_name="Ссылка", blank=True, null=True)
    image = models.ImageField(upload_to='batteries/', verbose_name="Изображение")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']  # Сортировка по полю 'order'
        verbose_name = "Карточка аккумулятора"
        verbose_name_plural = "Карточки аккумуляторов"

class BatteryInfo(models.Model):
    product_page = models.ForeignKey(ProductPage, related_name='batteries', on_delete=models.CASCADE, verbose_name="Страница продукта")
    title = models.CharField(max_length=100, verbose_name="Название аккумулятора",)
    product_code = models.CharField(max_length=50, verbose_name="Код изделия", blank=True, null=True)
    box_code = models.CharField(max_length=50, verbose_name="Код коробки", blank=True, null=True)
    power = models.CharField(max_length=50, verbose_name="Мощность", blank=True, null=True)
    capacity = models.CharField(max_length=50, verbose_name="Значение A (EN)", blank=True, null=True)
    polarity = models.CharField(max_length=50, verbose_name="Полюсное направление", blank=True, null=True)
    terminal_type = models.CharField(max_length=50, verbose_name="Тип полюса", blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Общий вес (кг)", blank=True, null=True)
    width = models.PositiveIntegerField(verbose_name="Ширина (мм)", blank=True, null=True)
    length = models.PositiveIntegerField(verbose_name="Длина (мм)", blank=True, null=True)
    height = models.CharField(max_length=50, verbose_name="Высота с клеммой (мм)", blank=True, null=True)
    image = models.ImageField(upload_to='battery_images/', verbose_name="Изображение аккумулятора", blank=True, null=True)
    
    # Новые поля
    nominal_capacity = models.CharField(max_length=50, verbose_name="Номинальная емкость", blank=True, null=True)
    cold_cranking_amperage = models.CharField(max_length=50, verbose_name="Ток холодной прокрутки", blank=True, null=True)
    warranty = models.CharField(max_length=50, verbose_name="Гарантия", blank=True, null=True)
    polarity_type = models.CharField(max_length=50, verbose_name="Полярность", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Информация об аккумуляторе"
        verbose_name_plural = "Информация об аккумуляторах"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Информация об аккумуляторе"
        verbose_name_plural = "Информация об аккумуляторах"

class Brand(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)  # Добавьте поле, если его нет

    def __str__(self):
        return self.name


# Модель для категорий
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название категории")
    description = models.TextField(blank=True, null=True, verbose_name="Описание категорий")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategories', blank=True, null=True, verbose_name="Родительская категория")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Изображение для {self.product.name}"
    
    class Meta:
        verbose_name = "Изображение товар"
        verbose_name_plural = "Изображение товаров"

class BannerShop(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок", blank=True, null=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    image = models.ImageField(upload_to='banners_shop/', verbose_name="Изображение баннера")
    link = models.URLField(max_length=255, verbose_name="Ссылка", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    order = models.PositiveIntegerField(verbose_name="Порядок", default=0, help_text="Порядок отображения баннеров")

    class Meta:
        verbose_name = "Баннер магазина"
        verbose_name_plural = "Баннеры магазина"
        ordering = ['order']

    def __str__(self):
        return self.title if self.title else "Без названия"
    

class ProductItem(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, verbose_name="URL")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение")
    button_text = models.CharField(max_length=50, default="Подробнее", verbose_name="Текст кнопки")
    button_link = models.URLField(blank=True, null=True, verbose_name="Ссылка кнопки")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Продукция (Главная)"
        verbose_name_plural = "Продукция (Главная)"
    
    