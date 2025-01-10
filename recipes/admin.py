from django.contrib import admin
from .models import Recipe

# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'prep_time', 'cook_time', 'servings', 'created_date')
    search_fields = ('title', 'ingredients')

    
admin.site.register(Recipe, RecipeAdmin)
