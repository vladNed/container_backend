from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.files.storage import FileSystemStorage

from projects.models import Project
from document_units.exceptions import InvalidFormatData
# Create your models here.

system_storage = FileSystemStorage(location='/media/documents')


class RawJSONField(JSONField):
    def db_type(self, connection):
        return 'json'


class DocumentFormatManager(models.Manager):

    VALID_FORMAT_TYPES = ['text', 'date', 'number']

    def create_format(self, name, project, data):
        '''
        Validates format data and creates format
        '''
        if not isinstance(data, dict):
            raise InvalidFormatData

        if len(data.keys()) < 0:
            raise InvalidFormatData

        for key, value in data.items():
            if value not in self.VALID_FORMAT_TYPES:
                raise InvalidFormatData

        document_format = self.model(name=name, project=project, data=data)
        document_format.save(using=self._db)

        return document_format


class DocumentFormat(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    data = JSONField(null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='formats', null=False)

    objects = DocumentFormatManager()

    def __str__(self):
        return f'[{self.id}] {self.name} -> {self.project}'


class DocumentUnit(models.Model):
    name = models.CharField(max_length=200, null=False)
    text = models.TextField(default="no text provided")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="documents", null=False)
    document_data = RawJSONField(null=True, default=dict)
    document_file = models.FileField(storage=system_storage, null=False)
    document_format = models.ForeignKey(DocumentFormat, on_delete=models.CASCADE, related_name='documents', null=True)

    def __str__(self):
        return f'[{self.id}] {self.name}'
