# Generated by Django 5.0.4 on 2024-04-16 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('prod_id', models.IntegerField(primary_key=True, serialize=False)),
                ('prod_name', models.CharField(max_length=20)),
                ('prod_category', models.CharField(choices=[('mobile', 'MOBILE'), ('laptop', 'LAPTOP'), ('tv', 'TV')], max_length=100)),
                ('prod_desc', models.CharField(max_length=255)),
                ('prod_price', models.IntegerField()),
                ('prod_image', models.ImageField(upload_to='Product_Images')),
            ],
        ),
    ]
