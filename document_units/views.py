from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from document_units.models import DocumentFormat
from document_units.serializers import DocumentFormatSerializer
# Create your views here.


class DocumentFormatViewSet(ViewSet):
    queryset = DocumentFormat.objects.all()
    serializer_class = DocumentFormatSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser, ]
