from django.db import models
from django.conf import settings
from django.utils import timezone

class Invoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=(('mpesa', 'M-Pesa'), ('paypal', 'PayPal')))
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # amount = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    
    def __str__(self):
        return f"Invoice #{self.id} - {self.payment_method} - {self.amount}"

