from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='products'
    )

    class Meta:
        ordering = ['name']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0), name='product_price_gte_0'
            ),
            models.CheckConstraint(
                condition=models.Q(stock__gte=0), name='product_stock_gte_0'
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name='orders'
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(
        Product, through='OrderItem', related_name='orders'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.pk} - {self.customer.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items'
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='order_items'
    )
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'product'], name='unique_product_per_order'
            ),
            models.CheckConstraint(
                condition=models.Q(quantity__gte=1), name='orderitem_quantity_gte_1'
            ),
            models.CheckConstraint(
                condition=models.Q(unit_price__gte=0), name='orderitem_unit_price_gte_0'
            ),
        ]

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in order #{self.order_id}" 