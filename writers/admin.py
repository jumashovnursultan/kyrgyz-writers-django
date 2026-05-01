from django.contrib import admin
from .models import Writer, Quote, Work, Favorite

@admin.register(Writer)
class WriterAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_year', 'death_year', 'epoch', 'language')
    search_fields = ('name', 'epoch', 'tags')
    list_filter = ('epoch', 'language')

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('writer', 'text')
    list_filter = ('writer',)

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer', 'year', 'genre')
    list_filter = ('writer', 'genre')
    search_fields = ('title',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'writer', 'created_at')
