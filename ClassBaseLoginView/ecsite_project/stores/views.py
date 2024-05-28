from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404

import os
from .models import(
  Products,Carts, CartItems
)

class ProductListView(LoginRequiredMixin, ListView):
  model = Products
  template_name = os.path.join('stores', 'product_list.html')

  def get_queryset(self):
    query = super().get_queryset()
    product_type_name = self.request.GET.get('product_type_name',  None)
    product_name = self.request.GET.get('product_name',  None)
    if product_type_name:
      query = query.filter(
        product_type__name=product_type_name
      )
    if product_name:
      query = query.filter(
        name = product_name
      )
    order_by_price = self.request.GET.get('order_by_price', 0)
    if order_by_price == '1':
      query = query.order_by('price')
    elif order_by_price == '2':
      query =  query.order_by('-price')
    return query
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['product_type_name'] = self.request.GET.get('product_type_name', '')
    context['product_name'] = self.request.GET.get('product_name', '')
    order_by_price = self.request.GET.get('order_by_price', 0)
    if order_by_price == '1':
      context['ascending'] = True
    elif order_by_price == '2':
      context['descending'] = True
    return context
  
class ProductDetailView(LoginRequiredMixin, DetailView):
  model = Products
  template_name = os.path.join('stores', 'product_detail.html')

@login_required
def add_product(request):
  if request.is_ajax:
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')
    product = get_object_or_404(Products, id=product_id)
    if int(quantity) > product.stock:
      response = JsonResponse({'message': '在庫数を超えています'})
      response.status_code = 403
      return response
    if int(quantity) <= 0:
      response = JsonResponse({'message': '0より大きい値を入力してください'})
      response.status_code = 403
      return response
    cart = Carts.objects.get_or_create(
      user=request.user
    )
    if all([product_id, cart, quantity]):
      CartItems.objects.save_item(
        quantity=quantity, product_id=product_id,
        cart=cart[0]
      )
   
      return JsonResponse({'message': '商品をカートに追加しました'})
    