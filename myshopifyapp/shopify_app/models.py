from django.db import models

class Shop(models.Model):
    shopify_domain = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)

    def __str__(self):
        return self.shopify_domain
