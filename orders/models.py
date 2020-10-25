from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save, post_save

from products.models import Product

User = get_user_model()

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('stale', 'Stale'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class Order(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='created')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_address = models.TextField(blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)
    inventory_updated = models.BooleanField(default=False)

    def mark_paid(self, custom_amount=None, save=False):
        paid_amount = self.total

        if custom_amount is not None:
            paid_amount = custom_amount

        self.paid = paid_amount
        self.status = 'paid'

        if not self.inventory_updated and self.product:
            self.product.remove_items_from_inventory(count=1, save=True)
            self.inventory_updated = True

        if save is True:
            self.save()
        return self.paid

    def calculate(self, save=False):
        if not self.product:
            return {}

        subtotal = self.product.price
        tax_rate = Decimal(0.12)
        tax_total = subtotal * tax_rate
        tax_total = Decimal("%.2f" % tax_total)
        total = subtotal + tax_total
        total = Decimal("%.2f" % total)
        totals = {
            "subtotal": subtotal,
            "tax": tax_total,
            "total": total
        }

        for k, v in totals.items():
            setattr(self, k, v)

            if save is True:
                self.save()

        return totals


def order_pre_save(sender, instance, *args, **kwargs):
    instance.calculate(save=False)


pre_save.connect(order_pre_save, sender=Order)


# def order_post_save(sender, instance, created, *args, **kwargs):
#     if created:
#         instance.calculate(save=True)
#
#
# post_save.connect(order_post_save, sender=Order)
