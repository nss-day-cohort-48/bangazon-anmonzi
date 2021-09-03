"""Customer order model"""
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from .customer import Customer
from .product import Product


class CustomerProductLike(models.Model):
    customer = models.ForeignKey("Customer", on_delete=DO_NOTHING)
    product = models.ForeignKey("Product", on_delete=CASCADE)