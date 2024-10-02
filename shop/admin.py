from django.contrib import admin
from .models import Contact, SocialLink, ProductPage, ContactTicket, News, Banner, Service, Advantage, SingleBanner, BatteryCard, BatteryInfo, Category, Product, ProductImage, Brand, Cart, BannerShop, Order, OrderItem, ProductItem


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Количество дополнительных пустых форм для добавления

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('contact_type', 'value')
    list_filter = ('contact_type',)
    search_fields = ('value',)

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name',)

class BatteryInfoInline(admin.TabularInline):
    model = BatteryInfo
    extra = 1  # Количество пустых форм для добавления


@admin.register(ProductPage)
class ProductPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [BatteryInfoInline]


@admin.register(ContactTicket)
class ContactTicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}  # Автозаполнение slug на основе заголовка
    search_fields = ('title', 'content')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'is_active')  # Отображаем ссылку в админке
    list_filter = ('is_active',)
    search_fields = ('title',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # Поля, которые будут отображаться в списке

@admin.register(Advantage)
class AdvantageAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle')  # Поля, которые будут отображаться в списке


@admin.register(SingleBanner)
class SingleBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    search_fields = ('title',)
    ordering = ('order',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo')


@admin.register(BatteryCard)
class BatteryCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'order')
    list_editable = ('order',)
    search_fields = ('title',)
    ordering = ('order',)


@admin.register(BatteryInfo)
class BatteryInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_page', 'product_code')
    list_filter = ('product_page',)
    search_fields = ('title', 'product_code')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'parent')  # Используем строки
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'discount_price', 'stock', 'available')  # Используем строки
    list_filter = ('category', 'brand', 'available')
    search_fields = ('name', 'description', 'sku')
    inlines = [ProductImageInline]

@admin.register(BannerShop)
class BannerShopAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'full_name', 'email', 'phone', 'payment_method', 'delivery_method', 'created_at']
    list_filter = ['created_at', 'payment_method', 'delivery_method']
    search_fields = ['full_name', 'email', 'phone']

@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'button_text', 'button_link')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)


admin.site.register(Cart)
