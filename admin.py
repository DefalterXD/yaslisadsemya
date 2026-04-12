from django.contrib import admin
from .models import DocumentCategory, Document

class SubCategoryInline(admin.TabularInline):
    model = DocumentCategory
    extra = 1
    verbose_name = "Подкатегория"
    fk_name = 'parent'

@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_subcategory')
    list_filter = ('parent',)
    inlines = [SubCategoryInline] # Позволяет добавлять подкатегории прямо внутри основной
    
    def is_subcategory(self, obj):
        return "Да" if obj.parent else "Нет"
    is_subcategory.short_description = "Это подкатегория?"

    def get_queryset(self, request):
        # В основном списке показываем всё, чтобы можно было редактировать
        return super().get_queryset(request)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    # Удобный поиск категории при добавлении документа
    autocomplete_fields = ['category']

# Добавляем поиск для категорий, чтобы autocomplete работал
DocumentCategoryAdmin.search_fields = ['name']