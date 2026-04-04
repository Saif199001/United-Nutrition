from django.shortcuts import render
from .models import Product, Category
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer, CategorySerializer

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