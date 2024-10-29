# Generated by Django 5.1.1 on 2024-10-29 10:23

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Invoice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "payment_method",
                    models.CharField(
                        choices=[("mpesa", "M-Pesa"), ("paypal", "PayPal")],
                        max_length=50,
                    ),
                ),
                ("transaction_id", models.CharField(max_length=100, unique=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("date", models.DateTimeField(default=django.utils.timezone.now)),
                ("description", models.TextField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
