from printerCtrl.models import Product
from printerCtrl.serializers import ProductSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse

import os


class PrintProduct(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        print(data)
        filename = "../printer/QRFiles/" + data['ProductId'] + "_" + data['Quantity'] + ".bin"
        excute_order="brother_ql_print --backend network " + filename + " tcp://192.168.1.152:9100"
        print(excute_order)
        # os.system("brother_ql_print --backend network ../printer/QRFiles/Test.bin tcp://192.168.1.152:9100")
        os.system(excute_order)
        return JsonResponse("ACTION COMPLETED", status=200, safe=False)
