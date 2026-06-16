# Generated manually: evita reservas duplicadas de la sala (misma fecha y hora).

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salapcs', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='salapc',
            unique_together={('date', 'hour')},
        ),
    ]
