from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Product, Category, ProductImage, Review, Brand
from drf_spectacular.utils import extend_schema
from .permissions import IsSeller
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.exceptions import PermissionDenied
import requests
# ZeroMQ
from zeromq_client import validate_seller

from .serializers import (
    ProductSerializer, CategorySerializer, ReviewSerializer, 
    ProductImageSerializer, BrandSerializer,
)


class ProductListView(generics.ListAPIView):

    permission_classes = [AllowAny]
    queryset = Product.objects.select_related("category", "brand").prefetch_related("images", "reviews")
    serializer_class = ProductSerializer

#-----------------------------------------------------------------------------------

class ProductDetailView(generics.RetrieveAPIView):

    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

#-----------------------------------------------------------------------------------

class SaleProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        products_on_sale = Product.objects.filter(in_sale=True)
        serializer = ProductSerializer(products_on_sale, many=True, context={'request': request})
        return Response(serializer.data)
    
#-----------------------------------------------------------------------------------

# Seller add-update-remove products
class AddProductView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def perform_create(self, serializer):
        user = self.request.user
        
        # Validate seller using ZeroMQ
        validation_response = validate_seller(user.id)
        if not validation_response.get("is_valid"):
            raise PermissionDenied("Invalid seller or not verified.")

        serializer.save(seller=user)

#-----------------------------------------------------------------------------------

class ProductUpdateView(generics.UpdateAPIView):

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSeller]

    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs["pk"], seller=self.request.user)

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)
#-----------------------------------------------------------------------------------

class ProductDeleteView(generics.DestroyAPIView):

    serializer_class = ProductSerializer 
    permission_classes = [IsAuthenticated, IsSeller]
    
    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs["pk"], seller=self.request.user)

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)
#-----------------------------------------------------------------------------------

class AddReviewView(generics.CreateAPIView):

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs['pk']
        product = Product.objects.get(pk=product_id)
        serializer.save(user=self.request.user, product=product)
        product.update_ratings()

#-----------------------------------------------------------------------------------

class AddProductImageView(generics.CreateAPIView):

    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs['pk']
        product = Product.objects.get(pk=product_id)
        serializer.save(product=product)

#-----------------------------------------------------------------------------------

@extend_schema(description="List root categories")
class CategoryListView(generics.ListAPIView):
    
    permission_classes = [AllowAny]
    queryset = Category.objects.filter(parent=None).prefetch_related('children')
    serializer_class = CategorySerializer

#-----------------------------------------------------------------------------------

@extend_schema(description="List Brands")
class BrandListView(generics.ListAPIView):

    permission_classes = [AllowAny]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

#-----additional----------------------------------------------------------------------

class ProductListCreateView(generics.ListCreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


#-----------------------------------------------------------------------------------
@extend_schema_view(
    get=extend_schema(description="Retrieve a product by its ID"),
    put=extend_schema(description="Update a product (sellers only)"),
    delete=extend_schema(description="Delete a product (sellers only)")
)
class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated, IsSeller]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        if self.request.user.is_seller:
            return self.queryset.filter(seller=self.request.user)
        else:
            return self.queryset

#------------------------------------------------------------------------------------