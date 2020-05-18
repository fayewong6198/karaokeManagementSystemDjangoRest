from .models import Room, Product, Category, Payment, ProductUsed
from rest_framework import viewsets, mixins, views
from rest_framework import permissions
from accounts.pagination import PaginationHandlerMixin, StandardResultsSetPagination
from .serializers import RoomSerializer, ProductSerializer, CategorySerializer, PaymentSerializer, ProductUsedSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Room.objects.all().order_by('-created_at')
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


# class PaymentViewSet(viewsets.ModelViewSet):
#     queryset = Payment.objects.all().order_by('-created_at')
#     serializer_class = PaymentSerializer
#     permission_classes = [permissions.IsAuthenticated]

class ListCreatePaymentViewSet(views.APIView, PaginationHandlerMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Payment.objects.all().order_by('-created_at')

    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        instance = Payment.objects.all().order_by('-created_at')
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(PaymentSerializer(page,
                                                                       many=True).data)
        else:
            serializer = PaymentSerializer(
                instance, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_class = RegisterSerializer
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()

        # Create schedule for user
        for product in request.data["products"]:
            product["payment"] = payment.id
            product_used_serializer = ProductUsedSerializer(data=product)
            product_used_serializer.is_valid(raise_exception=True)
            new_product_used = product_used_serializer.save()

        return Response({
            'user': PaymentSerializer(payment).data
        })


class RetrivePaymentViewSet(views.APIView, PaginationHandlerMixin):

    def get(self, request, format=None, pk=None):
        """
        Return a single user.
        """
        instance = get_object_or_404(Payment, pk=pk)

        serializer = Payment(instance=instance)
        return Response(serializer.data)

    def put(self, request, format=None, pk=None):
        """
        Update Payment.
        """
        instance = get_object_or_404(User, pk=pk)
        serializer = PaymentSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        instance.save()
        # Delete old product
        ProductUsed.objects.filter(staff=instance).delete()

        # Update schedule for user
        for product in request.data["products"]:
            product["payment"] = instance.id
            product_used_serializer = ProductUsedSerializer(data=product)
            product_used_serializer.is_valid(raise_exception=True)
            new_product_used = product_used_serializer.save()

        return Response(PaymentSerializer(instance=instance).data)

    def delete(selt, request, format=None, pk=None):
        payment = get_object_or_404(Payment, pk=pk)
        print(Payment)
        payment.delete()
        return Response({'msg': 'User deleted'})
