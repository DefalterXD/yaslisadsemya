from django import forms
from django.contrib import admin
from .models import DocumentCategory, Document

# --- ФОРМА ДЛЯ ДОКУМЕНТА (ДВА ПОЛЯ) ---
class DocumentAdminForm(forms.ModelForm):
    # Поле для выбора только ГЛАВНЫХ категорий
    main_category = forms.ModelChoiceField(
        queryset=DocumentCategory.objects.filter(parent__isnull=True),
        label="КАТЕГОРИЯ",
        required=True
    )
    
    # Поле для выбора ПОДКАТЕГОРИИ
    sub_category = forms.ModelChoiceField(
        queryset=DocumentCategory.objects.filter(parent__isnull=False),
        label="САБКАТЕГОРИЯ (если имеется)",
        required=False
    )

    class Meta:
        model = Document
        fields = ['main_category', 'sub_category', 'title', 'file', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Скрываем стандартное поле category, оно заполнится автоматически при сохранении
        self.fields['category'].widget = forms.HiddenInput()
        self.fields['category'].required = False

# --- ВКЛАДКА ДОКУМЕНТЫ ---
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    form = DocumentAdminForm
    list_display = ('title', 'get_main_cat', 'get_sub_cat', 'uploaded_at')
    list_filter = ('category',)

    @admin.display(description="КАТЕГОРИЯ")
    def get_main_cat(self, obj):
        return obj.category.parent.name if obj.category.parent else obj.category.name

    @admin.display(description="САБКАТЕГОРИЯ")
    def get_sub_cat(self, obj):
        return obj.category.name if obj.category.parent else "-"

    def save_model(self, request, obj, form, change):
        # Логика сохранения: если выбрана сабкатегория — используем её, 
        # если нет — используем главную категорию.
        main = form.cleaned_data.get('main_category')
        sub = form.cleaned_data.get('sub_category')
        obj.category = sub if sub else main
        super().save_model(request, obj, form, change)

# --- ВКЛАДКА 1: ТОЛЬКО ГЛАВНЫЕ КАТЕГОРИИ ---
@admin.register(DocumentCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ('parent',)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent__isnull=True)

# --- ВКЛАДКА 2: САБКАТЕГОРИИ (ЗЕРКАЛО) ---
class SubCategoryProxy(DocumentCategory):
    class Meta:
        proxy = True
        verbose_name = "Сабкатегория"
        verbose_name_plural = "Сабкатегории (Добавить сюда)"

@admin.register(SubCategoryProxy)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent__isnull=False)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = DocumentCategory.objects.filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)