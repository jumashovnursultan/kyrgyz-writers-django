from django.contrib import admin
from .models import Writer, Quote

@admin.register(Writer)
class WriterAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_year', 'death_year', 'epoch')
    search_fields = ('name', 'epoch')

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('writer', 'text')
    list_filter = ('writer',)