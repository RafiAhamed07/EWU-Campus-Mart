# Generated manually on 2026-04-05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0005_seed_builtin_categories_and_allow_empty_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="productoption",
            name="offer_price",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
