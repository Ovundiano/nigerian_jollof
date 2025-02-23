from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('recipes/', views.RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/new/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('register/', views.register, name='register'),
    path('varieties/', views.jollof_varieties, name='jollof_varieties'),
    path('varieties/<str:variety>/', views.variety_detail, name='variety_detail'),
]
