from django.db import models

class DocumentCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name of the category")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories', verbose_name='Parent category')

    class Meta:
        verbose_name = "Document category"
        verbose_name_plural = "Document categories"

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} -> {self.name}"
        return self.name

class Document(models.Model):
    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE, related_name='documents', verbose_name="Category")
    title = models.CharField(max_length=200, verbose_name="Name of the document")
    file = models.FileField(upload_to='documents/', verbose_name="File")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def __str__(self):
        return self.title