# Generated by Django 4.2.5 on 2023-11-05 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_rename_newcomment_new_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new_listing',
            name='category',
            field=models.CharField(choices=[('None', 'Na'), ('New', 'N'), ('Used', 'U'), ('Junk', 'J')], max_length=20),
        ),
    ]
