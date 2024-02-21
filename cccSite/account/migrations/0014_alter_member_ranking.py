# Generated by Django 4.2.6 on 2024-02-21 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_alter_member_ranking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='ranking',
            field=models.SmallIntegerField(choices=[(2, 'trusted member'), (99, 'admin'), (1, 'member'), (98, 'moderator')], default=1),
        ),
    ]
