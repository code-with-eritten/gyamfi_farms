# Generated by Django 5.1.7 on 2025-03-21 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='liveanimal',
            name='product',
        ),
        migrations.RemoveField(
            model_name='meat',
            name='product',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_category',
        ),
        migrations.AddField(
            model_name='product',
            name='age',
            field=models.PositiveIntegerField(blank=True, help_text='Age in months', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='breed',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='cut_type',
            field=models.CharField(blank=True, help_text='E.g., Leg, Breast, Whole', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='gender',
            field=models.CharField(blank=True, choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='is_frozen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='packaging',
            field=models.CharField(blank=True, help_text='E.g., Vacuum sealed, Fresh', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity_per_pack',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Weight in kg', max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='weight_per_unit',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Weight per unit in kg', max_digits=6, null=True),
        ),
        migrations.DeleteModel(
            name='Egg',
        ),
        migrations.DeleteModel(
            name='LiveAnimal',
        ),
        migrations.DeleteModel(
            name='Meat',
        ),
        migrations.DeleteModel(
            name='ProductCategory',
        ),
    ]
