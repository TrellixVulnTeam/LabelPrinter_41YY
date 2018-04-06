from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from printerCtrl import views

urlpatterns = [
    url(r'^print/$', views.PrintProduct.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
