# Generated by Django 2.1.5 on 2019-07-28 13:51

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CreditManagement', '0009_auto_20190728_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixedtransaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Money transferred'),
        ),
        migrations.AlterField(
            model_name='pendingtransaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Money transferred'),
        ),
    ]