# Generated by Django 2.2 on 2020-06-28 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchRequests',
            fields=[
                ('query', models.CharField(max_length=250, primary_key=True, serialize=False)),
                ('dateAdded', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='SearchResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.TextField()),
                ('link', models.URLField()),
                ('source', models.CharField(max_length=50)),
                ('request', models.ManyToManyField(to='news.SearchRequests')),
            ],
        ),
    ]
