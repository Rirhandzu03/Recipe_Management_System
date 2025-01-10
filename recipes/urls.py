from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeUpdateView, RecipeDeleteView, RecipesByCategoryView, RecipesByIngredientView, RecipeSearchView, RecipeListCreateView, RecipeDetailView
from . import views

# Initialize the router
router = DefaultRouter()

# Register the viewsets with the router
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'recipes', views.RecipeViewSet, basename='recipe')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:pk>/edit/', RecipeUpdateView.as_view(), name='recipe-edit'),
    path('recipes/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe-delete'),
    path('recipes/category/<str:category>/', RecipesByCategoryView.as_view(), name='recipes-by-category'),
    path('recipes/ingredients/', RecipesByIngredientView.as_view(), name='recipes-by-ingredients'),
    path('recipes/search/', RecipeSearchView.as_view(), name='recipe-search'),
    path('', RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
]

