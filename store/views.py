from django.shortcuts import render
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Gallery
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, OrderSerializer, GallerySerializer
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

# REGISTER
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User created successfully"})

    return Response(serializer.errors)


# Login
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"error": "Invalid credentials"})

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "username": user.username
    })

def home(request):
    categories = Category.objects.filter(is_active=True)

    protein_products = Product.objects.filter(
        category__name__iexact="Proteins",
        is_available=True
    )[:3]

    supplement_products = Product.objects.filter(
        category__name__iexact="Supliments",
        is_available=True
    )[:3]

    vitamin_products = Product.objects.filter(
        category__name__iexact="Vitamins",
        is_available=True
    )[:2]

    return render(request, 'home.html', {
        'categories': categories,
        'protein_products': protein_products,
        'supplement_products': supplement_products,
        'vitamin_products': vitamin_products
    })


def product_list(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.filter(is_active=True)

    # FILTER (category)
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # SORT
    sort = request.GET.get('sort')
    if sort == 'low-high':
        products = products.order_by('price')
    elif sort == 'high-low':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')

    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories
        })

@api_view(['GET'])
def api_products(request):
    products = Product.objects.filter(is_available=True)

    category = request.GET.get('category')
    if category:
        products = products.filter(category__slug=category)

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def api_categories(request):
    categories = Category.objects.filter(is_active=True)
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


# Get Cart
@api_view(['GET'])
def get_cart(request):
    if not request.user.is_authenticated:
        return Response({"error": "Login required"})

    cart, created = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


# Add to cart
@api_view(['POST'])
def add_to_cart(request):
    user = request.user

    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))

    cart, created = Cart.objects.get_or_create(user=user)
    product = Product.objects.get(id=product_id)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity

    item.save()

    return Response({"message": "Added to cart"})


# Remove from cart
@api_view(['POST'])
def remove_from_cart(request):
    user = request.user
    product_id = request.data.get('product_id')

    cart = Cart.objects.get(user=user)
    CartItem.objects.filter(cart=cart, product_id=product_id).delete()

    return Response({"message": "Removed"})


# update quantity
@api_view(['POST'])
def update_cart(request):
    user = request.user

    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity'))

    cart = Cart.objects.get(user=user)
    item = CartItem.objects.get(cart=cart, product_id=product_id)

    item.quantity = quantity
    item.save()

    return Response({"message": "Updated"})

# CHECKOUT (GUEST + USER)
@api_view(['POST'])
def checkout(request):
    user = request.user if request.user.is_authenticated else None

    name = request.data.get('name')
    email = request.data.get('email')
    phone = request.data.get('phone')
    address = request.data.get('address')
    items = request.data.get('items')

    total = 0

    order = Order.objects.create(
        user=user,
        name=name,
        email=email,
        phone=phone,
        address=address,
        total_price=0
    )

    for item in items:
        product = Product.objects.filter(id=item['product_id']).first()
        if not product:
            continue
            
        quantity = item['quantity']

        price = product.get_price()
        total += price * quantity

        OrderItem.objects.create(
            order=order,
            product=product,
            price=price,
            quantity=quantity
        )

    order.total_price = total
    order.save()

    return Response({"message": "Order placed"})    

# ORDER HISTORY
@api_view(['GET'])
def order_history(request):
    if not request.user.is_authenticated:
        return Response({"error": "Login required"})

    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

# Gallery
@api_view(['GET'])
def api_gallery(request):
    images = Gallery.objects.filter(is_active=True)
    serializer = GallerySerializer(images, many=True)
    return Response(serializer.data)