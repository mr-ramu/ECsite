from django.db import models
from accounts.models import Users


class ProductTypes(models.Model):
  name = models.CharField(max_length=1000)

  class Meta:
    db_table = 'product_types'

  def __str__(self):
    return self.name
  

class Manufacturers(models.Model):
  name = models.CharField(max_length=1000)

  class Meta:
    db_table = 'manufactures'

    def __str__(self):
      return self.name
    

class Products(models.Model):
  name = models.CharField(max_length=1000)
  price = models.IntegerField()
  stock = models.IntegerField()
  product_type = models.ForeignKey(
    ProductTypes, on_delete=models.CASCADE
  )
  manufacturer = models.ForeignKey(
    Manufacturers, on_delete=models.CASCADE
  )

  class Meta:
    db_table = 'products'
    
    def __str__(self):
      return self.name
    

class ProductPictures(models.Model):
  picture = models.FileField(upload_to='product_pictures/')
  product = models.ForeignKey(
    Products, on_delete=models.CASCADE
  )
  order = models.IntegerField()

class Meta:
  db_table = 'product_pictures'
  ordering = ['order']

def __str__(self):
  return self.product.name + ': ' + str(self.order)


class Carts(models.Model):
  user = models.OneToOneField(
    Users,
    on_delete=models.CASCADE,
    primary_key=True
  )

  class Meta:
    db_table = 'carts'

class CartItemsManager(models.Manager):
  def save_item(self, product_id, quantity, cart):
    c = self.model(quantity=quantity, product_id=product_id, cart=cart)
    c.save()

class CartItems(models.Model):
  quantity = models.PositiveIntegerField()
  product = models.ForeignKey(
    Products, on_delete=models.CASCADE
  )
  cart = models.ForeignKey(
    Carts, on_delete=models.CASCADE
  )
  objects = CartItemsManager()

  class Meta:
    db_table = 'cart_items'
    unique_together = [[ 'product', 'cart' ]]