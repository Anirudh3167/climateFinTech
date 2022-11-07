from rest_framework.response import Response
from rest_framework.decorators import api_view
from Backend.models import CartItems
from .serializers import CartSerializer

@api_view(['GET'])
def getData(request):
    items = CartItems.objects.all()
    serializer = CartSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def PostData(request):
    serializer = CartSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

