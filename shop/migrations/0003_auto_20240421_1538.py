# Generated by Django 3.2.4 on 2024-04-21 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_employee_expense_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='bulk_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='bulk_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='current_bulk_order',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
