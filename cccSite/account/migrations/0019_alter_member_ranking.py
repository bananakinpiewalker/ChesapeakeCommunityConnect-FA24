# Generated by Django 4.2.6 on 2024-03-05 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_alter_member_ranking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='ranking',
            field=models.SmallIntegerField(choices=[(2, 'trusted member'), (1, 'member'), (-1, 'banned'), (98, 'moderator'), (99, 'admin')], default=1),
        ),
    ]
