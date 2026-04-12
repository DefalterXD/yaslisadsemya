from django.contrib import admin
from .models import DocumentCategory, Document
from django import forms

class DocumentAdminForm(forms.ModelForm):
    # Создаем дополнительное поле для выбора подкатегории
    subcategory = forms.ModelChoiceField(
        queryset=DocumentCategory.objects.none(), 
        required=False, 
        label="Подкатегория"
    )

    class Meta:
        model = Document
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ограничиваем основное поле 'category' только ГЛАВНЫМИ категориями
        self.fields['category'].queryset = DocumentCategory.objects.filter(parent__isnull=True)
        self.fields['category'].label = "Основная категория"

        # Если мы редактируем уже существующий документ
        if self.instance and self.instance.pk and self.instance.category:
            if self.instance.category.parent:
                # Если текущая категория документа — это подкатегория
                self.initial['subcategory'] = self.instance.category
                self.initial['category'] = self.instance.category.parent
                self.fields['subcategory'].queryset = DocumentCategory.objects.filter(parent=self.instance.category.parent)
            else:
                # Если категория главная, подгружаем её подкатегории в список
                self.fields['subcategory'].queryset = DocumentCategory.objects.filter(parent=self.instance.category)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    form = DocumentAdminForm
    list_display = ('title', 'category', 'uploaded_at')
    
    def save_model(self, request, obj, form, change):
        # Если выбрана подкатегория, сохраняем её как основную категорию документа
        subcategory = form.cleaned_data.get('subcategory')
        if subcategory:
            obj.category = subcategory
        super().save_model(request, obj, form, change)