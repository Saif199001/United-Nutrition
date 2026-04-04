from django.contrib import admin
from .models import User, Category, Product, Cart, CartItem, Order, OrderItem


# ================= USER =================
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone', 'is_staff']
    search_fields = ['username', 'email']


# ================= CATEGORY =================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active']
    search_fields = ['name']


# ================= PRODUCT =================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_price', 'stock', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'is_available']


# ================= CART ITEM INLINE =================
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


# ================= CART =================
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    inlines = [CartItemInline]


# ================= ORDER ITEM INLINE =================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# ================= ORDER =================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'status', 'created_at']
    list_filter = ['status']
    inlines = [OrderItemInline]
