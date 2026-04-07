from django.contrib import admin
from .models import User, Category, Product, Cart, CartItem, Order, OrderItem, Gallery


# ================= USER =================
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone', 'is_staff', 'is_active']
    
    list_filter = ['is_staff', 'is_active']
    
    search_fields = ['username', 'email']


# ================= CATEGORY =================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    
    list_filter = ['is_active']
    
    search_fields = ['name']
    
    prepopulated_fields = {'slug': ('name',)}


# ================= PRODUCT =================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_price', 'stock', 'is_available', 'created_at']
    
    list_filter = ['category', 'is_available', 'created_at']
    
    search_fields = ['name', 'category__name']
    
    prepopulated_fields = {'slug': ('name',)}
    
    list_editable = ['price', 'stock', 'is_available']
    
    readonly_fields = ['created_at', 'updated_at']
    
    ordering = ['-created_at']


# ================= CART ITEM INLINE =================
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


# ================= CART =================
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    
    search_fields = ['user__username']
    
    readonly_fields = ['created_at']
    
    inlines = [CartItemInline]


# ================= ORDER ITEM INLINE =================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'price', 'quantity']


# ================= ORDER =================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_id',
        'user',
        'name',
        'email',
        'total_price',
        'status',
        'created_at'
    ]

    list_filter = ['status', 'created_at']

    search_fields = ['order_id', 'name', 'email', 'phone']

    list_editable = ['status']

    readonly_fields = ['order_id', 'created_at', 'total_price']

    ordering = ['-created_at']

    inlines = [OrderItemInline]


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_active', 'created_at']
    
    list_filter = ['is_active']
    
    search_fields = ['title']
