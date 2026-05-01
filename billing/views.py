from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer, Product, Invoice
from .serializers import CustomerSerializer, ProductSerializer, InvoiceSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.filter(is_active=True)  # Solo clientes activos
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['document_number']
    search_fields = ['first_name', 'last_name', 'email', 'document_number']

    def destroy(self, request, *args, **kwargs):
        """Soft delete: marca como inactivo en lugar de eliminar"""
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(
            {'success': True, 'message': 'Cliente eliminado correctamente'},
            status=status.HTTP_200_OK
        )

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related('customer').prefetch_related('items__product')
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'customer']
    ordering_fields = ['created_at', 'total_amount']
