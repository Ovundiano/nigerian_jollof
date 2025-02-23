from django.contrib import admin
from .models import Category, Recipe, Rating, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'cooking_time', 'servings', 'created_at', 'average_rating')
    list_filter = ('category', 'created_at', 'author')
    search_fields = ('title', 'description', 'ingredients')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'author', 'image')
        }),
        ('Recipe Details', {
            'fields': ('ingredients', 'instructions', 'cooking_time', 'servings')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('recipe__title', 'user__username')
    readonly_fields = ('created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'content_preview', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('content', 'recipe__title', 'user__username')
    readonly_fields = ('created_at',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Comment Preview'
