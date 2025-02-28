from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("recipes/", views.RecipeListView.as_view(), name="recipe_list"),
    path("recipe/<int:pk>/", views.RecipeDetailView.as_view(), name="recipe_detail"),
    path("recipe/new/", views.RecipeCreateView.as_view(), name="recipe_create"),
    path("register/", views.register, name="register"),
    path("varieties/", views.jollof_varieties, name="jollof_varieties"),
    path("varieties/<str:variety>/", views.variety_detail, name="variety_detail"),
    path("comment/<int:comment_id>/edit/", views.edit_comment, name="edit_comment"),
    path(
        "comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"
    ),
    path(
        "recipe/<int:pk>/update/",
        views.RecipeUpdateView.as_view(),
        name="recipe_update",
    ),
    path(
        "recipe/<int:pk>/delete/",
        views.RecipeDeleteView.as_view(),
        name="recipe_delete",
    ),
    path(
        "recipe/<int:pk>/comment/", views.AddCommentView.as_view(), name="add_comment"
    ),
    path("recipe/<int:pk>/rating/", views.AddRatingView.as_view(), name="add_rating"),
]
