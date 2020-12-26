from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.files.storage import FileSystemStorage

from projects.models import Project
# Create your models here.

system_storage = FileSystemStorage(location='/media/documents')


class RawJSONField(JSONField):
    def db_type(self, connection):
        return 'json'


class DocumentFormat(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    data = RawJSONField(default=dict)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='formats', null=False)

    def __str__(self):
        return f'[{self.id}] {self.name} -> {self.project}'


class DocumentUnit(models.Model):
    name = models.CharField(max_length=200, null=False)
    text = models.TextField(default="no text provided")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="documents", null=False)
    document_data = RawJSONField(null=True, default=dict)
    document_file = models.FileField(storage=system_storage)
    document_format = models.ForeignKey(DocumentFormat, on_delete=models.CASCADE, related_name='documents', null=True)

    def __str__(self):
        return f'[{self.id}] {self.name}'
