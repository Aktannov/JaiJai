# Generated by Django 4.0 on 2022-01-17 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0004_alter_rating_user_alter_rating_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
    ]