# Generated by Django 3.1.6 on 2021-06-10 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductUtil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('productutil_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.productutil')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('image', models.ImageField(upload_to='media/products')),
            ],
            bases=('products.productutil',),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('productutil_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.productutil')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('image', models.ImageField(upload_to='media/products')),
            ],
            bases=('products.productutil',),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('productutil_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.productutil')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='media/products')),
                ('description', models.TextField()),
                ('review', models.TextField()),
                ('rating', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('discounted_price', models.FloatField()),
                ('brands', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.brand')),
            ],
            bases=('products.productutil',),
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('productutil_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.productutil')),
                ('name', models.CharField(max_length=255)),
                ('items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='products.item')),
            ],
            bases=('products.productutil',),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('productutil_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.productutil')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('image', models.ImageField(upload_to='media/products')),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='products.category')),
            ],
            bases=('products.productutil',),
        ),
        migrations.CreateModel(
            name='ItemVariation',
            fields=[
                ('productutil_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.productutil')),
                ('value', models.CharField(max_length=250)),
                ('image', models.ImageField(upload_to='media/products')),
                ('variations', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_variations', to='products.variation')),
            ],
            bases=('products.productutil',),
        ),
        migrations.AddField(
            model_name='item',
            name='subcategories',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.subcategory'),
        ),
    ]
