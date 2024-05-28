from django.urls import path
from .views import(
  ProductListView, ProductDetailView,
  add_product,
)

app_name = 'stores'
urlpatterns = [
  path('product_list/', ProductListView.as_view(), name='product_list'),
  path('product_detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
  path('add_product/', add_product, name='add_product'),
]