# Generated by Django 5.0.7 on 2024-08-21 05:34

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='product',
            fields=[
                ('updated_at', models.DateField(auto_created=True)),
                ('created_at', models.DateField(auto_created=True)),
                ('pr_uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pr_name', models.CharField(max_length=100)),
                ('pr_slug', models.SlugField(unique=True)),
                ('pr_desc', models.TextField()),
                ('pr_price', models.IntegerField(default=0)),
                ('pr_demo_price', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='product_images',
            fields=[
                ('updated_at', models.DateField(auto_created=True)),
                ('created_at', models.DateField(auto_created=True)),
                ('pr_uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pr_images', models.ImageField(upload_to='products')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='productmetafield',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pr_measuring', models.CharField(blank=True, choices=[('kg', 'kg'), ('ml', 'ml'), ('L', 'L'), (None, None)], max_length=100, null=True)),
                ('pr_quantity', models.CharField(blank=True, max_length=100, null=True)),
                ('is_restrict', models.BooleanField(default=False)),
                ('restricted_quantity', models.IntegerField()),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='meta_field', to='products.product')),
            ],
        ),
    ]
