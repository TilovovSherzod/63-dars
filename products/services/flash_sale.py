from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from products.models import Product, ProductViewHistory

from rest_framework import generics, serializers
from products.models import FlashSale

# ViewSets da yozilgan varianti
class FlashSaleListCreateView(generics.ListCreateAPIView):
    queryset = FlashSale.objects.all()

    class FlashSaleSerializer(serializers.ModelSerializer):
        class Meta:
            model = FlashSale
            fields = ('id', 'product', 'discount_percentage', 'start_time', 'end_time')

    serializer_class = FlashSaleSerializer


@api_view(['GET'])
def check_flash_sale(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    user_viewed = ProductViewHistory.objects.filter(user=request.user, product=product).exists()

    upcoming_flash_sale = FlashSale.objects.filter(
        product=product,
        start_time__lte=datetime.now() + timedelta(hours=24)
    ).first()

    if user_viewed and upcoming_flash_sale:
        discount = upcoming_flash_sale.discount_percentage
        start_time = upcoming_flash_sale.start_time
        end_time = upcoming_flash_sale.end_time
        return Response({
            "message": f"This product will be on a {discount}% off flash sale!",
            "start_time": start_time,
            "end_time": end_time
        })
    else:
        return Response({
            "message": "No upcoming flash sales for this product."
        })


# Generic Views da yozilgan varianti


# class FlashSaleListCreateView(generics.ListCreateAPIView):
#     queryset = FlashSale.objects.all()
#
#     class FlashSaleSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = FlashSale
#             fields = ('id', 'product', 'discount_percentage', 'start_time', 'end_time')
#
#     serializer_class = FlashSaleSerializer
#
#
# @api_view(['GET'])
# def check_flash_sale(request, product_id):
#     try:
#         product = Product.objects.get(id=product_id)
#     except Product.DoesNotExist:
#         return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
#
#     user_viewed = ProductViewHistory.objects.filter(user=request.user, product=product).exists()
#
#     upcoming_flash_sale = FlashSale.objects.filter(
#         product=product,
#         start_time__lte=datetime.now() + timedelta(hours=24)
#     ).first()
#
#     if user_viewed and upcoming_flash_sale:
#         discount = upcoming_flash_sale.discount_percentage
#         start_time = upcoming_flash_sale.start_time
#         end_time = upcoming_flash_sale.end_time
#         return Response({
#             "message": f"This product will be on a {discount}% off flash sale!",
#             "start_time": start_time,
#             "end_time": end_time
#         })
#     else:
#         return Response({
#             "message": "No upcoming flash sales for this product."
#         })


# APIViews da yozilgan varianti

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from datetime import datetime, timedelta
# from products.models import Product, ProductViewHistory, FlashSale
# from rest_framework import serializers

# class FlashSaleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FlashSale
#         fields = ('id', 'product', 'discount_percentage', 'start_time', 'end_time')
#
#
# class FlashSaleListCreateView(APIView):
#     def get(self, request):
#         flash_sales = FlashSale.objects.all()
#         serializer = FlashSaleSerializer(flash_sales, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = FlashSaleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class CheckFlashSaleView(APIView):
#     def get(self, request, product_id):
#         try:
#             product = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
#
#         user_viewed = ProductViewHistory.objects.filter(user=request.user, product=product).exists()
#
#         upcoming_flash_sale = FlashSale.objects.filter(
#             product=product,
#             start_time__lte=datetime.now() + timedelta(hours=24)
#         ).first()
#
#         if user_viewed and upcoming_flash_sale:
#             discount = upcoming_flash_sale.discount_percentage
#             start_time = upcoming_flash_sale.start_time
#             end_time = upcoming_flash_sale.end_time
#             return Response({
#                 "message": f"This product will be on a {discount}% off flash sale!",
#                 "start_time": start_time,
#                 "end_time": end_time
#             })
#         else:
#             return Response({
#                 "message": "No upcoming flash sales for this product."
#             })
