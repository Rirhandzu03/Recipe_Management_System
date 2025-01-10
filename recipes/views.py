from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.generics import UpdateAPIView, DestroyAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView 
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RecipeSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from .models import Recipe
from django.db.models import Q



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer  
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'category', 'ingredients']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Custom Permission
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    
# Update View
class RecipeUpdateView(UpdateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated, IsOwner]

# Delete View
class RecipeDeleteView(DestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated, IsOwner]

# 
class RecipesByCategoryView(ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        category = self.kwargs['category']
        return Recipe.objects.filter(category__icontains=category)

class RecipesByIngredientView(ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        ingredients = self.request.query_params.getlist('ingredients')
        queryset = Recipe.objects.all()
        for ingredient in ingredients:
            queryset = queryset.filter(ingredients__icontains=ingredient)

        return queryset
    
class RecipeSearchView(ListAPIView):
    serializer_Class = RecipeSerializer

    def get_queryset(self):
        title = self.request.query_params.get('title')
        queryset = Recipe.objects.all()

        # Search filters
        title = self.request.query_params.get('title')
        category = self.request.query_params.get('category')
        preparation_time = self.request.query_params.get('preparation_time')
        cooking_time = self.request.query_params.get('cooking_time')
        servings  = self.request.query_params.get('servings')
         
        if title:
            queryset = queryset.filter(title__icontains=title)
        if category:
            queryset = queryset.filter(category__icontains=category)
        if preparation_time:
            queryset = queryset.filter(preparation_time__lte=preparation_time)
        if cooking_time:
            queryset = queryset.filter(title__lte=cooking_time)
        if servings:
            queryset = queryset.filter(servings__gte=servings)  

        return queryset

# Using DRF permissions and IsAuthenticated to restrict recipe creation
class RecipeListCreateView(ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RecipeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
                                              
        
    
     