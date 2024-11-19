from django.db import models
from django import forms

from django.contrib.auth.models import User
from django.utils.timezone import now

class Customer(models.Model):
    GENDER_CHOICES = (
       ('M', 'Male'),
       ('F', 'Female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="")
    phone = models.BigIntegerField()
    profile_pic = models.ImageField(null=True, upload_to="customer_pic", default="userimg.png")
    gender = models.CharField(choices=GENDER_CHOICES, max_length=50)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


TAG = (
    ('New', 'New'),
    ('Bestseller', 'Bestseller'),
    ('Trending', 'Trending'),
    ('Featured', 'Featured'),
    ('Sale', 'Sale'),
)


from django.db.models.signals import post_save
from django.dispatch import receiver



class Size(models.Model):
    size_label = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.size_label

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    price = models.IntegerField(default=0)
    bulk_price = models.IntegerField(default=0)  # Оптовая цена
    bulk_quantity = models.IntegerField(default=0)  # Количество для оптовой покупки
    current_bulk_order = models.IntegerField(default=0, editable=False)  # Текущее количество заказанных оптом единиц
    tag = models.CharField(default="New", choices=TAG, max_length=20)
    product_img = models.ImageField(upload_to="images", default="product.jpg")
    product_img1 = models.ImageField(upload_to="images", default="product.jpg")
    product_img2 = models.ImageField(upload_to="images", default="product.jpg")
    file = models.FileField(upload_to='file', null=True, blank=True)
    is_free = models.BooleanField(default=False)
    sizes = models.ManyToManyField(Size, related_name="products")

    def __str__(self):
        return self.product_name

    @property
    def is_bulk_ready(self):
        """Проверяет, достигнуто ли необходимое количество для оптовой покупки."""
        return self.current_bulk_order >= self.bulk_quantity

# Signal to update the current_bulk_order when a cart item is added or updated


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField()
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True)

    @property
    def price(self):
        return self.product.price

    @property
    def amount(self):
        return self.qty * self.product.price

    def __str__(self):
        return self.product.product_name + " by " + self.user.username

@receiver(post_save, sender=Cart)
def update_bulk_order(sender, instance, **kwargs):
    product = instance.product
    if product:
        # Обновляем текущее количество заказанных оптом единиц
        total_qty = Cart.objects.filter(product=product).aggregate(models.Sum('qty'))['qty__sum'] or 0
        product.current_bulk_order = total_qty
        product.save()



STATUS = (
    ('Placed', 'Placed'),
    ('Confirmed', 'Confirmed'),
    ('Preparing', 'Preparing'),
    ('Shipped', 'Shipped'),
    ('Out For Delivery', 'Out For Delivery'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    phone = models.BigIntegerField(null=True)
    house_no = models.CharField(null=True, max_length=20)
    street = models.CharField(null=True, max_length=50)
    city = models.CharField(null=True, max_length=20)
    pin = models.IntegerField(null=True)
    state = models.CharField(null=True, max_length=20)
    total = models.FloatField()
    code = models.CharField(max_length=15, default="")
    placed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code + " to " + self.first_name + "\t" + self.last_name

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS, default='Placed')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name + " by " + self.user.first_name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default="")
    subject = models.CharField(max_length=50)
    review = models.CharField(max_length=200)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name 


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_on = models.DateField(default=now, editable=False)

    def __str__(self):
        return self.user.first_name + " - " + self.product.product_name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.position}"

class Expense(models.Model):
    EXPENSE_TYPE_CHOICES = (
        ('Utilities', 'Utilities'),
        ('Rent', 'Rent'),
        ('Salaries', 'Salaries'),
        ('Maintenance', 'Maintenance'),
        ('Other', 'Other'),
    )
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50, choices=EXPENSE_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.type} - {self.date} - ${self.amount}"

class Report(models.Model):
    REPORT_TYPE_CHOICES = (
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Annual', 'Annual'),
    )
    type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    date = models.DateField()
    total_income = models.DecimalField(max_digits=12, decimal_places=2)
    total_expense = models.DecimalField(max_digits=12, decimal_places=2)
    net_profit = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.net_profit = self.total_income - self.total_expense
        super(Report, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.type} Report - {self.date}"
