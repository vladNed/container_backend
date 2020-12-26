from rest_framework import serializers
from document_units.models import DocumentFormat, DocumentUnit


class DocumentUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentUnit
        fields = '__all__'


class DocumentFormatSerializer(serializers.ModelSerializer):
    documents = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = DocumentFormat
        fields = '__all__',
