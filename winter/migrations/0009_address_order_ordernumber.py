# Generated by Django 3.1 on 2020-10-01 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('winter', '0008_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.IntegerField()),
                ('address1', models.TextField()),
                ('address2', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zipcode', models.IntegerField()),
                ('register', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='winter.register')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='winter.product')),
                ('register', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='winter.register')),
            ],
        ),
        migrations.CreateModel(
            name='OrderNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='winter.address')),
                ('order', models.ManyToManyField(to='winter.Order')),
                ('register', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='winter.register')),
            ],
        ),
    ]
