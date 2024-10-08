# Generated by Django 5.1.1 on 2024-09-05 02:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("goods", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "Category", "verbose_name_plural": "Categories"},
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=150, unique=True, verbose_name="Title"),
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(
                blank=True, max_length=200, null=True, unique=True, verbose_name="URL"
            ),
        ),
        migrations.CreateModel(
            name="Product",
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
                    "name",
                    models.CharField(max_length=150, unique=True, verbose_name="Title"),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        max_length=200,
                        null=True,
                        unique=True,
                        verbose_name="URL",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="goods_images",
                        verbose_name="Imagies",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=None,
                        max_digits=7,
                        verbose_name="Price",
                    ),
                ),
                (
                    "discount",
                    models.DecimalField(
                        decimal_places=2,
                        default=None,
                        max_digits=7,
                        verbose_name="Discount %",
                    ),
                ),
                (
                    "quantity",
                    models.PositiveIntegerField(default=0, verbose_name="Quantity"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="goods.category",
                        verbose_name="Category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
                "db_table": "product",
            },
        ),
    ]
