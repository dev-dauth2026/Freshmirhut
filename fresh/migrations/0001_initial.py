# Generated by Django 3.1.3 on 2021-05-14 23:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveBigIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='productsf')),
                ('marked_price', models.PositiveBigIntegerField()),
                ('selling_price', models.PositiveBigIntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_by', models.CharField(max_length=200)),
                ('shipping_address', models.CharField(max_length=200)),
                ('mobile', models.CharField(max_length=10)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('subtotal', models.PositiveBigIntegerField()),
                ('discount', models.PositiveBigIntegerField()),
                ('total', models.PositiveBigIntegerField()),
                ('order_status', models.CharField(choices=[('Order Received', 'Order Received'), ('Order Processing', 'Order Processing'), ('On the way', 'On the way'), ('Order Delivered', 'Order Delivered'), ('Order Cancelled', 'Order Cancelled')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fresh.cart')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('joined_on', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveBigIntegerField()),
                ('quantity', models.PositiveBigIntegerField()),
                ('subtotal', models.PositiveBigIntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fresh.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fresh.product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fresh.customer'),
        ),
    ]
