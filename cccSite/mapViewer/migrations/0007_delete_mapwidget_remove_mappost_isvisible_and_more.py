# Generated by Django 4.2.6 on 2024-03-05 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Filterer', '0007_delete_postfilterassoc_delete_postfilters'),
        ('mapViewer', '0006_remove_mappost_latitude_remove_mappost_longitude'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MapWidget',
        ),
        migrations.RemoveField(
            model_name='mappost',
            name='isVisible',
        ),
        migrations.AddField(
            model_name='mappost',
            name='visibility',
            field=models.SmallIntegerField(choices=[(-1, 'denied'), (2, 'visible'), (0, 'pending')], default=0),
        ),
    ]
