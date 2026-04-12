from django.contrib import admin
from .models import DocumentCategory, Document

# Вкладка 1: Чисто для ГЛАВНЫХ категорий
@admin.register(DocumentCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # Показываем только главные категории (где нет родителя)
    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent__isnull=True)
    
    # При создании новой категории в этой вкладке, поле "Родитель" будет скрыто
    exclude = ('parent',)

# Вкладка 2: Для Документов с нормальным отображением
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_main_cat', 'get_sub_cat', 'uploaded_at')
    list_filter = ('category',)

    @admin.display(description="КАТЕГОРИЯ")
    def get_main_cat(self, obj):
        return obj.category.parent.name if obj.category.parent else obj.category.name

    @admin.display(description="САБКАТЕГОРИЯ")
    def get_sub_cat(self, obj):
        return obj.category.name if obj.category.parent else "-"
    
    # Создаем "зеркало" для сабкатегорий
class SubCategoryProxy(DocumentCategory):
    class Meta:
        proxy = True
        verbose_name = "Сабкатегория"
        verbose_name_plural = "Сабкатегории (Добавить сюда)"

@admin.register(SubCategoryProxy)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    
    def get_queryset(self, request):
        # В этой вкладке только вложенные
        return super().get_queryset(request).filter(parent__isnull=False)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Чтобы в выборе родителя были только ГЛАВНЫЕ
        if db_field.name == "parent":
            kwargs["queryset"] = DocumentCategory.objects.filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)