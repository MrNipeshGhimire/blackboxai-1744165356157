# Generated by Django 5.2 on 2025-04-09 02:50

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tracker", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Budget",
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
                ("name", models.CharField(max_length=100)),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0.01)],
                    ),
                ),
                (
                    "period",
                    models.CharField(
                        choices=[
                            ("WEEKLY", "Weekly"),
                            ("MONTHLY", "Monthly"),
                            ("CUSTOM", "Custom"),
                        ],
                        default="MONTHLY",
                        max_length=10,
                    ),
                ),
                ("start_date", models.DateField(default=django.utils.timezone.now)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("category", models.CharField(blank=True, max_length=50)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["-start_date"],
            },
        ),
        migrations.AddField(
            model_name="transaction",
            name="category",
            field=models.CharField(
                choices=[
                    ("FOOD", "Food"),
                    ("TRANSPORT", "Transport"),
                    ("HOUSING", "Housing"),
                    ("UTILITIES", "Utilities"),
                    ("ENTERTAINMENT", "Entertainment"),
                    ("HEALTH", "Health"),
                    ("SHOPPING", "Shopping"),
                    ("EDUCATION", "Education"),
                    ("OTHER", "Other"),
                ],
                default="OTHER",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="transaction",
            name="receipt",
            field=models.ImageField(blank=True, null=True, upload_to="receipts/"),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="currency",
            field=models.CharField(default="USD", max_length=3),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="dark_mode",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="monthly_limit",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="weekly_limit",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
        migrations.AddIndex(
            model_name="transaction",
            index=models.Index(fields=["date"], name="tracker_tra_date_a467f2_idx"),
        ),
        migrations.AddIndex(
            model_name="transaction",
            index=models.Index(
                fields=["category"], name="tracker_tra_categor_09c75e_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="transaction",
            index=models.Index(
                fields=["transaction_type"], name="tracker_tra_transac_3aebc6_idx"
            ),
        ),
        migrations.AddField(
            model_name="budget",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
