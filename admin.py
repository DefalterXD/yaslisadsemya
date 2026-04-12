from django import forms
from django.contrib import admin
from .models import DocumentCategory, Document, MainCategory, SubCategory

class DocumentAdminForm(forms.ModelForm):
    # Поле для выбора только ГЛАВНЫХ категорий
    main_category = forms.ModelChoiceField(
        queryset=DocumentCategory.objects.filter(parent__isnull=True),
        label="1. Выберите основную категорию",
        required=True
    )
    
    # Поле для выбора ПОДКАТЕГОРИИ
    sub_category = forms.ModelChoiceField(
        queryset=DocumentCategory.objects.filter(parent__isnull=False),
        label="2. Выберите подкатегорию (если нужно)",
        required=False
    )

    class Meta:
        model = Document
        fields = ['main_category', 'sub_category', 'title', 'file', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Прячем стандартное поле category, оно заполнится автоматически
        self.fields['category'].widget = forms.HiddenInput()
        self.fields['category'].required = False

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    form = DocumentAdminForm
    list_display = ('title', 'get_main', 'get_sub', 'uploaded_at')

    def get_main(self, obj):
        return obj.category.parent.name if obj.category.parent else obj.category.name
    get_main.short_description = 'КАТЕГОРИЯ'

    def get_sub(self, obj):
        return obj.category.name if obj.category.parent else "-"
    get_sub.short_description = 'САБКАТЕГОРИЯ'

    def save_model(self, request, obj, form, change):
        # Логика: если выбрана сабкатегория — привязываем к ней. 
        # Если нет — к главной.
        main = form.cleaned_data.get('main_category')
        sub = form.cleaned_data.get('sub_category')
        obj.category = sub if sub else main
        super().save_model(request, obj, form, change)

# Регистрация категорий (те самые отдельные вкладки, которые мы делали)
@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    exclude = ('parent',)
    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent__isnull=True)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent__isnull=False)