
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comercio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('sector', models.CharField(max_length=100)),
                ('subsector', models.CharField(max_length=100)),
                ('articulos', models.TextField()),
                ('direccion', models.CharField(max_length=300)),
                ('celular', models.CharField(blank=True, max_length=20)),
                ('telefono', models.CharField(blank=True, max_length=20)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('link_maps', models.URLField(blank=True)),
                ('link_facebook', models.URLField(blank=True)),
                ('link_instagram', models.URLField(blank=True)),
            ],
        ),
    ]