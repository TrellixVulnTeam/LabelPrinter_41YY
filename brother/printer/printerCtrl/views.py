from printerCtrl.models import Product
from printerCtrl.serializers import ProductSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse

from PIL import Image


import os
import urllib.request
import requests


class PrintProduct(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        print(data)
        print("Retrieving Image from " + data['ImageURL'])
        original_image_path = "../printer/QRFiles/" + data['ProductId'] + data['dataFormat']
        resized_image_path = "../printer/QRFiles/resized_" + data['ProductId'] + data['dataFormat']
        rotated_image_path = "../printer/QRFiles/rotated_" + data['ProductId'] + data['dataFormat']
        urllib.request.urlretrieve(data['ImageURL'], original_image_path)
        # Resezin Image to fit it into small label paper
        # original_image=Image.open(original_image_path)
        # original_image.rotate(90, expand=True).save(rotated_image_path)

        # rotated_image=Image.open(rotated_image_path)
        # w, h = rotated_image.size
        # print('The rotated image size is {wide} wide x {height} high'.format(wide=w, height=h))
        # if data['Width']:
        #     width = data['Width']
        # if data['Height']:
        #     height = data['Height']
        # if width and height:
        #     max_size = (width, height)
        # elif width:
        #     max_size = (width, h)
        # elif height:
        #     max_size = (w, height)
        # else:
            # No width or height specified
            # raise RuntimeError('Width or height required!')

        # print ('MaxSize = ' + str(max_size))

        # rotated_image.thumbnail(max_size, Image.ANTIALIAS)
        # rotated_image.save(resized_image_path)

        # scaled_image = Image.open(resized_image_path)
        # width, height = scaled_image.size
        # print('The scaled image size is {wide} wide x {height} '
        #     'high'.format(wide=width, height=height))

        # Using Brother libraries to print the image
        print("Creating bin file for image " + "../printer/QRFiles/" + data['ProductId'] + data['dataFormat'])
        excute_order="brother_ql_create --model QL-710W --label-size 29 " + original_image_path + " > " + data['ProductId'] + ".bin"
        os.system(excute_order)
        print("Preparing to print file" + "../printer/QRFiles/" + data['ProductId'] + ".bin")
        excute_order="brother_ql_print --backend network " + data['ProductId'] + ".bin" + " tcp://192.168.1.152:9100"
        print("Printing: " + excute_order)
        # os.system("brother_ql_print --backend network ../printer/QRFiles/Test.bin tcp://192.168.1.152:9100")
        os.system(excute_order)
        return JsonResponse("ACTION COMPLETED", status=200, safe=False)

class MoveLegoArm(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        # data = JSONParser().parse(request)
        print("EndPoint Ready")
        requests.get("http://192.168.1.113:8080/initialize/")
        requests.get("http://192.168.1.113:8080/move_start/")
        return JsonResponse("ACTION COMPLETED", status=200, safe=False)
