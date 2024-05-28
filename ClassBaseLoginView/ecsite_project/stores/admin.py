from django.contrib import admin
from .models import(
  ProductTypes, Manufacturers, Products,
  ProductPictures
)
# Register your models here.

admin.site.register(
  [ProductTypes, Manufacturers, Products,ProductPictures]
)