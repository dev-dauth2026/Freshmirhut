from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([Customer,Product,Cart,CartProduct,Order,BusinessContact,BusinessTime,Notice,Admin,ProductImage,About,Service,Help,ContactUs,Update,YoutubeVideo,Career,SavedProduct])