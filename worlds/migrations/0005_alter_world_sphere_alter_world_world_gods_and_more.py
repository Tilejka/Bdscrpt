# Generated by Django 4.1.7 on 2023-07-29 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worlds', '0004_worldgod_sphere'),
    ]

    operations = [
        migrations.AlterField(
            model_name='world',
            name='sphere',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='world_sphere', to='worlds.sphere'),
        ),
        migrations.AlterField(
            model_name='world',
            name='world_gods',
            field=models.ManyToManyField(blank=True, related_name='world_gods', to='worlds.worldgod'),
        ),
        migrations.RemoveField(
            model_name='worldgod',
            name='domains',
        ),
        migrations.AddField(
            model_name='worldgod',
            name='domains',
            field=models.ManyToManyField(to='worlds.domain'),
        ),
    ]