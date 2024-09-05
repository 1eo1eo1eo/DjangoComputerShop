from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Title",
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        null=True,
        verbose_name="URL",
    )

    class Meta:
        db_table: str = "category"
        verbose_name: str = "Category"
        verbose_name_plural: str = "Categories"

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Title",
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        null=True,
        verbose_name="URL",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
    )
    image = models.ImageField(
        upload_to="goods_images",
        blank=True,
        null=True,
        verbose_name="Imagies",
    )
    price = models.DecimalField(
        default=None,
        max_digits=7,
        decimal_places=2,
        verbose_name="Price",
    )
    discount = models.DecimalField(
        default=None,
        max_digits=7,
        decimal_places=2,
        verbose_name="Discount %",
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Quantity",
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        verbose_name="Category",
    )

    class Meta:
        db_table: str = "product"
        verbose_name: str = "Product"
        verbose_name_plural: str = "Products"

    def __str__(self) -> str:
        return self.name
