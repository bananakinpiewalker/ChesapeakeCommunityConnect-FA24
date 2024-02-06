# Generated by Django 4.2.6 on 2023-11-24 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=75)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.CharField(max_length=300)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]