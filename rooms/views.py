from .models import Room, Product, Category, Payment, ProductUsed, Bill
from rest_framework import viewsets, mixins, views, filters
from rest_framework import permissions
from accounts.pagination import PaginationHandlerMixin, StandardResultsSetPagination, LargeResultsSetPagination
from .serializers import RoomSerializer, ProductSerializer, CategorySerializer, PaymentSerializer, ProductUsedSerializer, BillSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from decimal import *


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter)
    search_fields = ['roomId', 'price', 'status', 'id']
    filterset_fields = ['status']
    # Explicitly specify which fields the API may be ordered against

    # This will be used as the default ordering
    ordering = ['-created_at']


class AllRoomViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter)

    search_fields = ['roomId', 'price', 'status', 'id']

    # Explicitly specify which fields the API may be ordered against
    filterset_fields = ['status']
    # This will be used as the default ordering
    ordering = ['-created_at']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter)
    search_fields = ['id', 'sku', 'productName', 'price']
    filterset_fields = ['productName', 'sku']
    # Explicitly specify which fields the API may be ordered against

    # This will be used as the default ordering
    ordering = ['-created_at']


class AllProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

    # Explicitly specify which fields the API may be ordered against

    # This will be used as the default ordering
    ordering = ['-created_at']


class AllPaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all().order_by('-created_at')
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

    # Explicitly specify which fields the API may be ordered against

    # This will be used as the default ordering
    ordering = ['-created_at']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

    # Explicitly specify which fields the API may be ordered against

    # This will be used as the default ordering
    ordering = ['-created_at']


class AllCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

    # Explicitly specify which fields the API may be ordered against

    # This will be used as the default ordering
    ordering = ['-created_at']


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
        instance = Payment.objects.all().order_by('created_at')

        my_model_fields = [field.name for field in Payment._meta.get_fields()]

        if 'ordering' in request.query_params:

            sort_by = request.query_params.get('ordering')
            if sort_by is not None and sort_by in my_model_fields or sort_by[1:] in my_model_fields:
                instance = instance.order_by(sort_by)

        if 'status' in request.query_params:
            status = request.query_params.get('status')
            if status:
                instance = instance.filter(status=status)

        page = self.paginate_queryset(instance)

        if page is not None:
            serializer = self.get_paginated_response(PaymentSerializer(
                instance=page, context={'request': request}, many=True).data)
        else:
            serializer = PaymentSerializer(
                instance, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_class = ProductSerializer
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = serializer.save()
        payment.total = payment.get_total()

        room = get_object_or_404(Room, pk=request.data['room'])
        payment.price = room.price
        if (room.status == 'notAvailable'):
            return Response({"Room": [{"msg": "Room is not available"}]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # check stock in product:
        for product in request.data["products"]:
            _product = get_object_or_404(Product, pk=product['productId'])

            product_used_serializer = ProductUsedSerializer(data=product)

            # check Stock
            if _product.stock - Decimal(product['quantity']) < 0:
                return Response({'Products': [{"quantity": "There is only " + str(_product.stock) + " products left"}]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        room.status = 'notAvailable'

        room.save()

        payment.save()

        for product in request.data["products"]:

            product["payment"] = payment.id

            _product = get_object_or_404(Product, pk=product['productId'])

            product_used_serializer = ProductUsedSerializer(data=product)
            product_used_serializer.price = _product.price
            product_used_serializer.is_valid(raise_exception=True)
            new_product_used = product_used_serializer.save()

            # Update product stock

            _product.stock = _product.stock - new_product_used.quantity
            _product.save()

        if payment.status == "checkedOut":
            room = get_object_or_404(Room, pk=payment.room.id)

            room.status = 'available'

            room.save()

        payment.total = payment.get_total()

        payment.save()

        return Response(
            PaymentSerializer(payment).data
        )


class RetrivePaymentViewSet(views.APIView, PaginationHandlerMixin):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None, pk=None):
        """
        Return a single user.
        """
        instance = get_object_or_404(
            Payment, pk=pk)

        serializer = PaymentSerializer(
            instance=instance, context={'request': request})
        return Response(serializer.data)

    def put(self, request, format=None, pk=None):
        """
        Update Payment.
        """
        instance = get_object_or_404(Payment, pk=pk)
        # if instance.status == "checkedOut":
        #     return Response({"msg": "The payment can not be modified"})
        serializer = PaymentSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        if (request.data['status'] == 'checkedOut'):
            room = get_object_or_404(Room, pk=instance.room.id)

            room.status = 'available'

            room.save()

        instance.total = instance.get_total()

        instance.save()

        # check stock
        for product in request.data["products"]:

            # Check id of product
            productUsed = get_object_or_404(Product, pk=product["productId"])
            # Serializer
            product_used_serializer = ProductUsedSerializer(data=product)

            try:

                exitsProduct = ProductUsed.objects.all().get(
                    payment=instance, productId=product["productId"])
                if productUsed.stock + exitsProduct.quantity - Decimal(product['quantity']) < 0:
                    return Response({'Products': [{"quantity": "There is only " + str(productUsed.stock) + " products left"}]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except ObjectDoesNotExist:

                if productUsed.stock - Decimal(product['quantity']) < 0:
                    return Response({'Products': [{"quantity": "There is only " + str(productUsed.stock) + " products left"}]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # add quantity before delete
        for productUsed in ProductUsed.objects.all().filter(payment=instance):
            product_used = ProductUsedSerializer(productUsed)
            product = Product.objects.all().get(
                pk=product_used["productId"].value)
            product.stock = product.stock + \
                Decimal(product_used["quantity"].value)

            product.save()

        # Delete old product
        ProductUsed.objects.filter(payment=instance).delete()

        # Create new product used
        for product in request.data["products"]:
            product["payment"] = instance.id
            # Check id of product
            productUsed = get_object_or_404(Product, pk=product["productId"])
            # Serializer
            product_used_serializer = ProductUsedSerializer(data=product)
            product_used_serializer.price = productUsed.price
            product_used_serializer.is_valid(raise_exception=True)
            new_product_used = product_used_serializer.save()

        # Update product stock
        for productUsed in instance.products.all():
            product_used = ProductUsedSerializer(productUsed)
            id = product_used["productId"].value

            product = get_object_or_404(Product, pk=id)

            product.stock = product.stock - productUsed.quantity
            product.save()

        instance.total = instance.get_total()

        instance.save()

        return Response(PaymentSerializer(instance=instance).data)

    def delete(selt, request, format=None, pk=None):
        payment = get_object_or_404(Payment, pk=pk)
        room = get_object_or_404(Room, pk=payment.room.id)
        room.status = 'available'
        if payment.status == 'checkedIn':
            # add quantity before delete
            for productUsed in ProductUsed.objects.all().filter(payment=payment):
                product_used = ProductUsedSerializer(productUsed)
                product = Product.objects.all().get(
                    pk=product_used["productId"].value)
                product.stock = product.stock + \
                    Decimal(product_used["quantity"].value)

                product.save()

        if payment.status == 'checkedOut':
            if request.user.is_staff == False:
                return Response({"Authenticated": {"msg": "Unauthodized"}}, status=status.HTTP_401_UNAUTHORIZED)

        room.save()
        payment_deleted = payment.delete()
        return Response({'msg': payment_deleted})
