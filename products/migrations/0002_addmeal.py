# Generated by Django 5.0.7 on 2024-08-22 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='addmeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('cattegory', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='image')),
            ],
        ),
    ]
